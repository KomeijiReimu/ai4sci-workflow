"""Focused offline CLI contracts. No model calls or simulated research runs."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Any
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Fixture(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / ".local" / "test-checks"
        scratch.mkdir(parents=True, exist_ok=True)
        tmp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(tmp.cleanup)
        self.work = Path(tmp.name)

    def cli(self, script, *args, code):
        result = subprocess.run([sys.executable, str(ROOT / "checks" / script), *map(str, args)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        return json.loads(result.stdout)


class Audit(Fixture):
    plan: dict[str, Any]
    n: dict[str, Any]
    q: dict[str, Any]
    claim: dict[str, Any]
    run_record: dict[str, Any]

    def setUp(self):
        super().setUp()
        self.root = self.work / "project"
        self.r = self.root / "research"
        self.r.mkdir(parents=True)
        self.plan = {"question": "What was observed?", "criteria": [{"id": "A", "description": "Measure estimate"}]}
        self.n = {"kind": "number", "key": {"n": "8"}, "column": "estimate", "path": "research/results.csv",
                  "display": "0.250", "value": 0.25, "atol": 0.0005}
        self.q = {"kind": "quote", "path": "research/source.md", "quote": "sample mean"}
        self.claim = {"id": "C1", "criterion": "A", "statement": "At n=8 the sample mean is 0.250.",
                      "status": "supported", "evidence": [self.n, self.q]}
        self.claims = [self.claim]
        self.run_record = {"status": "completed", "command": "python3 measure.py", "outputs": ["research/results.csv"]}
        (self.r / "results.csv").write_text("n,estimate\n9,0.999\n8,0.2495\n", encoding="utf-8")
        (self.r / "source.md").write_text("The statistic is the sample mean.\n", encoding="utf-8")
        self.save()

    def save(self):
        raw = json.dumps(self.plan).encode()
        (self.r / "plan.json").write_bytes(raw)
        (self.r / "plan.sha256").write_bytes(hashlib.sha256(raw).hexdigest().encode() + b"\n")
        (self.r / "claims.json").write_text(json.dumps({"claims": self.claims}), encoding="utf-8")
        (self.r / "run.json").write_text(json.dumps(self.run_record), encoding="utf-8")
        (self.r / "paper.md").write_text("# Results\n" + "\n".join(f"{c['statement']} [{c['id']}]" for c in self.claims), encoding="utf-8")

    def audit(self, code):
        return self.cli("audit.py", self.root, code=code)

    def test_verified_sources_and_csv(self):
        result = self.audit(0)
        self.assertEqual((result["run"], result["claims"], result["deliverability"]),
                         ("complete", {"C1": "supported"}, "ready"))
        self.assertEqual(result["scientific_run"], "completed")

    def test_missing_required_files_and_modified_freeze(self):
        for name in ("plan.json", "plan.sha256", "run.json", "claims.json", "paper.md", "source.md", "results.csv"):
            with self.subTest(name=name):
                path = self.r / name
                raw = path.read_bytes()
                path.unlink()
                self.assertEqual(self.audit(2)["deliverability"], "blocked")
                path.write_bytes(raw)
        with (self.r / "plan.json").open("ab") as f:
            f.write(b"\n")
        self.assertIn("digest", self.audit(2)["errors"][0])

    def test_scientific_run_status_and_output_binding(self):
        for bad in ({"status": "blocked"}, {"status": "invented"},
                    dict(self.run_record, outputs=[]), dict(self.run_record, command=" "),
                    dict(self.run_record, outputs=["research/source.md"]),
                    dict(self.run_record, outputs=["research/results.csv"] * 2)):
            with self.subTest(bad=bad):
                (self.r / "run.json").write_text(json.dumps(bad))
                self.audit(2)
        self.claim["statement"] = "The source identifies the sample mean."
        self.claim["evidence"] = [self.q]
        for status, code in (("not-applicable", 0), ("failed", 1), ("blocked", 1)):
            with self.subTest(status=status):
                self.run_record = {"status": status, "reason": "No measurements available"}
                self.save()
                result = self.audit(code)
                self.assertEqual(result["scientific_run"], status)
                self.assertEqual(result["claims"]["C1"], "supported")

    def test_matched_conditions(self):
        self.plan["matched_conditions"] = ["threads", "dataset"]
        old = {"id": "old", "conditions": {"threads": 1, "dataset": "A"}}
        new = {"id": "new", "conditions": {"threads": 1, "dataset": "A"}}
        self.run_record["arms"] = [old, new]
        self.save()
        self.audit(0)
        for arms in ([old], [old, old], [old, dict(new, conditions={"threads": 1})],
                     [old, dict(new, conditions={"threads": 4, "dataset": "A"})]):
            with self.subTest(arms=arms):
                self.run_record["arms"] = arms
                self.save()
                self.audit(2)

    def test_declared_hashes(self):
        name = "research/results.csv"
        digest = hashlib.sha256((self.root / name).read_bytes()).hexdigest()
        self.run_record["sha256"] = {name: digest}
        self.save()
        self.audit(0)
        for hashes in ({}, {name: "0" * 64}, {name: digest, "extra": digest}):
            with self.subTest(hashes=hashes):
                self.run_record["sha256"] = hashes
                self.save()
                self.audit(2)

    def test_optional_run_plan_digest(self):
        digest = (self.r / "plan.sha256").read_text().strip()
        self.audit(0)  # legacy: omitted
        self.run_record["plan_sha256"] = digest
        self.save()
        self.audit(0)
        for bad in ("0" * 64, digest.upper(), digest + "\n", None, 123):
            with self.subTest(digest=bad):
                self.run_record["plan_sha256"] = bad
                self.save()
                self.assertIn("plan_sha256", self.audit(2)["errors"][0])

    def test_frozen_observations_cover_unprinted_rows(self):
        row = self.plan["criteria"][0]
        self.assertEqual(self.audit(0)["criterion_coverage"],
                         {"A": {"required_observations": 0, "verified_observations": 0}})
        row["required_observations"] = [dict(path=self.n["path"], key={"n": n}, column="estimate")
                                        for n in ("8", "9")]
        row["description"] = "Predict positive estimates for both samples"
        self.n.update(display="-0.250", value=-.25)
        self.claim["statement"] = "At n=8 the estimate was −0.250, contrary to our prediction."
        # The manuscript reports the supported negative observation. Even so,
        # the independent, unprinted second sample must exist in the frozen grid.
        csv = self.root / self.n["path"]
        for extra, code in (("9,-0.001\n", 0), ("", 2), ("9,1\n9,2\n", 2), ("9,NA\n", 2)):
            with self.subTest(extra=extra):
                csv.write_text("n,estimate\n8,-0.25\n" + extra)
                self.run_record["sha256"] = {self.n["path"]: hashlib.sha256(csv.read_bytes()).hexdigest()}
                self.save()
                report = self.audit(code)
                self.assertEqual(report["criterion_coverage"]["A"],
                                 {"required_observations": 2, "verified_observations": 1 + int(not code)})
                self.assertEqual(report["claims"]["C1"], "supported")
                if code:
                    for part in ("A", self.n["path"], "'9'", "estimate"):
                        self.assertIn(part, report["errors"][0])

    def test_frozen_observation_requires_declared_unique_cell(self):
        obs = {"path": self.n["path"], "key": {"n": "9"}, "column": "estimate"}
        self.plan["criteria"][0]["required_observations"] = [obs]
        for path in ("research/missing.csv", "research/unlisted.csv"):
            with self.subTest(path=path):
                obs["path"] = path
                if "missing" in path:
                    self.run_record["outputs"].append(path)
                else:
                    self.run_record["outputs"].pop()
                    (self.root / path).write_bytes((self.root / self.n["path"]).read_bytes())
                self.save()
                self.assertIn("required observation " + path, self.audit(2)["errors"][0])
        obs["path"] = self.n["path"]
        (self.root / obs["path"]).write_text("n,name,estimate\n8,first,.25\n9,second,.9\n")
        self.plan["criteria"][0]["required_observations"].append(dict(obs, key={"name": "second"}))
        self.save()
        self.assertIn("duplicate cell", self.audit(2)["errors"][0])

    def test_frozen_bounds_use_raw_cell_and_verify_declared_outcome(self):
        locator = {k: self.n[k] for k in ("path", "key", "column")}
        self.plan["criteria"][0]["required_observations"] = [dict(locator, bounds={"min": .25, "max": .2505})]
        for raw, outcome, declared, code in (("0.2499999999999999999999999999999999", "missed", "missed", 0),
                                             ("0.2499999999999999999999999999999999", "missed", "met", 2),
                                             ("0.250", "met", "met", 0), ("0.2505", "met", "met", 0)):
            with self.subTest(raw=raw, declared=declared):
                (self.root / self.n["path"]).write_text("n,estimate\n8," + raw + "\n")
                self.n["numeric_outcome"] = declared
                self.claim["statement"] = f"At n=8 the estimate rounded to 0.250 and {declared} the frozen interval."
                self.save()
                report = self.audit(code)
                self.assertEqual(report["observation_outcomes"], {"A": [dict(locator, outcome=outcome)]})
                if code:
                    self.assertIn("numeric_outcome", report["errors"][0])

    def test_numeric_outcome_requires_same_criterion_and_bounded_cell(self):
        cell = {k: self.n[k] for k in ("path", "key", "column")}
        self.plan["criteria"][0]["required_observations"] = [cell]
        self.plan["criteria"].append({"id": "B", "description": "Bounded",
                                      "required_observations": [dict(cell, bounds={"min": 0, "max": 1})]})
        self.claims.append(dict(self.claim, criterion="B", id="C2", statement="The resulting estimate is 0.250.",
                                evidence=[dict(self.n, numeric_outcome="met")]))
        for supplied in ("met", "missed", "not_evaluated", None):
            with self.subTest(supplied=supplied):
                self.n["numeric_outcome"] = supplied
                self.save()
                report = self.audit(2)
                self.assertEqual(report["claims"], {"C1": "invalid", "C2": "supported"})
                self.assertEqual(report["observation_outcomes"]["A"], [])
                self.assertIn("numeric_outcome", report["errors"][0])

    def test_frozen_bounds_schema_and_unobserved_cells(self):
        locator = {k: self.n[k] for k in ("path", "key", "column")}
        for bad in (None, {"min": 1}, {"min": 1, "max": 0}, {"min": 0, "max": True},
                    {"min": "0", "max": 1}, {"min": 0, "max": 1, "atol": 1}):
            self.plan["criteria"][0]["required_observations"] = [dict(locator, bounds=bad)]
            self.save()
            self.assertIn("bounds", self.audit(2)["errors"][0])
        self.plan["criteria"][0]["required_observations"] = [dict(locator, bounds={"min": 1, "max": 1})]
        self.claim.update(status="untested", statement="No estimate available.", evidence=[])
        (self.root / self.n["path"]).unlink()
        for status, code in (("completed", 2), ("failed", 1), ("blocked", 1)):
            if status != "completed":
                self.run_record = {"status": status, "reason": "Sensor unavailable"}
            self.save()
            self.assertEqual(self.audit(code)["observation_outcomes"], {"A": [dict(locator, outcome="not_evaluated")]})

    def test_observation_schema(self):
        obs = {"path": self.n["path"], "key": {"n": "9"}, "column": "estimate"}
        for bad in (None, [], {}, [obs, obs], [dict(obs, key={})], [dict(obs, key={"n": 9})],
                    [dict(obs, key={"": "9"})], [dict(obs, column="n")], [dict(obs, path="../results.csv")],
                    [dict(obs, column="")], [dict(obs, columns=["x"])], ["any row"], [{"key": {"n": "9"}}]):
            with self.subTest(bad=bad):
                self.plan["criteria"][0]["required_observations"] = bad
                self.save()
                self.assertIn("required_observations", self.audit(2)["errors"][0])

    def test_incomplete_observation_status(self):
        self.plan["criteria"][0]["required_observations"] = [
            {"path": self.n["path"], "key": {"n": "9"}, "column": "estimate"}]
        self.claim.update(statement="No conclusion yet.", evidence=[], status="untested")
        self.save()
        self.assertEqual(self.audit(1)["criterion_coverage"]["A"]["verified_observations"], 1)
        (self.root / self.n["path"]).unlink()
        for status in ("failed", "blocked", "not-applicable"):
            self.run_record = {"status": status, "reason": "Instrument offline"}
            self.save()
            self.assertEqual(self.audit(2 if status == "not-applicable" else 1)["criterion_coverage"]["A"],
                             {"required_observations": 1, "verified_observations": 0})

    def test_mathematical_minus_and_exponent_in_number(self):
        self.claim["statement"] = "At n=−8 the estimate is−2.50e−1."
        self.n.update(display="-2.50e-1", value=-.25, key={"n": "-8"})
        (self.r / "results.csv").write_text("n,estimate\n-8,-0.250\n")
        self.save()
        self.audit(0)
        self.n["display"] = "−2.50e−1"
        self.save()
        self.audit(0)
        self.n.update(display="2.50e-1", value=.25)
        (self.r / "results.csv").write_text("n,estimate\n-8,0.250\n")
        self.save()
        self.assertIn("display", self.audit(2)["errors"][0])

    def test_hyphenated_names_do_not_bind_or_require_numeric_evidence(self):
        self.claim["statement"] = "For case MESH-64: ResNet-50 on CIFAR-10 measured 0.250."
        self.save()
        self.audit(0)
        self.claim.update(statement="The score was -50.", evidence=[self.q])
        self.q.update(quote="-50", displays=["-50"])
        (self.r / "source.md").write_text("This model was ResNet-50.")
        self.save()
        self.assertIn("quote displays", self.audit(2)["errors"][0])

    def test_hyphen_label_exception_does_not_hide_negative_measurements(self):
        for text, display in (("For MESH-64: x=−2.", "-2"), ("For CIFAR-10: x=-2.", "-2"),
                              ("At ResNet-50 the effect was−2.", "-2"), ("误差为-2。", "-2"),
                              ("The effect was-2.0e−1.", "-2.0e-1")):
            with self.subTest(text=text):
                self.claim.update(statement=text, evidence=[self.q])
                self.save()
                self.assertIn("unbound", self.audit(2)["errors"][0])
                self.n.update(display=display, value=float(display))
                (self.r / "results.csv").write_text("n,estimate\n8," + display + "\n")
                self.claim["evidence"].append(self.n)
                self.save()
                self.audit(0)

    def test_mathematical_minus_in_literal_quote(self):
        self.claim.update(statement="The estimate is -2.50e-1.", evidence=[self.q])
        self.q.update(quote="Estimate: −2.50e−1", displays=["−2.50e−1"])
        (self.r / "source.md").write_text(self.q["quote"])
        self.save()
        self.audit(0)
        self.q["quote"] = "Estimate: -2.50e-1"
        self.save()
        self.assertIn("literal quote", self.audit(2)["errors"][0])
        self.q.update(quote="2.50e−1", displays=["2.50e-1"])
        self.claim["statement"] = "The estimate is 2.50e−1."
        self.save()
        self.assertIn("quote displays", self.audit(2)["errors"][0])

    def test_equal_measurements_require_independent_cells_not_keys(self):
        (self.r / "results.csv").write_text("n,name,estimate,other\n8,first,8,8\n")
        self.claim["statement"] = "At n=8 the estimate is 8 and the other measurement is 8."
        self.n.update(display="8", value=8, atol=0)
        self.save()
        self.assertIn("unbound", self.audit(2)["errors"][0])
        self.claim["evidence"].append(dict(self.n, key={"name": "first"}))
        self.save()
        self.assertIn("duplicate evidence", self.audit(2)["errors"][0])
        self.claim["evidence"][-1]["column"] = "other"
        self.save()
        self.audit(0)
        self.claim["statement"] = "At n=8 the estimate was measured."
        self.save()
        self.assertIn("non-key", self.audit(2)["errors"][0])

    def test_quoted_display_multiplicity(self):
        self.claim.update(statement="A measured 7 and B measured 7.", evidence=[self.q])
        self.q.update(quote="A: 7", displays=["7"])
        (self.r / "source.md").write_text("A: 7 and B: 7")
        self.save()
        self.assertIn("unbound", self.audit(2)["errors"][0])
        self.claim["evidence"].append(dict(self.q, quote="A: 7 and"))
        self.save()
        self.assertIn("unbound", self.audit(2)["errors"][0])
        self.claim["evidence"][-1]["quote"] = "B: 7"
        self.save()
        self.audit(0)
        self.claim["evidence"] = [dict(self.q, quote="A: 7 and B: 7")]
        self.save()
        self.audit(0)

    def test_transcription_enforces_both_exact_inclusive_limits(self):
        for display, value, atol, csv, code in (
                ("0.250", .25, 1, "0.2505", 0),
                ("0.250", .25, 1, "0.250500000000000000000000000001", 2),
                ("0.250", .25, 1, "-0.25", 2),
                ("0.250", .25, 0, "0.25001", 2),
                ("0.250", .25, -.1, "0.25", 2),
                ("+2.50e-3", .0025, 1, ".002495", 0),
                ("+2.50e-3", .0025, 1, ".002494999999999999999999999999", 2),
                ("8", 8, 1, "8.5", 0), ("8", 8, 1, "8.5001", 2)):
            with self.subTest(display=display, csv=csv, atol=atol):
                self.claim["statement"] = f"The estimate is {display}."
                self.n.update(display=display, value=value, atol=atol)
                (self.r / "results.csv").write_text("n,estimate\n8," + csv + "\n")
                self.save()
                self.audit(code)

    def test_archived_scientific_displays(self):
        for study in ("opencode-study", "quadrature", "source-audit"):
            with self.subTest(study=study):
                self.cli("audit.py", ROOT / "examples" / study, code=0)

    def test_chinese_numeric_statement(self):
        self.claim["statement"] = "当n=8时误差为0.250。"
        self.save()
        self.audit(0)
        self.claim["statement"] += "另一误差为0.74。"
        self.save()
        self.assertIn("unbound", self.audit(2)["errors"][0])

    def test_literature_quoted_numbers(self):
        self.run_record = {"status": "not-applicable", "reason": "文献综述"}
        self.claim["statement"] = "文献报告精度为85.2%。"
        self.q.update(quote="精度为85.2%", displays=["85.2"])
        self.claim["evidence"] = [self.q]
        (self.r / "source.md").write_text("精度为85.2%，参见表格。", encoding="utf-8")
        self.save()
        self.audit(0)
        self.claim["statement"] = "文献报告精度为95.2%。"
        self.q["displays"] = ["95.2"]
        self.save()
        self.assertIn("quote displays", self.audit(2)["errors"][0])

    def test_explicit_gaps_and_statuses(self):
        for status in ("partial", "unsupported", "untested", "contradicted"):
            with self.subTest(status=status):
                self.claim["status"] = status
                self.claim["evidence"] = ([self.n] if status in {"partial", "contradicted"} else []) + [
                    {"kind": "blocked", "reason": "Instrument offline"}]
                self.save()
                r = self.audit(1)
                self.assertEqual((r["run"], r["claims"]["C1"], r["deliverability"]), ("complete", status, "incomplete"))
                self.assertIn("Instrument offline", " ".join(r["incomplete"]))
        self.claim["status"] = "supported"
        self.claim["evidence"] = [self.n, {"kind": "incomplete", "reason": "replicate pending"}]
        self.save()
        self.audit(2)

    def test_no_vacuous_pass(self):
        self.claim["evidence"] = []
        self.save()
        self.audit(2)
        self.plan["criteria"].append({"id": "B", "description": "Second outcome"})
        self.claim["evidence"] = [self.n]
        self.save()
        self.assertIn("uncovered", self.audit(2)["errors"][0])

    def test_wrong_report_with_valid_unrelated_evidence(self):
        self.claim["statement"] = "At n=8 the estimate is 0.950, above reference 0.250."
        self.save()
        self.assertIn("unbound", self.audit(2)["errors"][0])
        self.n["display"] = "0.950"
        self.save()
        self.assertIn("display", self.audit(2)["errors"][0])

    def test_quote_mismatch_and_marker_alignment(self):
        self.q["quote"] = "sample median"
        self.save()
        self.assertIn("quote", self.audit(2)["errors"][0])
        self.q["quote"] = "sample mean"
        self.save()
        path = self.r / "paper.md"
        raw = path.read_text()
        for paper in (raw.replace("0.250", "0.251"), raw + "\n[C1]", raw + "\n[C99]", raw.replace(" [C1]", "")):
            with self.subTest(paper=paper):
                path.write_text(paper)
                self.audit(2)

    def test_quote_cannot_cite_own_report_files(self):
        for name, quote in (("paper.md", "sample mean"), ("claims.json", "sample mean"), ("run.json", "completed"),
                            ("plan.json", "question"), ("plan.sha256", (self.r / "plan.sha256").read_text().strip())):
            alias = self.r / (name + ".alias")
            alias.symlink_to(name)
            hardlink = self.r / (name + ".hardlink")
            os.link(self.r / name, hardlink)
            for target in (name, alias.name, hardlink.name):
                with self.subTest(target=target):
                    self.q.update(path="research/" + target, quote=quote)
                    self.save()
                    self.assertIn("evidence cannot cite", self.audit(2)["errors"][0])

    def test_control_file_cannot_be_an_output(self):
        os.link(self.r / "plan.json", self.r / "pretend.csv")
        self.run_record["outputs"].append("research/pretend.csv")
        self.save()
        self.assertIn("run output cannot", self.audit(2)["errors"][0])

    def test_duplicates(self):
        self.claims.append(dict(self.claim))
        self.save()
        self.assertIn("duplicate claim", " ".join(self.audit(2)["errors"]))
        self.claims.pop()
        self.claim["evidence"].append(dict(self.n))
        self.save()
        self.assertIn("duplicate evidence", self.audit(2)["errors"][0])
        (self.r / "claims.json").write_text('{"claims":[],"claims":[]}')
        self.assertIn("duplicate JSON", self.audit(2)["errors"][0])

    def test_key_precision_and_nonfinite(self):
        for data in ("8,0.251", "8,0.25\n8,0.25", "7,0.25", "8,NaN", "8,Infinity"):
            with self.subTest(data=data):
                (self.r / "results.csv").write_text("n,estimate\n" + data)
                self.audit(2)
        self.n["atol"] = float("nan")
        self.save()
        self.assertIn("non-finite", self.audit(2)["errors"][0])

    def test_no_absolute_traversal_or_external_symlink(self):
        target = self.work / "outside.md"
        target.write_text("sample mean")
        (self.r / "link.md").symlink_to(target)
        for path in (str(target), "research/../../outside.md", "research/link.md", r"C:\\outside.md"):
            with self.subTest(path=path):
                self.q["path"] = path
                self.save()
                self.audit(2)


class Compare(Fixture):
    def setUp(self):
        super().setUp()
        self.a = self.work / "expected.csv"
        self.b = self.work / "actual.csv"
        self.a.write_text("id,x,cl\na,10,A\nb,20,A\nc,30,B\nd,40,B\n")
        self.b.write_text("cl,x,id\ny,40.4,d\ny,30,c\nz,20,b\nz,10,a\n")

    def compare(self, code, *args):
        return self.cli("compare.py", self.a, self.b, "--id", "id", *args, code=code)

    def test_reorder_tolerance_and_permuted_labels(self):
        self.assertEqual(self.compare(0, "--column", "x", "--rtol", "0.01", "--labels", "cl")["ari"], 1)
        self.compare(0, "--column", "x", "--atol", "0.4")
        self.compare(1, "--column", "x", "--atol", "0.39")

    def test_reference_cannot_be_actual_file(self):
        alias = self.work / "actual-alias.csv"
        os.link(self.a, alias)
        for actual in (self.a, alias):
            with self.subTest(actual=actual):
                self.b = actual
                self.assertIn("distinct files", self.compare(2, "--column", "x")["diagnostics"][0])

    def test_wrong_partition(self):
        self.b.write_text("id,cl\na,X\nb,Y\nc,X\nd,Y\n")
        self.assertEqual(self.compare(1, "--labels", "cl")["ari"], -0.5)

    def test_missing_duplicate_and_nonfinite(self):
        self.b.write_text("id,x\na,10\nq,1\n")
        result = self.compare(1, "--column", "x")
        self.assertIn("missing ID: b", result["diagnostics"])
        self.assertIn("extra ID: q", result["diagnostics"])
        for bad in ("id,x\na,10\na,11\n", "id,x,x\na,1,2\n", "id,x\n", "id,x\n,123\n", "id,x\na,NaN\nb,20\nc,30\nd,40\n"):
            with self.subTest(bad=bad):
                self.b.write_text(bad)
                self.compare(2, "--column", "x")

    def test_bounded_output(self):
        self.b.write_text("id,x\n" + "".join(f"extra{i},1\n" for i in range(40)))
        result = self.compare(1, "--column", "x")
        self.assertEqual((len(result["diagnostics"]), result["diagnostic_count"]), (20, 44))
