"""Review-trail regressions against the actual manuscripts, replies and evidence."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/review-rounds'
SPEC = 'research/rounds.json'
PAPER = 'research/paper.md'
REPLY = 'research/reply.md'


class ReviewRounds(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / '.local/tmp'
        scratch.mkdir(parents=True, exist_ok=True)
        temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        shutil.copytree(EXAMPLE, self.root, dirs_exist_ok=True)
        self.spec = json.loads((self.root / SPEC).read_text())
        self.first, self.last = self.spec['rounds']

    def check(self, status):
        (self.root / SPEC).write_text(json.dumps(self.spec))
        result = subprocess.run([sys.executable, ROOT / 'checks/rounds.py', self.root], capture_output=True, text=True)
        self.assertEqual(result.returncode, status, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['deliverability'], ('ready', 'incomplete', 'blocked')[status])
        return report

    def ref(self, name):
        return {'path': name, 'sha256': hashlib.sha256((self.root / name).read_bytes()).hexdigest()}

    def update_final(self, role, old, new):
        name = self.last[role]['path']
        file = self.root / name
        original = file.read_text()
        self.assertIn(old, original)
        file.write_text(original.replace(old, new))
        shutil.copyfile(file, self.root / (PAPER if role == 'manuscript' else REPLY))
        self.last[role] = self.ref(name)

    def test_two_reviewers_two_rounds_and_no_reconstructed_plan(self):
        report = self.check(0)
        self.assertFalse((self.root / 'research/plan.json').exists())
        self.assertEqual(report['history'][0]['issues'], {'I1': 'revised', 'I2': 'revised'})
        self.assertEqual(report['history'][1]['reopened'], ['I1'])
        self.assertEqual(report['history'][1]['new'], ['I3'])
        self.assertEqual(report['issues']['I3'], 'no-change')

    def test_reopened_and_unanswered_new_concern(self):
        self.last['decisions'] = []
        report = self.check(1)
        self.assertEqual(report['issues'], {'I1': 'reopened', 'I2': 'revised', 'I3': 'open'})
        self.assertIn('I1: reopened', report['incomplete'])

    def test_open_disagreement_with_explicit_reply(self):
        decision = self.last['decisions'][0]
        line = '[I1] [A1] [B2] [A2] We have not reconciled the two estimates.'
        self.update_final('reply', decision['response'], line)
        self.last['decisions'][0] = {'issue':'I1', 'status':'open', 'response':line}
        self.assertEqual(self.check(1)['issues']['I1'], 'reopened')

    def test_oracle_unregistered_followup_then_registered_reopening(self):
        line = "[I2] [B4] We have not resolved the reviewer's renewed objection about the threshold."
        text = (self.root / REPLY).read_text()
        self.update_final('reply', text, text + '\n' + line + '\n')
        self.assertIn('B4', self.check(2)['errors'][0])
        self.last['comments'].append({'id':'B4', 'issue':'I2', 'reviewer':'B', 'location':'## Interpretation',
                                      'comment':'What distinction does the annual threshold make?'})
        self.last['decisions'].append({'issue':'I2', 'status':'open', 'response':line})
        self.assertEqual(self.check(1)['issues']['I2'], 'reopened')

    def test_oracle_deleted_issue_and_misassigned_comment_remain_visible(self):
        self.last['comments'] = [c for c in self.last['comments'] if c['issue'] != 'I3']
        self.last['decisions'] = [d for d in self.last['decisions'] if d['issue'] != 'I3']
        self.assertIn('I3', self.check(2)['errors'][0])
        self.update_final('reply', '[I3] [B3]', '[I2] [A1]')
        self.assertIn('A1', self.check(2)['errors'][0])

    def test_oracle_citations_unmarked_prose_and_carried_issue(self):
        text = (self.root / REPLY).read_text()
        note = ('\n[C77] is a bibliography label, not a new issue.\n'
                'An editor can mention [B77] or [I99] in ordinary prose.\n'
                '[I2] [B1] The first round addressed the threshold question. See [C77].\n')
        self.update_final('reply', text, text + note)
        self.check(0)

    def test_oracle_marker_only_edit_is_not_a_revision(self):
        d = self.last['decisions'][1]
        old = d['passage']
        d.update(status='revised', passage=old + ' [C7]')
        self.update_final('manuscript', old, d['passage'])
        self.assertIn('I3', self.check(2)['errors'][0])
        d['status'] = 'no-change'
        self.check(0)
        self.update_final('manuscript', d['passage'], old + ' [C8]')
        self.assertIn('I3', self.check(2)['errors'][0])

    def test_bound_response_cannot_be_borrowed_from_another_issue(self):
        first, second = self.last['decisions']
        self.update_final('reply', second['response'] + '\n', '')
        borrowed = first['response'] + ' The separate baseline question [I3] [B3] remains unanswered.'
        self.update_final('reply', first['response'], borrowed)
        first['response'] = second['response'] = borrowed
        self.assertIn('I3', self.check(2)['errors'][0])

    def test_bound_response_requires_leading_comment_labels_not_prose(self):
        decision = self.last['decisions'][0]
        answer = decision['response'] + ' See claim [C9] for context.'
        self.update_final('reply', decision['response'], answer)
        decision['response'] = answer
        self.check(0)
        misplaced = answer.replace('[A2] ', '') + ' This also concerns [A2].'
        self.update_final('reply', answer, misplaced)
        decision['response'] = misplaced
        self.assertIn('I1', self.check(2)['errors'][0])

    def test_older_reply_or_manuscript_handed_over(self):
        for role, name in [('manuscript', PAPER), ('reply', REPLY)]:
            with self.subTest(role=role):
                shutil.copyfile(self.root / self.first[role]['path'], self.root / name)
                self.assertIn('byte for byte', self.check(2)['errors'][0])
                shutil.copyfile(self.root / self.last[role]['path'], self.root / name)

    def test_previous_reply_and_original_cannot_be_overwritten(self):
        for ref in (self.spec['original'], self.first['manuscript'], self.first['reply']):
            with self.subTest(path=ref['path']):
                file = self.root / ref['path']
                raw = file.read_bytes()
                file.write_bytes(raw + b'\n')
                self.assertIn('digest', self.check(2)['errors'][0])
                file.write_bytes(raw)

    def test_earlier_reply_or_comment_reference_with_refreshed_hashes(self):
        self.update_final('reply', self.last['manuscript']['path'], self.first['manuscript']['path'])
        self.assertIn('does not identify', self.check(2)['errors'][0])
        self.update_final('reply', self.first['manuscript']['path'], self.last['manuscript']['path'])
        line = self.last['decisions'][0]['response']
        self.update_final('reply', line, line.replace('[A2] ', ''))
        self.last['decisions'][0]['response'] = line.replace('[A2] ', '')
        self.assertIn('references', self.check(2)['errors'][0])

    def test_reply_only_closure_is_invalid_even_with_fresh_hashes(self):
        line = self.last['decisions'][0]['passage']
        old = self.first['decisions'][0]['passage']
        self.update_final('manuscript', line, old)
        self.assertIn('passage', self.check(2)['errors'][0])
        self.last['decisions'][0]['passage'] = old
        self.assertIn('previous manuscript', self.check(2)['errors'][0])

    def test_closed_passage_cannot_disappear_in_later_round(self):
        line = self.first['decisions'][1]['passage']
        self.update_final('manuscript', line, 'The threshold has now been crossed.')
        self.assertIn('I2: previously closed', self.check(2)['errors'][0])

    def test_digest_only_and_missing_evidence_do_not_close_issue(self):
        source = self.last['decisions'][0]['evidence'][1]
        source['quote'] = 'WMO reported no uncertainty.'
        self.assertIn('evidence quote missing', self.check(2)['errors'][0])
        del source['quote']
        self.assertIn('quote', self.check(2)['errors'][0])
        (self.root / source['path']).unlink()
        self.assertIn('wmo.txt', self.check(2)['errors'][0])

    def test_source_and_paper_may_use_different_words(self):
        decision = self.last['decisions'][0]
        translated = '哥白尼使用 ERA5 报告了相对工业化前的年温差，世界气象组织则综合了六套数据。'
        self.update_final('manuscript', decision['passage'], translated)
        decision['passage'] = translated
        for item, quote in zip(decision['evidence'], ['According to ERA5', 'WMO’s consolidated analysis of the six datasets']):
            del item['verbatim']
            item['quote'] = quote
        self.check(0)
        decision['evidence'][1]['quote'] = 'A sentence absent from the original.'
        self.assertIn('evidence quote missing', self.check(2)['errors'][0])

    def test_explicit_verbatim_binding_rejects_wrong_value_with_same_suffix(self):
        decision = self.last['decisions'][0]
        old = decision['passage']
        new = old.replace('1.60°C', '11.60°C')
        self.update_final('manuscript', old, new)
        decision['passage'] = new
        self.assertIn('verbatim quote', self.check(2)['errors'][0])

    def test_no_change_requires_original_text_and_reason_in_reply(self):
        decision = self.last['decisions'][1]
        line = decision['passage'] + ' The period is approximate.'
        self.update_final('manuscript', decision['passage'], line)
        decision['passage'] = line
        self.assertIn('no-change passage', self.check(2)['errors'][0])
        self.update_final('reply', decision['response'], '[I3] [B3]')
        decision['response'] = '[I3] [B3]'
        self.assertIn('response line', self.check(2)['errors'][0])

    def test_alias_or_paper_as_source(self):
        decision = self.last['decisions'][0]
        name = 'inputs/pretend-source.txt'
        os.link(self.root / PAPER, self.root / name)
        decision['evidence'] = [{**self.ref(name), 'quote':decision['passage']}]
        self.assertIn('aliases', self.check(2)['errors'][0])

    def test_duplicate_comment_wrong_location_and_invalid_shape(self):
        item = self.last['comments'][0]
        item['location'] = 'Unknown section'
        self.assertIn('location', self.check(2)['errors'][0])
        item['id'] = 'A1'
        self.assertIn('reused comment', self.check(2)['errors'][0])
        self.spec['rounds'][1] = []
        self.assertIn('expected an object', self.check(2)['errors'][0])

    def test_actual_package_must_match_round_and_submission_record(self):
        # Reuse an already packaged DOCX. These synthetic round comments are test data.
        study = ROOT / 'examples/penguins-revision'
        for name in (PAPER, 'research/claims.json', 'research/submission.json', 'research/delivery-review.json',
                     'research/results.csv', 'paper/final.docx'):
            (self.root / name).parent.mkdir(exist_ok=True)
            shutil.copyfile(study / name, self.root / name)
        v1 = 'versions/penguin-v1.md'
        shutil.copyfile(self.root / PAPER, self.root / v1)
        shutil.copyfile(self.root / 'paper/final.docx', self.root / 'versions/penguin-v1.docx')
        r1 = 'versions/penguin-reply-v1.md'
        response = '[I1] [A1] The manuscript now specifies the training set count.'
        (self.root / r1).write_text(f'Manuscript version: `{v1}`\n\n{response}\n')
        shutil.copyfile(self.root / r1, self.root / REPLY)
        original = 'versions/penguin-v0.md'
        (self.root / original).write_text('The study used penguin records.\n')
        self.spec = {'original':self.ref(original), 'rounds':[{
            'manuscript':self.ref(v1), 'reply':self.ref(r1), 'package':self.ref('versions/penguin-v1.docx'),
            'comments':[{'id':'A1', 'issue':'I1', 'reviewer':'A', 'comment':'How many training records?',
                         'location':'The study used penguin records.'}],
            'decisions':[{'issue':'I1', 'status':'revised', 'response':response,
                          'passage':'The training set contained 223 eligible records. [C1]',
                          'evidence':[{**self.ref('research/results.csv'), 'quote':'223', 'verbatim':True}]}]}]}
        self.check(0)
        with (self.root / 'versions/penguin-v1.docx').open('ab') as fp:
            fp.write(b'X')
        self.spec['rounds'][0]['package'] = self.ref('versions/penguin-v1.docx')
        self.assertIn('DOCX/PDF bytes', self.check(2)['errors'][0])
        (self.root / 'research/submission.json').unlink()
        self.assertIn('submission:', self.check(2)['errors'][0])


if __name__ == '__main__':
    unittest.main()
