import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Installation(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / '.local' / 'tmp'
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)

    def cmd(self, *arguments, script=None):
        return subprocess.run([sys.executable, script or ROOT / 'ai4sci.py', *arguments], text=True, capture_output=True)

    def test_install_preserves_existing_config_and_is_idempotent(self):
        config = self.project / 'opencode.jsonc'
        config.write_text('{/* keep */}')
        self.assertEqual(self.cmd('init', self.project).returncode, 0)
        self.assertEqual(config.read_text(), '{/* keep */}')
        skill = self.project / '.opencode/skills/ai4sci/SKILL.md'
        self.assertTrue(skill.is_file())
        manifest = json.loads((self.project / '.ai4sci-kit/manifest.json').read_text())
        for rel, digest in manifest['sha256'].items():
            self.assertEqual(hashlib.sha256((self.project / rel).read_bytes()).hexdigest(), digest)
        self.assertIn('0 files installed', self.cmd('init', self.project).stdout)

    def test_conflict_is_detected_before_copying(self):
        conflict = self.project / '.opencode/skills/ai4sci-review/SKILL.md'
        conflict.parent.mkdir(parents=True)
        conflict.write_text('my local version')
        self.assertNotEqual(self.cmd('init', self.project).returncode, 0)
        self.assertFalse((self.project / '.ai4sci-kit').exists())
        self.assertEqual(conflict.read_text(), 'my local version')

    def test_freeze_refuses_changed_plan(self):
        research = self.project / 'research'
        research.mkdir()
        plan = research / 'plan.json'
        plan.write_bytes((ROOT / 'examples/quadrature/research/plan.json').read_bytes())
        self.assertEqual(self.cmd('freeze', self.project).returncode, 0)
        record = (research / 'plan.sha256').read_bytes()
        plan.write_text(plan.read_text() + '\n')
        self.assertNotEqual(self.cmd('freeze', self.project).returncode, 0)
        self.assertEqual((research / 'plan.sha256').read_bytes(), record)

    def test_stats_requires_real_inputs(self):
        self.assertNotEqual(self.cmd('stats', self.project / 'absent').returncode, 0)
        report = self.project / 'paper.md'
        report.write_text('We ran a regression (p < 0.01). Income causes higher happiness.')
        result = self.cmd('stats', report)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertTrue(output['coverage']['plan_adherence'].startswith('not checked'))
        self.assertTrue(output['findings'])
