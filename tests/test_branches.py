import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from checks.branches import branches


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / 'examples/branch-decision'
CSV = 'research/cells.csv'


def cell(identifier):
    return {'key': {'id': identifier}, 'path': CSV, 'column': 'score'}


class BranchDecisions(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / '.local' / 'tmp'
        scratch.mkdir(parents=True, exist_ok=True)
        temp = tempfile.TemporaryDirectory(dir=scratch)
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        r = self.root / 'research'
        r.mkdir()
        (r / 'run.json').write_text(json.dumps({'status': 'completed', 'outputs': [CSV]}))
        inventory = self.root / 'dev-ids.txt'
        inventory.write_bytes(b'unit-17\nunit-34\n')
        self.inventory = f'dev-ids.txt,{hashlib.sha256(inventory.read_bytes()).hexdigest()}'
        self.rows = ('id,fold,limit,rule,width,score,other\n'
                     'a,dev,3,x,1,0.5,100\n'
                     'b,dev,3,y,1,0.50000000000000000000001,200\n'
                     'c,dev,3,z,1,0.49999999999999999999999,300\n'
                     'd,dev,3,z,2,0.49,400\n')
        header, *data = self.rows.splitlines()
        self.rows = '\n'.join([header + ',inventory,ids_sha256', *(line + ',' + self.inventory for line in data), ''])
        self.stage = {'parent': 'a', 'observation': 'The reference is exactly halfway.',
                      'predictions': ['A signed shift will lower the residual.', 'Quantization will erase the shift.'],
                      'vary': 'rule', 'budget': 2,
                      'children': [{'id': 'b', 'value': 'y', 'result': cell('b')},
                                   {'id': 'c', 'value': 'z', 'result': cell('c')}],
                      'decision': {'kind': 'best', 'selected': 'c', 'reason': 'The residual is smallest.'}}
        self.tree = {'root': {'id': 'a', 'result': cell('a')}, 'direction': 'min', 'matched': ['fold', 'limit'],
                     'population': {'path': 'inventory', 'sha256': 'ids_sha256'},
                     'settings': ['rule', 'width'], 'rounds': [self.stage]}

    def check(self, expected, error=None):
        (self.root / CSV).write_text(self.rows)
        (self.root / 'research/branches.json').write_text(json.dumps(self.tree))
        code, detail = branches(self.root)
        self.assertEqual(code, expected, detail)
        if error:
            self.assertIn(error, detail['errors'][0])
        return detail

    def test_scalar_requires_unique_improvement_in_declared_direction_on_raw_decimals(self):
        for direction, best, adverse in [('min', 'c', 'b'), ('max', 'b', 'c')]:
            self.tree['direction'] = direction
            self.stage['decision']['selected'] = best
            nodes = self.check(0)['nodes']
            self.assertEqual(nodes[best]['contrast'], 'better')
            self.assertEqual(nodes[adverse]['contrast'], 'adverse')
            self.stage['decision']['selected'] = adverse
            self.check(2, 'raw scores')
        self.stage['decision'] = {'kind': 'none', 'reason': 'No unique improvement.'}
        self.check(2, 'raw scores')

    def test_none_when_adverse_tied_with_parent_or_two_best_children(self):
        rows = self.rows
        for b, c in [('0.6', '0.7'), ('0.5', '0.5'), ('0.4', '0.4')]:
            with self.subTest(b=b, c=c):
                self.rows = rows.replace('0.50000000000000000000001', b).replace('0.49999999999999999999999', c)
                self.stage['decision'] = {'kind': 'none', 'reason': 'No unique strict improvement.'}
                self.check(0)
                self.stage['decision'] = {'kind': 'best', 'selected': 'b', 'reason': 'First listed.'}
                self.check(2, 'raw scores')

    def test_confounding_sample_change_and_wrong_metric_are_not_ranked(self):
        rows = self.rows
        decision = self.stage['decision']
        for key, adjusted in [('fold', 'c,test,3,z,1'), ('limit', 'c,dev,8,z,1'),
                              ('rule', 'c,dev,3,y,1'), ('width', 'c,dev,3,z,4'), ('metric column', 'c,dev,3,z,1')]:
            with self.subTest(key=key):
                self.rows = rows.replace('c,dev,3,z,1', adjusted)
                self.stage['children'][1]['result']['column'] = 'other' if key == 'metric column' else 'score'
                self.stage['decision'] = decision
                self.check(2, 'comparable')
                self.stage['decision'] = {'kind': 'stop', 'reason': 'Conditions differed. No ranking.'}
                node = self.check(0)['nodes']['c']
                self.assertEqual((node['contrast'], node['differences']), ('incomparable', [key]))

    def test_follow_is_a_judgment_and_child_inherits_actual_selected_settings(self):
        self.stage['decision'] = {'kind': 'follow', 'selected': 'c', 'reason': 'Study how this rule scales.'}
        extra = dict(self.stage, parent='c', vary='width', budget=1, children=[{'id': 'd', 'value': '2', 'result': cell('d')}],
                     decision={'kind': 'best', 'selected': 'd', 'reason': 'Smallest on the recorded fold.'})
        self.tree['rounds'].append(extra)
        self.assertEqual(self.check(0)['nodes']['d']['parent'], 'c')
        extra['parent'] = 'b'
        self.check(2, 'parent must be')
        extra['parent'] = 'c'
        self.rows = self.rows.replace('d,dev,3,z,2', 'd,dev,3,x,2')
        self.check(2, 'comparable')
        self.stage['decision']['selected'] = 'b'
        self.tree['rounds'].pop()
        self.assertEqual(self.check(0)['nodes']['b']['contrast'], 'adverse')

    def test_population_bytes_not_display_label_or_file_name_decide_comparability(self):
        rows = self.rows
        other = self.root / 'same-fold.txt'
        original = (self.root / 'dev-ids.txt').read_bytes()
        for data, expected in ((original, 0), (b'unit-17\nunit-35\n', 2)):
            other.write_bytes(data)
            lookup = f'{other.name},{hashlib.sha256(data).hexdigest()}'
            self.rows = rows.replace('300,' + self.inventory, '300,' + lookup)
            self.check(expected, 'comparable' if expected else None)
        self.stage['decision'] = {'kind': 'pending', 'reason': 'Repeat on the actual matched units.'}
        self.assertEqual(self.check(1)['nodes']['c']['differences'], ['ids_sha256'])
        other.write_bytes(original)
        self.check(2, 'population digest')

    def test_failed_attempt_and_untried_alternative_remain_visible_without_a_score(self):
        failed, untried = self.stage['children']
        del failed['result'], untried['result']
        complete_rows = self.rows
        self.rows = '\n'.join(self.rows.splitlines()[:2]) + '\n'
        (self.root / 'failure.log').write_text('Input did not load.\n')
        failed['failures'] = [{'command': 'python3 trial.py', 'exit': 4, 'log': 'failure.log', 'reason': 'No input.'}]
        self.stage['decision'] = {'kind': 'pending', 'reason': 'Need an input for the deciding contrast.'}
        report = self.check(1)
        self.assertEqual(report['incomplete'], ['a: Need an input for the deciding contrast.'])
        self.assertEqual(report['nodes']['b'], {'parent': 'a', 'status': 'failed'})
        self.assertEqual(report['nodes']['c'], {'parent': 'a', 'status': 'untried'})
        failed['failures'][0].update(exit=0, reason='Exited normally but wrote no measurement.')
        self.assertEqual(self.check(1)['nodes']['b']['status'], 'failed')
        self.stage['decision'] = {'kind': 'stop', 'reason': 'The requested study only asked for a feasibility decision.'}
        self.check(0)
        self.stage['decision'] = {'kind': 'none', 'reason': 'No result.'}
        self.check(2, 'comparable')
        self.stage['decision'] = {'kind': 'best', 'selected': 'c', 'reason': 'Maybe next time.'}
        self.check(2, 'measured child')
        failed['result'], untried['result'] = cell('b'), cell('c')
        self.rows = complete_rows
        self.check(2, 'exceed budget')
        self.stage['budget'] = 3
        self.assertEqual(self.check(0)['decisions']['a']['attempts'], 3)
        (self.root / 'failure.log').unlink()
        self.check(2, 'failure.log')

    def test_row_identity_output_binding_and_real_baseline(self):
        self.tree['root']['result']['key'] = {'id': 'missing'}
        self.check(2, 'matched 0 rows')
        self.tree['root']['result']['key'] = {'fold': 'dev'}
        self.check(2, 'matched 4 rows')
        self.tree['root']['result']['key'] = {'id': 'a'}
        c = self.stage['children'][1]
        c['result']['key'] = {'other': '200'}
        self.check(2, 'already used')
        c['result'] = cell('c')
        (self.root / 'research/run.json').write_text(json.dumps({'outputs': ['research/archive.csv']}))
        self.check(2, 'declared run output')
        self.tree['root']['result']['path'] = '../elsewhere.csv'
        self.check(2, 'project-relative')

    def test_no_independent_confirmation_alias_or_unregistered_selection(self):
        self.stage['decision']['kind'] = 'confirm'
        self.check(2)
        self.stage['decision'] = {'kind': 'follow', 'selected': 'a', 'reason': 'Point back at the parent.'}
        self.check(2, 'measured child')
        self.stage['children'][0]['id'] = 'a'
        self.check(2, 'new ID')

    def test_round_notes_and_plan_fields_required(self):
        for prop, bad in [('predictions', ['same', 'same']), ('observation', ''), ('budget', True), ('vary', 'fold')]:
            with self.subTest(prop=prop):
                saved = self.stage[prop]
                self.stage[prop] = bad
                self.check(2)
                self.stage[prop] = saved

    def test_showcase_blocks_deletion_of_required_branch_ledger(self):
        study = self.root / 'archived'
        shutil.copytree(EXAMPLE / 'research', study / 'research')
        command = [sys.executable, ROOT / 'ai4sci.py', 'audit', study]
        intact = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(intact.returncode, 0, intact.stdout + intact.stderr)
        (study / 'research/branches.json').unlink()
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report['deliverability'], 'blocked')
        self.assertTrue(any('branches.json' in error for error in report['branches']['errors']))

    def test_showcase_clean_replay_and_adverse_promotion(self):
        fresh = self.root / 'replay'
        research = fresh / 'research'
        research.mkdir(parents=True)
        shutil.copy(EXAMPLE / 'run.py', fresh)
        shutil.copy(EXAMPLE / 'research/plan.json', research)
        for command in ([sys.executable, ROOT / 'ai4sci.py', 'freeze', '.'], [sys.executable, 'run.py']):
            result = subprocess.run(command, cwd=fresh, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual({p.name: p.read_bytes() for p in research.iterdir()},
                         {p.name: p.read_bytes() for p in (EXAMPLE / 'research').iterdir()})
        code, detail = branches(fresh)
        self.assertEqual(code, 0, detail)
        self.assertEqual({k: int(v['score']) for k, v in detail['nodes'].items()},
                         {'raw': 396, 'adjacent': 512, 'paired': 257, 'runs': 19})
        ledger = research / 'branches.json'
        changed = json.loads(ledger.read_text())
        changed['rounds'][0]['decision']['selected'] = 'adjacent'
        ledger.write_text(json.dumps(changed))
        code, detail = branches(fresh)
        self.assertEqual(code, 2)
        self.assertIn('raw scores', detail['errors'][0])
        before = ledger.read_bytes()
        result = subprocess.run([sys.executable, 'run.py'], cwd=fresh, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(ledger.read_bytes(), before)

    def test_showcase_records_a_pending_round_before_measuring_its_child(self):
        fresh = self.root / 'timing'
        r = fresh / 'research'
        r.mkdir(parents=True)
        for name in ('plan.json', 'plan.sha256'):
            shutil.copy(EXAMPLE / 'research' / name, r)
        shutil.copy(EXAMPLE / 'run.py', fresh)
        # Observe the ledger at the measurement boundary, not just after replay.
        probe = '''
import json
import run
real_measure = run.payload
seen = []
def observe(trace, lag, packing):
    if lag:
        tree = json.loads((run.RESEARCH / 'branches.json').read_text())
        stage = tree['rounds'][-1]
        value = str(lag) if stage['vary'] == 'lag' else packing
        node, = (child for child in stage['children'] if child['value'] == value)
        assert stage['decision']['kind'] == 'pending' and 'result' not in node
        assert stage['observation'] and len(set(stage['predictions'])) == 2 and stage['budget'] > 0
        seen.append((stage['parent'], node['id']))
    return real_measure(trace, lag, packing)
run.payload = observe
run.main()
assert seen == [('raw', 'adjacent'), ('raw', 'paired'), ('paired', 'runs')]
'''
        result = subprocess.run([sys.executable, '-c', probe], cwd=fresh, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
