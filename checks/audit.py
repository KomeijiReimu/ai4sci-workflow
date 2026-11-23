"""Audit a research project against checks/contract.md; no third-party modules."""

import argparse
from collections import Counter
import csv
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import hashlib
import json
from pathlib import Path, PureWindowsPath
import re
import sys

if __package__:
    from .common import DECIMAL, Findings, number, table
    from .sources import load_sources
else:
    from common import DECIMAL, Findings, number, table
    from sources import load_sources


STATUSES = {"supported", "partial", "unsupported", "contradicted", "untested"}
MARKER = re.compile(r"\[(C[0-9]+)\]")
# Skip ASCII identifier suffixes like ResNet-50 before recognizing numeric
# tokens. A mathematical minus is never a name separator. A decimal point
# followed by a digit, or an exponent, makes the suffix a number, not a label.
DISPLAY_DECIMAL = DECIMAL.replace("[+-]", "[+−-]")
TOKEN = re.compile(rf"(?<!\w)[A-Za-z_]\w*-[0-9]+(?!\w|\.[0-9])|"
                   rf"(?:(?=[+−-])|(?<![\w.]))(?P<number>{DISPLAY_DECIMAL})(?!\w)", re.ASCII)
INPUT_ERRORS = (ValueError, OSError, RuntimeError, csv.Error, InvalidOperation)


def numeric_tokens(raw):
    # Keep offsets in the literal text and normalize only numeric spellings.
    for match in TOKEN.finditer(raw):
        if match.lastgroup == "number":
            yield match.span(), match.group().replace("−", "-")


def relative_name(name):
    if (not isinstance(name, str) or not name or "\\" in name or "\0" in name or
            PureWindowsPath(name).drive or any(p in ("", ".", "..") for p in name.split("/"))):
        raise ValueError("path must be a project-relative file without traversal")


def local_file(root, name):
    relative_name(name)
    path = (root / name).resolve(strict=True)
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError("path must resolve to a regular file inside PROJECT")
    return path


def file_id(path):
    stat = path.stat()
    return stat.st_dev, stat.st_ino


def unique_object(pairs):
    result = {}
    for k, v in pairs:
        if k in result:
            raise ValueError(f"duplicate JSON field {k!r}")
        result[k] = v
    return result


def reject_constant(token):
    raise ValueError(f"non-finite JSON number {token}")


def manifest(raw, name):
    data = json.loads(raw.decode("utf-8"),
                      object_pairs_hook=unique_object, parse_float=Decimal,
                      parse_constant=reject_constant)
    if not isinstance(data, dict):
        raise ValueError(f"{name}: expected a JSON object")
    return data


def text(obj, field):
    if not isinstance(obj, dict) or not isinstance(obj.get(field), str) or not obj[field].strip():
        raise ValueError(f"missing or blank text field: {field}")
    return obj[field]


def records(obj, field):
    rows = obj.get(field)
    if not isinstance(rows, list):
        raise ValueError(f"{field}: expected an array")
    return rows


def cell_fields(entry):
    key = entry.get("key")
    if (not isinstance(key, dict) or not key or
            any(not k.strip() or not isinstance(v, str) or not v.strip() for k, v in key.items())):
        raise ValueError("key must map nonblank columns to nonblank CSV strings")
    col = text(entry, "column")
    if col in key:
        raise ValueError("result column cannot be a key")
    return key, col


def parse_plan(raw: bytes) -> dict:
    plan = manifest(raw, "research/plan.json")
    text(plan, "question")
    criteria = set()
    for row in records(plan, "criteria"):
        criterion = text(row, "id")
        text(row, "description")
        if criterion in criteria:
            raise ValueError(f"duplicate criterion {criterion}")
        criteria.add(criterion)
        if "required_observations" in row:
            entries = records(row, "required_observations")
            if not entries:
                raise ValueError(f"{criterion}: required_observations cannot be empty")
            seen = set()
            for index, entry in enumerate(entries):
                try:
                    if not isinstance(entry, dict) or set(entry) - {"bounds"} != {"path", "key", "column"}:
                        raise ValueError("expected path, key, column and optional bounds")
                    name = text(entry, "path")
                    relative_name(name)
                    key, col = cell_fields(entry)
                    if "bounds" in entry:
                        bounds = entry["bounds"]
                        if (not isinstance(bounds, dict) or set(bounds) != {"min", "max"} or
                                any(type(v) not in (int, Decimal) for v in bounds.values())):
                            raise ValueError("bounds requires JSON numbers min and max")
                        if number(bounds["min"]) > number(bounds["max"]):
                            raise ValueError("bounds.min exceeds bounds.max")
                    locator = (name, tuple(sorted(key.items())), col)
                    if locator in seen:
                        raise ValueError(f"duplicate cell: {locator}")
                    seen.add(locator)
                except ValueError as exc:
                    raise ValueError(f"{criterion}.required_observations[{index}]: {exc}") from exc
    if not criteria:
        raise ValueError("plan requires at least one criterion")
    if "matched_conditions" in plan:
        names = records(plan, "matched_conditions")
        if (not names or any(not isinstance(k, str) or not k.strip() for k in names)
                or len(set(names)) != len(names)):
            raise ValueError("matched_conditions must contain distinct nonblank names")
    if "require_source_manifest" in plan and type(plan["require_source_manifest"]) is not bool:
        raise ValueError("require_source_manifest must be Boolean")
    return plan


