"""Audit a research project against checks/contract.md; no third-party modules."""

import argparse
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path, PureWindowsPath
import re
import sys

from common import DECIMAL, Findings, number, table


STATUSES = {"supported", "partial", "unsupported", "contradicted", "untested"}
MARKER = re.compile(r"\[(C[0-9]+)\]")
# Digits inside identifiers (e.g. CO2) are not numeric tokens. A trailing
# sentence period is punctuation, not part of the displayed number.
TOKEN = re.compile(rf"(?<![\w.])({DECIMAL})(?!\w)", re.ASCII)
INPUT_ERRORS = (ValueError, OSError, RuntimeError, csv.Error, InvalidOperation)


def local_file(root, name):
    if (not isinstance(name, str) or not name or "\\" in name or
            PureWindowsPath(name).drive or any(p in ("", ".", "..") for p in name.split("/"))):
        raise ValueError("path must be a project-relative file without traversal")
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


def audit(root):
    errors = Findings()
    states = {}
    pending = Findings()
    scientific_run = None
    try:
        root = root.resolve(strict=True)
        controls = {name: local_file(root, "research/" + name) for name in
                    ("plan.json", "plan.sha256", "run.json", "claims.json", "paper.md")}
        control_ids = {file_id(path) for path in controls.values()}
        raw = controls["plan.json"].read_bytes()
        expected = hashlib.sha256(raw).hexdigest().encode("ascii") + b"\n"
        if controls["plan.sha256"].read_bytes() != expected:
            raise ValueError("research/plan.sha256: digest differs from frozen plan")
        plan = manifest(raw, "research/plan.json")
        run = manifest(controls["run.json"].read_bytes(), "research/run.json")
        declared = text(run, "status")
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
            names = records(plan, "matched_conditions")
            if (not names or any(not isinstance(k, str) or not k.strip() for k in names)
                    or len(set(names)) != len(names)):
                raise ValueError("matched_conditions must contain distinct nonblank names")
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
        text(plan, "question")
        criteria = set()
        for row in records(plan, "criteria"):
            criterion = text(row, "id")
            text(row, "description")
            if criterion in criteria:
                raise ValueError(f"duplicate criterion {criterion}")
            criteria.add(criterion)
        if not criteria:
            raise ValueError("plan requires at least one criterion")

        covered = set()
        statements = set()
        markers = MARKER.findall(paper)
        paper_lines = {line.strip() for line in paper.splitlines()}
        tables, sources = {}, {}
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

                bound = set()
                tokens = list(TOKEN.finditer(statement))
                seen = set()
                verified = 0
                has_gap = False
                for entry in records(claim, "evidence"):
                    kind = text(entry, "kind")
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
                            quote = text(entry, "quote")
                            if path not in sources:
                                sources[path] = path.read_text(encoding="utf-8")
                            if quote not in sources[path]:
                                raise ValueError("source does not contain literal quote")
                            if "displays" in entry:
                                displays = records(entry, "displays")
                                quoted = set(TOKEN.findall(quote))
                                reported = {m.group() for m in tokens}
                                if (any(not isinstance(d, str) or d not in quoted or d not in reported for d in displays)
                                        or len(set(displays)) != len(displays)):
                                    raise ValueError("quote displays must be distinct numeric tokens in both quote and statement")
                                bound.update(m.span() for m in tokens if m.group() in displays)
                            locator = (kind, identity, quote)
                        elif kind == "number":
                            if scientific_run == "completed" and identity not in outputs:
                                raise ValueError("numeric evidence CSV not declared in run outputs")
                            if scientific_run == "not-applicable":
                                raise ValueError("numeric evidence requires an experiment run record, not literature-only")
                            key = entry.get("key")
                            if not isinstance(key, dict) or not key or any(not isinstance(v, str) or not v.strip() for v in key.values()):
                                raise ValueError("number.key must map columns to nonblank CSV strings")
                            col = text(entry, "column")
                            if col in key:
                                raise ValueError("result column cannot be a key")
                            if path not in tables:
                                tables[path] = table(path)
                            header, rows = tables[path]
                            if col not in header or not key.keys() <= set(header):
                                raise ValueError("unknown result or key column")
                            matches = [r for r in rows if all(r[k] == v for k, v in key.items())]
                            if len(matches) != 1:
                                raise ValueError(f"key matched {len(matches)} rows, expected one")
                            if any(type(entry.get(k)) not in (int, Decimal) for k in ("value", "atol")):
                                raise ValueError("value and atol must be JSON numbers")
                            value, tol = number(entry["value"]), number(entry["atol"])
                            if tol < 0 or abs(number(matches[0][col]) - value) > tol:
                                raise ValueError("CSV result differs from value or invalid tolerance")
                            display = entry.get("display", str(entry["value"]))
                            if not isinstance(display, str) or number(display) != value:
                                raise ValueError("display must denote value exactly")
                            occurrences = [m for m in tokens if m.group() == display]
                            if not occurrences:
                                raise ValueError("display not found as numeric token in statement")
                            bound.update(m.span() for m in occurrences)
                            for k, v in key.items():
                                bound.update(m.span() for m in tokens if m.group() == v and
                                             re.search(rf"(?<!\w){re.escape(k)}=$", statement[:m.start()], re.ASCII))
                            locator = (kind, identity, tuple(sorted(key.items())), col)
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
                if status in {"supported", "partial"} and any(m.span() not in bound for m in tokens):
                    raise ValueError("unbound numeric token in statement")
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
                  "deliverability": ("ready", "incomplete", "blocked")[code],
                  "error_count": errors.count, "errors": errors.messages,
                  "incomplete_count": pending.count, "incomplete": pending.messages}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    status, report = audit(parser.parse_args().project)
    print(json.dumps(report, sort_keys=True))
    sys.exit(status)
