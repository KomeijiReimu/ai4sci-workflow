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
