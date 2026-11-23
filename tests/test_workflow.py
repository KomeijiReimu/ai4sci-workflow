import hashlib
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
            for requirement in ('method,n,signed_error', 'order', 'plot_command', 'polyline', 'research/review.md'):
                self.assertIn(requirement, command[-1])
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

    def test_live_launcher_checks_archived_paper_not_just_ready_audit(self):
        launcher = ROOT / 'scripts/live_study.py'
        real_run = subprocess.run
        for case, diagnostic in [('archive', None), ('unembedded', 'Markdown-embedded SVG'),
                                 ('wrong-order', 'doubling rate'), ('malformed-order', 'not-a-rate')]:
            attempt = self.project / case
            study = attempt / 'study'

            def launch(command, **kwargs):
                if command[0] != 'opencode':
                    return real_run(command, **kwargs)
                shutil.copytree(ROOT / 'examples/opencode-study/research', study / 'research')
                if case == 'unembedded':
                    paper = study / 'research/paper.md'
                    paper.write_text(paper.read_text().replace('![', '['))
                if case in ('wrong-order', 'malformed-order'):
                    research = study / 'research'
                    csv_path = research / 'results.csv'
                    if case == 'wrong-order':
                        # Same wrong rate in paper, ledger and raw table: general audit passes.
                        csv_path.write_text(csv_path.read_text().replace('1.9999999999921272', '4'))
                        paper = research / 'paper.md'
                        paper.write_text(paper.read_text().replace('2.00000', '4.00000'))
                        ledger = research / 'claims.json'
                        ledger.write_text(ledger.read_text().replace('2.00000', '4.00000').replace('"value": 2.0,', '"value": 4.0,'))
                    else:
                        csv_path.write_text(csv_path.read_text().replace('0.9689731043793759', 'not-a-rate'))
                    manifest = research / 'run.json'
                    run_record = json.loads(manifest.read_text())
                    run_record['sha256']['research/results.csv'] = hashlib.sha256(csv_path.read_bytes()).hexdigest()
                    manifest.write_text(json.dumps(run_record))
                return subprocess.CompletedProcess(command, 0)

            with self.subTest(case=case), patch.object(sys, 'argv', [str(launcher), str(attempt)]), \
                    patch('shutil.which', return_value='opencode'), patch('subprocess.run', side_effect=launch) as run:
                if diagnostic is None:
                    runpy.run_path(str(launcher), run_name='__main__')
                else:
                    with self.assertRaisesRegex(SystemExit, f'Benchmark failed: .*{diagnostic}'):
                        runpy.run_path(str(launcher), run_name='__main__')
                self.assertEqual(run.call_count, 2)  # One model invocation and one checkout audit.
                self.assertEqual(json.loads((attempt / 'audit.json').read_text())['deliverability'], 'ready')
                quality = json.loads((attempt / 'quality.json').read_text())
                self.assertEqual(quality['result'], 'pass' if diagnostic is None else 'fail')
                if diagnostic is None:
                    self.assertEqual(quality['checked_mesh_errors'], 12)
                    self.assertEqual(quality['checked_doubling_rates'], 10)
                    self.assertEqual(quality['rate_columns'], {'order': {'cells': 10, 'marked_bindings': 2}})
                    self.assertEqual(quality['review']['status'], 'present, not assessed')
                else:
                    self.assertIn(diagnostic, quality['reason'])

    def test_live_launcher_checks_measured_plot_data_commands_and_review(self):
        check = runpy.run_path(str(ROOT / 'scripts/live_study.py'))['check_study']
        research = self.project / 'research'
        shutil.copytree(ROOT / 'examples/opencode-study/research', research)
        svg = research / 'error.svg'
        source = svg.read_text()
        svg.unlink()
        with self.assertRaisesRegex(ValueError, 'project-local file'):
            check(self.project)
        svg.write_text(source)
        for name, old, new, reason in [
                ('run.json', ',\n    "research/error.svg"\n', '\n', 'declared in run outputs'),
                ('run.json', 'python3 research/plot_errors.py', 'python3 missing.py', 'project-local file'),
                ('error.svg', source, '<svg xmlns="http://www.w3.org/2000/svg"><circle r="5"/></svg>', 'polyline'),
                ('error.svg', '599.55,252.74', '599.55,300.00', 'Plotted point'),
                ('results.csv', '0.002604166666666685', '0.004321', 'inaccurate mesh error'),
                ('claims.json', '"column": "signed_error"', '"column": "order"', 'marked final-grid'),
                ('claims.json', '"value": 2.0,', '"value": 4.0,', 'marked doubling rate'),
                ('review.md', (research / 'review.md').read_text(), ' \n', 'Empty review artifact')]:
            with self.subTest(name=name, reason=reason):
                path = research / name
                original = path.read_text()
                self.assertIn(old, original)
                path.write_text(original.replace(old, new))
                with self.assertRaisesRegex(ValueError, reason):
                    check(self.project)
                path.write_text(original)

    def test_live_launcher_review_language_and_optional_rates(self):
        check = runpy.run_path(str(ROOT / 'scripts/live_study.py'))['check_study']
        research = self.project / 'research'
        shutil.copytree(ROOT / 'examples/opencode-study/research', research)
        review = research / 'review.md'
        paraphrase = review.read_text().replace('判定：可以交付', '审阅意见：建议交稿').replace('未参与实验和写稿', '未加入作者团队')
        for text in (paraphrase, '作者自查：对判据的解释仍有分歧，还不能交稿。'):
            review.write_text(text)
            self.assertEqual(check(self.project)['review'], {'path': 'research/review.md', 'status': 'present, not assessed'})
        # Older / alternative rate columns are outside this fixed benchmark's checks.
        for name, old, new in [('results.csv', ',order\n', ',estimated_rate\n'),
                               ('claims.json', '"column": "order"', '"column": "estimated_rate"')]:
            path = research / name
            path.write_text(path.read_text().replace(old, new))
        self.assertEqual(check(self.project)['checked_doubling_rates'], 0)

    def test_live_launcher_checks_both_rate_columns_and_bindings(self):
        check = runpy.run_path(str(ROOT / 'scripts/live_study.py'))['check_study']
        research = self.project / 'research'
        shutil.copytree(ROOT / 'examples/opencode-study/research', research)
        table = research / 'results.csv'
        header, *rows = table.read_text().splitlines()
        both = [header + ',observed_order', *(r + ',' + r.rsplit(',', 1)[1] for r in rows)]
        table.write_text('\n'.join(both) + '\n')
        claims = research / 'claims.json'
        claims.write_text(claims.read_text().replace('"column": "order"', '"column": "observed_order"', 1))
        quality = check(self.project)
        self.assertEqual(quality['checked_doubling_rates'], 20)
        self.assertEqual(quality['rate_columns'], {c: {'cells': 10, 'marked_bindings': 1} for c in ('order', 'observed_order')})
        table.write_text('\n'.join([*both[:-1], both[-1].rsplit(',', 1)[0] + ',4']) + '\n')
        with self.assertRaisesRegex(ValueError, 'reported doubling rate: observed_order'):
            check(self.project)
        table.write_text('\n'.join(both) + '\n')
        claims.write_text(claims.read_text().replace('"value": 2.0,', '"value": 4.0,'))
        with self.assertRaisesRegex(ValueError, 'marked doubling rate .*observed_order'):
            check(self.project)

    def test_live_launcher_stops_after_model_exit_or_timeout(self):
        launcher = ROOT / 'scripts/live_study.py'
        for failure, message in [(subprocess.CompletedProcess([], 17), 'OpenCode exited 17'),
                                 (subprocess.TimeoutExpired('opencode', 1), 'Time limit reached')]:
            attempt = self.project / message
            with self.subTest(message=message), patch.object(sys, 'argv', [str(launcher), str(attempt)]), \
                    patch('shutil.which', return_value='opencode'), patch('subprocess.run', side_effect=[failure]) as run:
                with self.assertRaisesRegex(SystemExit, message):
                    runpy.run_path(str(launcher), run_name='__main__')
                run.assert_called_once()
                self.assertTrue((attempt / 'events.jsonl').is_file())
                self.assertTrue((attempt / 'request.txt').is_file())
                self.assertFalse((attempt / 'audit.json').exists())

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

    def test_stats_uses_canonical_study_plan(self):
        research = self.project / 'research'
        research.mkdir()
        plan = research / 'plan.json'
        plan.write_text(json.dumps({'question':'Does rainfall predict the outcome?',
                                    'criteria':[{'id':'K1','description':'Use rainfall as the sole predictor.'}]}))
        code = self.project / 'fit.R'
        code.write_text('fit <- lm(outcome ~ rainfall + humidity, data = records)\n')
        result = self.cmd('stats', code, plan)
        self.assertEqual(result.returncode, 0, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['coverage']['plan_adherence'], 'scanned')
        self.assertTrue(any('humidity' in f['evidence'] for f in report['findings']))
        plan.write_text('{}')
        self.assertNotEqual(self.cmd('stats', code, plan).returncode, 0)