def csv_cell(path, key, col, tables):
    if path not in tables:
        tables[path] = table(path)
    header, rows = tables[path]
    if col not in header or not key.keys() <= set(header):
        raise ValueError("unknown result or key column")
    matches = [i for i, r in enumerate(rows) if all(r[k] == v for k, v in key.items())]
    if len(matches) != 1:
        raise ValueError(f"key matched {len(matches)} rows, expected one")
    i = matches[0]
    return i, number(rows[i][col])


def audit(root):
    errors = Findings()
    states = {}
    pending = Findings()
    scientific_run = None
    coverage = {}
    observation_outcomes = {}
    source_records = None
    try:
        root = root.resolve(strict=True)
        controls = {name: local_file(root, "research/" + name) for name in
                    ("plan.json", "plan.sha256", "run.json", "claims.json", "paper.md")}
        control_ids = {file_id(path) for path in controls.values()}
        raw = controls["plan.json"].read_bytes()
        expected = hashlib.sha256(raw).hexdigest().encode("ascii") + b"\n"
        if controls["plan.sha256"].read_bytes() != expected:
            raise ValueError("research/plan.sha256: digest differs from frozen plan")
        plan = parse_plan(raw)
        coverage = {row["id"]: {"required_observations": len(row.get("required_observations", [])),
                                "verified_observations": 0} for row in plan["criteria"]}
        observations = []
        for row in plan["criteria"]:
            cid = row["id"]
            observation_outcomes[cid] = []
            for entry in row.get("required_observations", []):
                receipt = None
                if "bounds" in entry:
                    receipt = {k: entry[k] for k in ("path", "key", "column")}
                    receipt["outcome"] = "not_evaluated"
                    observation_outcomes[cid].append(receipt)
                observations.append((cid, entry, receipt))
        registry = load_sources(root, plan, local_file, file_id, manifest, control_ids)
        if registry is not None:
            source_records = len(registry)
        run = manifest(controls["run.json"].read_bytes(), "research/run.json")
        if "plan_sha256" in run and run["plan_sha256"] != expected[:-1].decode("ascii"):
            raise ValueError("run.plan_sha256 differs from frozen plan digest")
        declared = text(run, "status")
        tables = {}
        cell_outcomes = {}
        for criterion, entry, receipt in observations:
            name, key, col = entry["path"], entry["key"], entry["column"]
            try:
                if declared == "not-applicable":
                    raise ValueError("required observation requires an experiment")
                if declared == "completed":
                    if name not in records(run, "outputs"):
                        raise ValueError("missing from declared run outputs")
                    path = local_file(root, name)
                    i, csv_value = csv_cell(path, key, col, tables)
                    cell = (criterion, file_id(path), i, col)
                    if cell in cell_outcomes:
                        raise ValueError("duplicate cell")
                    outcome = None
                    if receipt is not None:
                        bounds = entry["bounds"]
                        # Direct comparison of Fraction with Decimal/int is exact.
                        outcome = "met" if bounds["min"] <= csv_value <= bounds["max"] else "missed"
                        receipt["outcome"] = outcome
                    cell_outcomes[cell] = outcome
                    coverage[criterion]["verified_observations"] += 1
            except INPUT_ERRORS as exc:
                errors.add(f"{criterion}: required observation {name} {key} {col}: {exc}")
        outputs = set()
        if declared == "completed" or "sha256" in run or "outputs" in run:
            hashes = run.get("sha256", {})
            if not isinstance(hashes, dict):
                raise ValueError("run.sha256 must map output names to SHA-256 digests")
            for name in records(run, "outputs"):
                path = local_file(root, name)
                identity = file_id(path)
                if identity in control_ids:
                    raise ValueError("run output cannot be a project control file")
                if identity in outputs:
                    raise ValueError("research/run.json: duplicate output path")
                outputs.add(identity)
                if "sha256" in run:
                    digest = hashlib.sha256()
                    with path.open("rb") as stream:
                        for chunk in iter(lambda: stream.read(1048576), b""):
                            digest.update(chunk)
                    if hashes.get(name) != digest.hexdigest():
                        raise ValueError(f"missing or incorrect run.sha256 digest: {name}")
            if hashes.keys() - set(run["outputs"]):
                raise ValueError("run.sha256 contains an undeclared output")
        if declared == "completed":
            text(run, "command")
            if not outputs:
                raise ValueError("research/run.json: completed run has no outputs")
        elif declared in {"failed", "blocked", "not-applicable"}:
            reason = text(run, "reason")
            if declared != "not-applicable":
                pending.add(f"scientific run {declared}: {reason}")
        else:
            raise ValueError("research/run.json: unknown status")
        scientific_run = declared
        if "matched_conditions" in plan:
            names = plan["matched_conditions"]
            if declared == "not-applicable":
                raise ValueError("matched_conditions requires an experiment")
            if declared == "completed":
                arms = records(run, "arms")
                if len(arms) < 2:
                    raise ValueError("matched_conditions requires at least two arms")
                ids, reference = set(), {}
                for arm in arms:
                    aid = text(arm, "id")
                    if aid in ids:
                        raise ValueError(f"duplicate arm ID: {aid}")
                    ids.add(aid)
                    conditions = arm.get("conditions")
                    for key in names:
                        val = conditions.get(key) if isinstance(conditions, dict) else None
                        if not isinstance(val, (str, int, Decimal)) or isinstance(val, str) and not val.strip():
                            raise ValueError(f"arm {aid}: missing or invalid condition {key}")
                        # JSON true is not the number 1; JSON 1.0 and 1 are equal.
                        tagged = (isinstance(val, bool), val)
                        if reference.setdefault(key, tagged) != tagged:
                            raise ValueError(f"arm {aid}: condition {key} differs from first arm")
        claims = records(manifest(controls["claims.json"].read_bytes(), "research/claims.json"), "claims")
        paper = controls["paper.md"].read_text(encoding="utf-8")
        if not paper.strip():
            raise ValueError("empty manuscript")
        criteria = set(coverage)

        covered = set()
        statements = set()
        markers = MARKER.findall(paper)
        paper_lines = {line.strip() for line in paper.splitlines()}
        sources, source_tokens = {}, {}
        for index, claim in enumerate(claims):
            label = f"claims[{index}]"
            try:
                cid = text(claim, "id")
                label = cid
                if not re.fullmatch(r"C[1-9][0-9]*", cid) or cid in states:
                    raise ValueError("invalid or duplicate claim ID")
                states[cid] = "invalid"
                criterion = text(claim, "criterion")
                if criterion not in criteria:
                    raise ValueError("unknown criterion")
                covered.add(criterion)
                status = text(claim, "status")
                if status not in STATUSES:
                    raise ValueError("unknown status")
                statement = text(claim, "statement")
                if statement in statements or MARKER.search(statement):
                    raise ValueError("duplicate statement or embedded marker")
                statements.add(statement)
                if markers.count(cid) != 1 or f"{statement} [{cid}]" not in paper_lines:
                    raise ValueError("expected one manuscript line: statement [ID]")

                tokens = list(numeric_tokens(statement))
                reported = Counter(d for _, d in tokens)
                number_counts = Counter()
                quoted_spans = {}
                key_spans = set()
                seen = set()
                verified = 0
                has_gap = False
                for entry in records(claim, "evidence"):
                    kind = text(entry, "kind")
                    if "numeric_outcome" in entry and kind != "number":
                        raise ValueError("numeric_outcome requires number evidence")
                    if kind in {"incomplete", "blocked"}:
                        reason = text(entry, "reason")
                        locator = (kind, reason)
                        pending.add(f"{cid}: {kind}: {reason}")
                        has_gap = True
                    else:
                        path = local_file(root, text(entry, "path"))
                        identity = file_id(path)
                        if identity in control_ids:
                            raise ValueError("evidence cannot cite a project control file")
                        if kind == "quote":
                            if registry is not None and identity not in registry:
                                raise ValueError(f"missing source registration: {path}")
                            quote = text(entry, "quote")
                            if path not in sources:
                                sources[path] = path.read_text(encoding="utf-8")
                            if quote not in sources[path]:
                                raise ValueError("source does not contain literal quote")
                            if "displays" in entry:
                                displays = records(entry, "displays")
                                if not all(isinstance(d, str) for d in displays):
                                    raise ValueError("quote displays must be numeric strings")
                                wanted = {d.replace("−", "-") for d in displays}
                                if len(wanted) != len(displays) or not wanted <= reported.keys():
                                    raise ValueError("quote displays must be distinct numeric tokens in both quote and statement")
                                # Count actual source tokens, not arbitrary numeric
                                # substrings, and don't count one overlapping excerpt twice.
                                if path not in source_tokens:
                                    source_tokens[path] = {span for span, _ in numeric_tokens(sources[path])}
                                quoted = [(span, d) for span, d in numeric_tokens(quote) if d in wanted]
                                offset = sources[path].find(quote)
                                while offset != -1:
                                    proof = {(identity, offset + a, offset + b): d for (a, b), d in quoted
                                             if (offset + a, offset + b) in source_tokens[path]}
                                    if wanted == set(proof.values()):
                                        quoted_spans.update(proof)
                                        break
                                    offset = sources[path].find(quote, offset + 1)
                                else:
                                    raise ValueError("quote displays must occur as numeric tokens in the source quote")
                            locator = (kind, identity, quote)
                        elif kind == "number":
                            if scientific_run == "completed" and identity not in outputs:
                                raise ValueError("numeric evidence CSV not declared in run outputs")
                            if scientific_run == "not-applicable":
                                raise ValueError("numeric evidence requires an experiment run record, not literature-only")
                            key, col = cell_fields(entry)
                            i, csv_value = csv_cell(path, key, col, tables)
                            if "numeric_outcome" in entry:
                                declared_outcome = entry["numeric_outcome"]
                                if declared_outcome not in ("met", "missed"):
                                    raise ValueError("numeric_outcome must be met or missed")
                                actual = cell_outcomes.get((criterion, identity, i, col))
                                if declared_outcome != actual:
                                    raise ValueError(f"{criterion}: numeric_outcome {declared_outcome} for "
                                                     f"{entry['path']} {key} {col}; frozen outcome: {actual or 'none'}")
                            if any(type(entry.get(k)) not in (int, Decimal) for k in ("value", "atol")):
                                raise ValueError("value and atol must be JSON numbers")
                            value, tol = number(entry["value"]), number(entry["atol"])
                            display = entry.get("display", str(entry["value"]))
                            if not isinstance(display, str):
                                raise ValueError("display must be a numeric string")
                            display = display.replace("−", "-")
                            if number(display) != value:
                                raise ValueError("display must denote value exactly")
                            # Decimal preserves trailing zeros and includes the scientific
                            # exponent; Fraction avoids dependence on decimal context precision.
                            exponent = Decimal(display).as_tuple().exponent
                            assert isinstance(exponent, int)  # number(display) verified a finite decimal
                            half_unit = Fraction(10) ** exponent / 2
                            if abs(csv_value - value) > min(tol, half_unit):
                                raise ValueError("CSV result differs from value beyond atol or display rounding precision")
                            number_counts[display] += 1
                            for k, v in key.items():
                                key_spans.update(span for span, d in tokens if d == v.replace("−", "-") and
                                                 re.search(rf"(?<!\w){re.escape(k)}=$", statement[:span[0]], re.ASCII))
                            locator = (kind, identity, i, col)
                        else:
                            raise ValueError("unknown evidence kind")
                        verified += 1
                    if locator in seen:
                        raise ValueError("duplicate evidence")
                    seen.add(locator)
                if status in {"supported", "partial", "contradicted"} and not verified:
                    raise ValueError(f"{status} requires verified evidence")
                if status == "supported" and has_gap:
                    raise ValueError("supported claim declares an evidence gap")
                results = Counter(d for span, d in tokens if span not in key_spans)
                if not number_counts.keys() <= results.keys():
                    raise ValueError("display not found as a non-key numeric token in statement")
                unbound = results - number_counts - Counter(quoted_spans.values())
                if status in {"supported", "partial"} and unbound:
                    raise ValueError(f"unbound numeric token in statement: {next(iter(unbound))}")
                states[cid] = status
                if status != "supported":
                    pending.add(f"{cid}: {status}")
            except INPUT_ERRORS as exc:
                errors.add(f"{label}: {exc}")
        for cid in sorted(set(markers) - states.keys()):
            errors.add(f"unknown manuscript marker [{cid}]")
        for criterion in sorted(criteria - covered):
            errors.add(f"uncovered criterion: {criterion}")
    except INPUT_ERRORS as exc:
        errors.add(exc)
    code = 2 if errors.count else 1 if pending.count else 0
    return code, {"run": "invalid" if errors.count else "complete", "scientific_run": scientific_run, "claims": states,
                  "criterion_coverage": coverage, "observation_outcomes": observation_outcomes,
                  "source_records": source_records,
                  "deliverability": ("ready", "incomplete", "blocked")[code],
                  "error_count": errors.count, "errors": errors.messages,
                  "incomplete_count": pending.count, "incomplete": pending.messages}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    status, report = audit(parser.parse_args().project)
    print(json.dumps(report, sort_keys=True))
    sys.exit(status)
