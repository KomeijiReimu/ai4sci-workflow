"""Read-only check from the pinned CSV. Run with python3 -B verify_independent.py."""

import csv
import json
from collections import Counter, defaultdict
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
from pathlib import Path

here = Path(__file__).resolve().parent
source = here.parent / 'data/penguins.csv'


def rows(path):
    with path.open(encoding='utf-8', newline='') as stream:
        return list(csv.DictReader(stream))


def nine(q):
    scale = 10**9
    k = round(q * scale)
    return f"{'-' if k < 0 else ''}{abs(k) // scale}.{abs(k) % scale:09d}"


digest = sha256(source.read_bytes()).hexdigest()
assert digest == 'f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93'
train, test, excluded = {}, {}, []
totals, unknown_sex = Counter(), Counter()
for i, r in enumerate(rows(source), 1):
    yr, sp = int(r['year']), r['species']
    assert yr in (2007, 2008, 2009)
    totals[yr] += 1
    x, y = r['flipper_length_mm'], r['body_mass_g']
    if x in ('NA', '') or y in ('NA', ''):
        excluded.append((i, yr, sp, x, y))
        continue
    (test if yr == 2009 else train)[i] = (int(x), int(y), sp)
    unknown_sex[yr] += r['sex'] in ('NA', '')

# Pairwise differences eliminate the intercept. Sum over unordered training pairs.
pairs = [(x-u, y-v) for (x, y, _), (u, v, _) in combinations(train.values(), 2)]
b = Fraction(sum(dx*dy for dx, dy in pairs), sum(dx*dx for dx, _ in pairs))
mu = Fraction(sum(y for _, y, _ in train.values()), len(train))
a = sum(y-b*x for x, y, _ in train.values()) / len(train)

saved = rows(here / 'predictions.csv')
assert len(saved) == len(test) and {int(r['row_id']) for r in saved} == test.keys()
errors, by_species = [], defaultdict(list)
for r in saved:
    x, y, sp = test[int(r['row_id'])]
    yhat = a+b*x
    assert (x, y) == (int(r['flipper_length_mm']), int(r['body_mass_g']))
    assert (nine(mu), nine(yhat)) == (r['mean_prediction_g'], r['linear_prediction_g'])
    e, f = abs(mu-y), abs(yhat-y)
    errors.append((e, f))
    by_species[sp].append(e-f)

base, line = (sum(v)/len(v) for v in zip(*errors))
delta = sum(e-f for e, f in errors) / len(errors)
assert base-line == delta
counts = (2009, totals[2007]+totals[2008], len(train), totals[2007]+totals[2008]-len(train),
          totals[2009], len(test), totals[2009]-len(test))
fields = 'test_year train_total train_used train_excluded test_total test_used test_excluded'.split()
metrics = 'train_mean_g intercept_g slope_g_per_mm mean_mae_g linear_mae_g reduction_g'.split()
summary = dict(zip(fields + metrics, [*map(str, counts), *map(nine, (mu, a, b, base, line, delta))]))
assert rows(here / 'results.csv') == [summary]
conditions = {'input_sha256': digest, 'metric': 'MAE (g)'}
for arm, ids in [('train', train), ('test', test)]:
    conditions[arm + '_row_ids_sha256'] = sha256(''.join(f'{i}\n' for i in ids).encode()).hexdigest()
arms = json.loads((here / 'run.json').read_text())['arms']
assert {arm['id'] for arm in arms} == {'training_mean', 'flipper_ols'}
assert all(arm['conditions'] == conditions for arm in arms)
print(summary, '\nyear totals:', dict(totals), 'excluded:', excluded, 'eligible sex missing:', dict(unknown_sex))
for sp, differences in sorted(by_species.items()):
    print(sp, 'train:', sum(s == sp for _, _, s in train.values()), 'test:', len(differences),
          'mean paired difference (g):', nine(sum(differences)/len(differences)))
print('All paired records and summary fields match at stored precision.')
