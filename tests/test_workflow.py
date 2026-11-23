import json
import os
from pathlib import Path
import runpy
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


class Workflow(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / '.local' / 'tmp'
        scratch.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name)

    def cmd(self, *arguments, cwd=ROOT):
        return subprocess.run([sys.executable, ROOT / 'ai4sci.py', *arguments], cwd=cwd, text=True, capture_output=True)

    def test_init_is_not_a_command(self):
        self.assertEqual(self.cmd('init', self.project).returncode, 2)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_checkout_cli_checks_two_studies_without_setup(self):
        # Keep the external case outside the repo (and off memory-backed /tmp).
        external = tempfile.TemporaryDirectory(prefix='ai4sci study ', dir=Path.home())
        self.addCleanup(external.cleanup)
        outside = Path(external.name).resolve()
        self.assertFalse(outside.is_relative_to(ROOT))
        for study in (self.project, outside):
            with self.subTest(study=study):
                research = study / 'research'
                shutil.copytree(ROOT / 'examples/quadrature/research', research, ignore=shutil.ignore_patterns('plan.sha256'))
                before = set(study.rglob('*'))
                result = self.cmd('freeze', study)
                self.assertEqual(result.returncode, 0, result.stderr)
                for cwd, args in ((ROOT, [study]), (study, [])):
                    result = self.cmd('audit', *args, cwd=cwd)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    self.assertEqual(json.loads(result.stdout)['deliverability'], 'ready')
                for name in ('paper.md', 'claims.json'):
                    path = research / name
                    path.write_text(path.read_text().replace('0.3359375', '0.7359375'))
                result = self.cmd('audit', '.', cwd=study)
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
                self.assertEqual(json.loads(result.stdout)['claims']['C1'], 'invalid')
                self.assertEqual(set(study.rglob('*')), before | {research / 'plan.sha256'})

    def test_live_launcher_retains_evidence_and_audits_empty_model_output(self):
        launcher = ROOT / 'scripts/live_study.py'
        attempt = self.project / 'new attempt'
        study = attempt / 'study'
        real_run = subprocess.run

        def launch(command, **kwargs):
            if command[0] == sys.executable:
                self.assertEqual(command[1:], [ROOT / 'ai4sci.py', 'audit', study])
                self.assertNotIn('env', kwargs)
                return real_run(command, **kwargs)
            self.assertEqual(command[:-1], ['opencode', 'run', '--archived', '--format', 'json', '--model', 'mock/model'])
            self.assertEqual(kwargs['cwd'], ROOT)
            self.assertEqual(kwargs['env']['PWD'], str(ROOT))
            self.assertEqual((attempt / 'request.txt').read_text().rstrip(), command[-1])
            for path in (ROOT / 'skills/ai4sci/SKILL.md', ROOT / 'checks/contract.md', study):
                self.assertIn(str(path), command[-1])
            return subprocess.CompletedProcess(command, 0)  # A zero model exit is not a completed study.

        with patch.object(sys, 'argv', [str(launcher), str(attempt), '--model', 'mock/model']), \
                patch.dict(os.environ, PWD=str(self.project)), \
                patch('shutil.which', return_value='opencode') as which, \
                patch('subprocess.run', side_effect=launch) as run:
            with self.assertRaisesRegex(SystemExit, 'Independent audit failed'):
                runpy.run_path(str(launcher), run_name='__main__')
        which.assert_called_once_with('opencode')
        self.assertEqual(run.call_count, 2)
        self.assertEqual({p.name for p in attempt.iterdir()}, {'study', 'request.txt', 'events.jsonl', 'stderr.txt', 'audit.json'})
        self.assertEqual({p.relative_to(study).as_posix() for p in study.rglob('*')},
                         {'inputs', 'inputs/trapezoid-note.md', 'inputs/left-note.md'})
        self.assertEqual(json.loads((attempt / 'audit.json').read_text())['deliverability'], 'blocked')

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
