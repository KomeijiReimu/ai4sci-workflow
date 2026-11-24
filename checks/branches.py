"""Check recorded exploratory decisions against local measurements. Never launch a run."""

import hashlib
from pathlib import Path

from .audit import (INPUT_ERRORS, cell_fields, csv_cell, file_id, local_file, manifest,
                    records, text)


def names(obj, field):
    values = records(obj, field)
    if (not values or any(not isinstance(v, str) or not v.strip() for v in values)
            or len(set(values)) != len(values)):
        raise ValueError(f'{field}: expected distinct nonblank names')
    return values


def shape(obj, required, optional=()):
    if not isinstance(obj, dict) or not set(required) <= set(obj) <= set(required) | set(optional):
        raise ValueError(f'expected fields {", ".join(required)} with optional {", ".join(optional) or "none"}')


def branches(root: Path):
    nodes, decisions, errors, incomplete = {}, {}, [], []
    label = 'branches.json'
    try:
        root = root.resolve(strict=True)
        name = 'research/branches.json'
        tree = manifest(local_file(root, name).read_bytes(), name)
        shape(tree, ('root', 'direction', 'population', 'matched', 'settings', 'rounds'))
        direction = text(tree, 'direction')
        matched, settings = names(tree, 'matched'), names(tree, 'settings')
        population = tree['population']
        shape(population, ('path', 'sha256'))
        source, sha = text(population, 'path'), text(population, 'sha256')
        columns = [source, sha, *matched, *settings]
        if direction not in ('min', 'max') or len(set(columns)) != len(columns):
            raise ValueError('expected min or max and distinct population, matched and settings columns')
        run_name = 'research/run.json'
        run = manifest(local_file(root, run_name).read_bytes(), run_name)
        outputs = names(run, 'outputs')
        tables, used_rows, results, digests = {}, set(), {}, {}

        def measure(node, parent):
            identifier = text(node, 'id')
            loc = node['result']
            shape(loc, ('path', 'key', 'column'))
            path = local_file(root, text(loc, 'path'))
            if loc['path'] not in outputs:
                raise ValueError('result CSV is not a declared run output')
            key, col = cell_fields(loc)
            if col in columns:
                raise ValueError('metric cannot also be a comparison condition')
            i, score = csv_cell(path, key, col, tables)
            row_id = file_id(path), i
            if row_id in used_rows:
                raise ValueError('result row already used by another node')
            used_rows.add(row_id)
            row = tables[path][1][i]
            for field in columns:
                text(row, field)
            inventory = local_file(root, row[source])
            if inventory not in digests:
                if not inventory.stat().st_size:
                    raise ValueError('population file is empty')
                digest = hashlib.sha256()
                with inventory.open('rb') as stream:
                    for chunk in iter(lambda: stream.read(1048576), b''):
                        digest.update(chunk)
                digests[inventory] = digest.hexdigest()
            if digests[inventory] != row[sha]:
                raise ValueError(f'population digest differs from {row[source]}')
            results[identifier] = col, score, row
            nodes[identifier] = {'parent': parent, 'status': 'measured', 'score': row[col]}

        baseline = tree['root']
        shape(baseline, ('id', 'result'))
        first = text(baseline, 'id')
        measure(baseline, None)
        eligible = {first}
        rounds = records(tree, 'rounds')
        if not rounds:
            raise ValueError('a branch ledger needs a decision round')
        for index, stage in enumerate(rounds):
            label = f'rounds[{index}]'
            shape(stage, ('parent', 'observation', 'predictions', 'vary', 'budget', 'children', 'decision'))
            parent = text(stage, 'parent')
            if parent not in eligible:
                raise ValueError('parent must be the root or a previously selected child, used once')
            eligible.remove(parent)
            label = f'round under {parent}'
            parent_col, reference, fixed = results[parent]
            text(stage, 'observation')
            vary = text(stage, 'vary')
            if vary not in settings or len(names(stage, 'predictions')) != 2:
                raise ValueError('name one setting to vary and two competing predictions')
            budget = stage['budget']
            if type(budget) is not int or budget < 1:
                raise ValueError('budget must be a positive number of child attempts')
            scores, values, spent = {}, set(), 0
            children = records(stage, 'children')
            if not children:
                raise ValueError('decision round has no children')
            for child in children:
                shape(child, ('id', 'value'), ('result', 'failures'))
                cid, value = text(child, 'id'), text(child, 'value')
                label = f'{parent} -> {cid}'
                if cid in nodes or value in values or value == fixed[vary]:
                    raise ValueError('child needs a new ID and a distinct change from parent and siblings')
                values.add(value)
                failures = records(child, 'failures') if 'failures' in child else []
                for failure in failures:
                    shape(failure, ('command', 'exit', 'log', 'reason'))
                    text(failure, 'command')
                    text(failure, 'reason')
                    if type(failure['exit']) is not int or not local_file(root, text(failure, 'log')).stat().st_size:
                        raise ValueError('a failed attempt needs an integer exit and a nonempty local log')
                spent += len(failures)
                if 'result' not in child:
                    nodes[cid] = {'parent': parent, 'status': 'failed' if failures else 'untried'}
                    continue
                measure(child, parent)
                spent += 1
                col, score, row = results[cid]
                differences = [k for k in [sha, *matched, *settings] if row[k] != (value if k == vary else fixed[k])]
                if col != parent_col:
                    differences.append('metric column')
                if differences:
                    nodes[cid].update(contrast='incomparable', differences=differences)
                else:
                    gain = (score - reference) if direction == 'max' else (reference - score)
                    scores[cid] = gain
                    nodes[cid]['contrast'] = 'better' if gain > 0 else 'tie' if gain == 0 else 'adverse'
            label = f'decision under {parent}'
            if spent > budget:
                raise ValueError(f'{spent} attempts exceed budget {budget}')
            decision = stage['decision']
            kind = text(decision, 'kind')
            select = kind in ('best', 'follow')
            shape(decision, ('kind', 'reason', 'selected') if select else ('kind', 'reason'))
            reason = text(decision, 'reason')
            if kind not in ('best', 'none', 'follow', 'stop', 'pending'):
                raise ValueError('unknown decision kind')
            if select:
                selected = text(decision, 'selected')
                if selected not in results or nodes[selected]['parent'] != parent:
                    raise ValueError('selected node must be a measured child of this parent')
                eligible.add(selected)
            if kind in ('best', 'none'):
                if len(scores) != len(children):
                    raise ValueError('scalar decision requires comparable measurements for all children')
                top = max(scores.values())
                winners = [cid for cid, gain in scores.items() if gain == top and gain > 0]
                if (kind == 'best' and winners != [decision['selected']]) or (kind == 'none' and len(winners) == 1):
                    raise ValueError('scalar decision disagrees with raw scores: ' + str(winners))
            if kind == 'pending':
                incomplete.append(f'{parent}: {reason}')
            decisions[parent] = {**decision, 'attempts': spent, 'budget': budget}
    except INPUT_ERRORS as exc:
        errors.append(f'{label}: {exc}')
    code = 2 if errors else int(bool(incomplete))
    return code, {'use': 'exploratory', 'nodes': nodes, 'decisions': decisions,
                  'errors': errors, 'incomplete': incomplete}
