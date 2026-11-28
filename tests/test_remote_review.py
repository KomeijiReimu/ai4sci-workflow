"""Exercise the verifier against the OpenCode v2 wire shape, without a live agent."""

from contextlib import redirect_stderr, redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from checks import remote_review as review


class RemoteReview(unittest.TestCase):
    def setUp(self):
        tmp = Path(__file__).resolve().parents[1] / '.local/tmp'
        tmp.mkdir(parents=True, exist_ok=True)
        folder = tempfile.TemporaryDirectory(dir=tmp)
        self.addCleanup(folder.cleanup)
        self.plan = Path(folder.name) / 'plan'
        self.package = Path(folder.name) / 'package.tar.gz'
        self.plan.write_bytes(b'plan\xff')
        self.package.write_bytes(b'\x1f\x8b\xff')
        plan, package = [hashlib.sha256(p.read_bytes()).hexdigest() for p in (self.plan, self.package)]
        self.sessions, self.messages = {}, {}
        self.args = [str(self.plan), str(self.package), '--parent', 'ses-parent', '--qualified', 'host/reviewer#high']
        for role in ('design', 'science', 'launch'):
            child = 'ses-' + role
            self.args.extend(['--' + role, child])
            model = {'providerID': 'host', 'id': 'reviewer', 'variant': 'high'}
            self.sessions[child] = {'id': child, 'parentID': 'ses-parent', 'agent': 'oracle', 'model': model}
            marker = f'AI4SCI-REMOTE {role} {plan}' + ('' if role == 'design' else ' ' + package)
            self.messages[child] = [
                {'id': 'idle', 'type': 'idle', 'outcome': 'succeeded'},
                {'id': 'answer', 'type': 'assistant', 'agent': 'oracle', 'model': dict(model), 'finish': 'stop',
                 'time': {'created': 100, 'completed': 120}, 'content': [
                     {'type': 'reasoning', 'text': 'PRIVATE-THOUGHT'},
                     {'type': 'text', 'text': 'Checked the prespecified comparison and its inputs.\n' + marker}]},
            ]
        self.proc = patch.object(review.subprocess, 'run', side_effect=self.host).start()
        self.addCleanup(patch.stopall)

    def host(self, cmd, **kwargs):
        self.assertEqual(cmd[:2], ['opencode', 'api'])
        self.assertEqual(cmd[3], '--param')
        child = cmd[4].removeprefix('sessionID=')
        if cmd[2] == 'session.get':
            self.assertEqual(len(cmd), 5)
            body = {'data': self.sessions[child]}
        else:
            self.assertEqual(cmd[2:], ['session.message.list', '--param', 'sessionID=' + child,
                                       '--param', 'order=desc', '--param', 'limit=2'])
            body = {'data': self.messages[child][:2], 'cursor': {'next': 'older'}}
        return subprocess.CompletedProcess(cmd, 0, json.dumps(body).encode())

    def check(self, code, expected, *extra):
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            status = review.main(self.args + list(extra))
        self.assertEqual(status, code, err.getvalue())
        self.assertIn(expected, (err if code else out).getvalue())
        self.assertEqual((out if code else err).getvalue(), '')
        self.assertNotIn('PRIVATE', out.getvalue() + err.getvalue())

    def test_clean_pass_and_resumed_design(self):
        self.check(0, 'review return references matched.')
        self.assertEqual(self.proc.call_count, 6)
        self.sessions['ses-design']['parentID'] = 'ses-original'
        self.messages['ses-design'][1]['model'].pop('variant')
        self.check(0, 'references matched', '--design-parent', 'ses-original', '--qualified', 'host/reviewer',
                   '--contributor', 'ses-implementer')

    def test_finals_must_acknowledge_latest_design_even_for_identical_bytes(self):
        self.messages['ses-design'][1]['time']['completed'] = 150
        self.check(1, 'acknowledgement pending from science, launch')
        self.messages['ses-science'][1]['time']['completed'] = 150
        self.check(1, 'acknowledgement pending from launch')
        self.messages['ses-launch'][1]['time']['completed'] = 151
        self.check(0, 'references matched')

    def test_reused_child_contributor_or_parent(self):
        for flag, value in [('--science', 'ses-design'), ('--launch', 'ses-science'),
                            ('--contributor', 'ses-launch'), ('--parent', 'ses-science'),
                            ('--design-parent', 'ses-design')]:
            with self.subTest(flag=flag):
                self.check(1, 'reused', flag, value)
        self.proc.assert_not_called()

    def test_stale_even_after_one_byte_change(self):
        for artifact, role in [(self.plan, 'design'), (self.package, 'science')]:
            with self.subTest(role=role):
                raw = artifact.read_bytes()
                artifact.write_bytes(raw[:-1] + b'\xfe')
                self.check(1, role + ': final return marker mismatch')
                artifact.write_bytes(raw)

    def test_actual_assistant_profile_not_session_default_or_agent_label(self):
        answer = self.messages['ses-science'][1]
        for key in ('providerID', 'id', 'variant'):
            with self.subTest(key=key), patch.dict(answer['model'], {key: 'weaker'}):
                self.check(1, 'science: assistant profile not qualified')
        with patch.dict(answer['model'], {'variant': None}):
            self.check(1, 'assistant profile not qualified', '--qualified', 'host/reviewer')
        answer['agent'] = 'another-agent'
        self.check(1, 'assistant agent mismatch')

    def test_no_fallback_to_older_success(self):
        history = self.messages['ses-science']
        idle, good = history
        for newest in [[{'type': 'user'}], [{'type': 'idle', 'outcome': 'failed'}],
                       [idle, {**good, 'finish': 'tool-calls'}], [idle, {**good, 'time': {'created': 125}}],
                       [idle, {**good, 'error': {'message': 'PRIVATE'}}],
                       [idle, {**good, 'content': [{'type': 'text', 'text': 'Rejected: control is missing.'}]}]]:
            with self.subTest(newest=newest):
                self.messages['ses-science'] = newest + history
                self.check(1, 'science:')

    def test_require_standalone_marker_and_visible_review(self):
        answer = self.messages['ses-design'][1]
        body = answer['content'][-1]['text']
        marker = body.splitlines()[-1]
        for text in [marker, '\n' + marker, body + ' ', body + '\nmore', body.replace('\n', ' ')]:
            with self.subTest(text=text):
                answer['content'] = [{'type': 'reasoning', 'text': body}, {'type': 'text', 'text': text}]
                self.check(1, 'design:')
        answer['content'] = [{'type': 'text', 'text': body}, {'type': 'tool', 'state': {'status': 'completed'}}]
        self.check(1, 'final return marker mismatch')

    def test_foreign_parent_session_identity_and_cold_fork(self):
        for change, reason in [({'parentID': 'ses-other'}, 'parent mismatch'), ({'id': 'ses-design'}, 'child'),
                               ({'fork': {'sessionID': 'ses-design'}}, 'forked'),
                               ({'outcome': 'interrupted'}, 'session outcome')]:
            with self.subTest(change=change), patch.dict(self.sessions['ses-launch'], change):
                self.check(1, reason)

    def test_missing_artifact_or_verifier_and_bad_response(self):
        self.proc.side_effect = FileNotFoundError('PRIVATE')
        self.check(1, 'OpenCode session.get unavailable')
        self.proc.side_effect = None
        self.proc.return_value = subprocess.CompletedProcess([], 0, b'not-json PRIVATE')
        self.check(1, 'malformed OpenCode session.get')
        self.plan.unlink()
        self.check(1, 'artifact missing')


if __name__ == '__main__':
    unittest.main()
