"""Offline tests adapted from ARIS tests/test_codex_image2_server.py (MIT).

Upstream revision, original paths and license: integrations/codex-image/guide.md.
"""

import base64
from contextlib import ExitStack
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / 'integrations' / 'codex-image'
sys.path.insert(0, str(DIR))
spec = importlib.util.spec_from_file_location('codex_image2_server', DIR / 'server.py')
assert spec and spec.loader
MODULE = importlib.util.module_from_spec(spec)
spec.loader.exec_module(MODULE)
sys.path.pop(0)

PNG = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII='


class CodexImageTests(unittest.TestCase):
    def setUp(self):
        tmp = ROOT / '.local' / 'codex-image' / 'test-tmp'
        tmp.mkdir(parents=True, exist_ok=True)
        contexts = ExitStack()
        self.addCleanup(contexts.close)
        self.project = Path(contexts.enter_context(tempfile.TemporaryDirectory(dir=tmp)))
        self.state = self.project / '.local' / 'codex-image'
        self.out = self.state / 'images' / 'out.png'
        for name, value in [('PROJECT_DIR', self.project), ('STATE_DIR', self.state), ('JOBS_DIR', self.state / 'jobs')]:
            contexts.enter_context(mock.patch.object(MODULE, name, value))

    def test_stdio_discovery(self):
        messages = [{'jsonrpc': '2.0', 'id': i, 'method': m} for i, m in enumerate(['initialize', 'tools/list'], 1)]
        result = subprocess.run([sys.executable, str(DIR / 'server.py')], cwd=self.project, input=''.join(json.dumps(m)+'\n' for m in messages), capture_output=True, text=True, check=True, timeout=10)
        init, tools = map(json.loads, result.stdout.splitlines())
        self.assertIn('tools', init['result']['capabilities'])
        self.assertEqual([t['name'] for t in tools['result']['tools']], ['generate_start', 'generate_status'])

    def test_bridge_prompt_includes_references(self):
        prompt = MODULE.build_bridge_prompt('Blue circle.', system='No labels.', reference_image_paths=['ref.png'])
        for value in ('No labels.', 'ref.png', 'Blue circle.', 'native image generation'):
            self.assertIn(value, prompt)

    def test_native_artifact_from_saved_path(self):
        path = self.project / 'source.png'
        path.write_bytes(base64.b64decode(PNG))
        out, source, _, err = MODULE.materialize_generated_image({'savedPath': str(path)}, self.out)
        self.assertIsNone(err)
        self.assertEqual((out, source, self.out.read_bytes()), (self.out, str(path), path.read_bytes()))

    def test_rejects_signature_only_png(self):
        item = {'result': base64.b64encode(MODULE.PNG_SIGNATURE+b'fake-png-payload').decode()}
        self.assertIn('PNG', MODULE.materialize_generated_image(item, self.out)[3])
        self.assertFalse(self.out.exists())

    def test_paths_reject_escape(self):
        self.assertIn('outputPath must stay under', MODULE.start_async_generate('Test', output_path='../escape.png')[1])
        self.assertIn('Invalid jobId', MODULE.get_generate_status('../outside')[1])

    def test_missing_codex(self):
        with mock.patch.object(MODULE, 'find_codex_bin', return_value=None):
            payload, err = MODULE.run_codex_image('Test', cwd=self.project, output_path=self.out)
        self.assertIsNone(payload)
        self.assertIn('Codex CLI not found', err)

    def test_job_persists_timeout_and_expiry(self):
        with mock.patch.object(MODULE.subprocess, 'Popen', return_value=mock.Mock(pid=4321)):
            payload, err = MODULE.start_async_generate('Test', timeout_seconds=45)
        self.assertIsNone(err)
        job_file = MODULE.job_state_path(payload['jobId'])
        job = json.loads(job_file.read_text())
        self.assertEqual(job['request']['timeoutSec'], 45)
        self.assertIsNotNone(job['expiresAt'])
        job['expiresAt'] = '2000-01-01T00:00:00Z'
        MODULE.write_json(job_file, job)
        status, err = MODULE.get_generate_status(payload['jobId'])
        self.assertEqual(status['status'], 'failed')
        self.assertIn('deadline', status['error'])
        self.assertNotIn('prompt', json.loads(job_file.read_text())['request'])

    def make_app_server_fixture(self):
        # This child is an explicit protocol fixture, not Codex or a smoke image.
        fake = self.project / 'fixture'
        fake.write_text(f'''#!{sys.executable}
import json, os, sys, time
def recv(): return json.loads(input())
def emit(**msg): print(json.dumps(msg), flush=True)
def reply(i, result): emit(id=i, result=result)
def notify(m, **p): emit(method=m, params=dict(threadId='t', **p))
assert recv()['method'] == 'initialize'; reply(1, {{}})
assert recv()['method'] == 'initialized'
opts = recv()['params']; assert opts['sandbox'] == 'read-only' and opts['approvalPolicy'] == 'never'
reply(2, {{'thread': {{'id': 't'}}}})
assert recv()['method'] == 'turn/start'; reply(3, {{'turn': {{'id': 'u'}}}})
kind = os.environ['FIXTURE_ITEM']
if kind == 'eof': sys.exit(0)
if kind == 'timeout': time.sleep(5); sys.exit(0)
auth = {{'message':'Reconnecting', 'additionalDetails':'workspace routing discovery unauthorized (401) PRIVATE_RPC'}}
print('PRIVATE_STDERR', file=sys.stderr, flush=True)
notify('error', turnId='other', willRetry=False, error=auth)
if kind == '401': notify('error', turnId='u', willRetry=False, error=auth); sys.exit(0)
if kind.startswith('retry-'):
    notify('error', turnId='u', willRetry=True, error=auth)
    if kind == 'retry-lost': sys.exit(0)
    if kind == 'retry-failed': notify('turn/completed', turn={{'id':'u','status':'failed','error':auth}}); sys.exit(0)
    kind = 'imageGeneration'
notify('item/completed', turnId='u', item={{'type':kind, 'status':'completed', 'result':'{PNG}', 'id':'ig', 'text':'No image.'}})
notify('turn/completed', turn={{'id':'u', 'status':'completed'}})
sys.stdin.readline()
''')
        fake.chmod(0o700)
        return fake

    def test_native_stdio_protocol_offline(self):
        fake = self.make_app_server_fixture()
        with mock.patch.object(MODULE, 'find_codex_bin', return_value=str(fake)):
            for kind, expected in [('agentMessage', 'No completed native'), ('retry-success', None)]:
                with self.subTest(kind=kind), mock.patch.dict(os.environ, FIXTURE_ITEM=kind):
                    payload, err = MODULE.run_codex_image('Test', cwd=self.project, output_path=self.out, timeout_sec=5)
                    if expected:
                        self.assertIsNone(payload)
                        self.assertIn(expected, err)
                        self.assertFalse(self.out.exists())
                    else:
                        self.assertIsNone(err)
                        self.assertTrue(payload['nativeToolConfirmed'])
                        self.assertEqual(payload['eventId'], 'ig')
                        self.assertEqual(self.out.read_bytes(), base64.b64decode(PNG))

    def test_uncertain_vs_rejected_turns_through_cli(self):
        fake = self.make_app_server_fixture()
        for kind, expected in [('eof', 'unknown'), ('timeout', 'unknown'), ('commandExecution', 'unknown'), ('401', 'failed'), ('retry-lost', 'unknown'), ('retry-failed', 'failed')]:
            with self.subTest(kind=kind):
                env = dict(os.environ, CODEX_IMAGE2_PROJECT_DIR=str(self.project), CODEX_IMAGE2_CODEX_BIN=str(fake), FIXTURE_ITEM=kind)
                cmd = [sys.executable, str(DIR / 'cli.py')]
                queued = subprocess.run(cmd+['generate', '--timeout', '1', 'Test request'], env=env, capture_output=True, check=True, timeout=5)
                job_id = json.loads(queued.stdout)['jobId']
                check = subprocess.run(cmd+['status', job_id, '--wait', '5'], env=env, capture_output=True, timeout=8)
                self.assertEqual(check.returncode, 1)
                report = json.loads(check.stdout)
                self.assertEqual((report['status'], report['done'], report['threadId'], report['turnId']), (expected, True, 't', 'u'))
                job = MODULE.read_json(MODULE.job_state_path(job_id))
                self.assertNotIn('PRIVATE_', json.dumps(report) + json.dumps(job))
                self.assertEqual(job['attempt']['phase'], 'accepted')
                if expected == 'unknown':
                    self.assertEqual(job['request']['prompt'], 'Test request')
                    self.assertIn('Do not resubmit', report['resumeHint'])
                else:
                    self.assertNotIn('prompt', job['request'])
                    self.assertIn('authentication rejected (401)', report['error'])
                self.assertEqual(MODULE.run_async_job(job_id), 1)  # No replay.
                self.assertEqual(MODULE.get_generate_status(job_id)[0], report)

    def test_dead_or_expired_worker_after_possible_submission(self):
        for expiry in ['2000-01-01T00:00:00Z', '2999-01-01T00:00:00Z']:
            with self.subTest(expiry=expiry):
                path = MODULE.job_state_path('lost')
                MODULE.write_json(path, {'jobId':'lost', 'expiresAt':expiry, 'status':'running', 'workerPid':None,
                                         'request':{'prompt':'Keep me'}, 'attempt':{'phase':'submitting', 'threadId':'t'}})
                report, err = MODULE.get_generate_status('lost')
                self.assertIsNone(err)
                self.assertEqual((report['status'], report['done'], report['threadId']), ('unknown', True, 't'))
                self.assertEqual(MODULE.read_json(path)['request']['prompt'], 'Keep me')


if __name__ == '__main__':
    unittest.main()
