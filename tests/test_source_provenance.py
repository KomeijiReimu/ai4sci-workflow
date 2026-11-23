"""Check a source-only study without depending on a live search service."""

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SourceProvenance(unittest.TestCase):
    def setUp(self):
        tmp = ROOT / '.local/tmp'
        tmp.mkdir(parents=True, exist_ok=True)
        project = tempfile.TemporaryDirectory(dir=tmp)
        self.addCleanup(project.cleanup)
        self.project = Path(project.name)
        self.r = self.project / 'research'
        shutil.copytree(ROOT / 'examples/source-audit/research', self.r)
        self.entries = []
        for name, title in [('trapezoid-note.md', 'Trapezoid derivation'), ('left-note.md', 'Left-sum derivation')]:
            self.entries.append(dict(id=name, title=title, origin='Supplied teaching notes',
                                     locator='Derivation', access='provided', path='research/'+name,
                                     sha256=hashlib.sha256((self.r/name).read_bytes()).hexdigest()))
        self.catalog()

    def catalog(self):
        (self.r/'sources.json').write_text(json.dumps({'sources': self.entries}), encoding='utf-8')

    def cli(self, command, expected):
        result = subprocess.run([sys.executable, ROOT/'ai4sci.py', command, self.project], capture_output=True, text=True)
        self.assertEqual(result.returncode, expected, result.stdout+result.stderr)
        return result

    def test_legacy_optional_and_required_receipts(self):
        self.assertEqual(json.loads(self.cli('audit', 0).stdout)['source_records'], 2)
        (self.r/'sources.json').unlink()
        self.assertIsNone(json.loads(self.cli('audit', 0).stdout)['source_records'])
        plan = self.r/'plan.json'
        plan.write_text(json.dumps({**json.loads(plan.read_text()), 'require_source_manifest':True}))
        (self.r/'plan.sha256').unlink()
        self.cli('freeze', 0)
        self.assertIn('required', self.cli('audit', 2).stdout)
        self.catalog()
        self.cli('audit', 0)

    def test_changed_snapshot_and_unregistered_quote(self):
        note = self.r/'left-note.md'
        raw = note.read_bytes()
        note.write_bytes(raw+b'\n')  # The quoted sentence itself is unchanged.
        self.assertIn('digest', self.cli('audit', 2).stdout)
        note.write_bytes(raw)
        self.entries.pop()
        self.catalog()
        self.assertEqual(json.loads(self.cli('audit', 2).stdout)['claims']['C2'], 'invalid')

    def test_duplicate_snapshot_and_missing_public_identity(self):
        self.entries.append({**self.entries[0], 'id':'other-title'})
        self.catalog()
        self.assertIn('duplicate', self.cli('audit', 2).stdout)
        self.entries.pop()
        self.entries[0]['access'] = 'abstract'
        self.catalog()
        self.assertIn('URL', self.cli('audit', 2).stdout)

    def test_freeze_rejects_an_invalid_plan_before_leaving_a_digest(self):
        record = self.r/'plan.sha256'
        record.unlink()
        for raw in (b'{"question":"Q","criteria":[42]}', b'{"question":"Q","question":"other","criteria":[1]}'):
            (self.r/'plan.json').write_bytes(raw)
            self.cli('freeze', 1)
            self.assertFalse(record.exists())
