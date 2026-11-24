"""Measure lossless payload sizes on one deterministic interleaved counter trace."""

import csv
import hashlib
import json
from itertools import groupby
from pathlib import Path


RESEARCH = Path('research')
CSV = 'research/bytes.csv'


def payload(trace, lag, packing):
    residuals = [v - (trace[i - lag] if lag and i >= lag else 0) for i, v in enumerate(trace)]
    codes = [2 * v if v >= 0 else -2 * v - 1 for v in residuals]
    if packing == 'runs':
        codes = [v for code, group in groupby(codes) for v in (len(list(group)), code)]
    data = ''.join(map(chr, codes)).encode('utf-8')

    decoded = list(map(ord, data.decode('utf-8')))
    if packing == 'runs':
        decoded = [v for count, v in zip(decoded[::2], decoded[1::2], strict=True) for _ in range(count)]
    values = []
    for code in decoded:
        delta = -(code // 2) - 1 if code % 2 else code // 2
        values.append(delta + (values[-lag] if lag and len(values) >= lag else 0))
    if values != trace:
        raise ValueError('payload did not decode to the input')
    return len(data)


def save(name, obj):
    (RESEARCH / name).write_text(json.dumps(obj, indent=2) + '\n', encoding='utf-8')


def main():
    digest = hashlib.sha256((RESEARCH / 'plan.json').read_bytes()).hexdigest()
    if (RESEARCH / 'plan.sha256').read_bytes() != (digest + '\n').encode('ascii'):
        raise SystemExit('Freeze the supplied plan before replay.')
    if any(p.name not in ('plan.json', 'plan.sha256') for p in RESEARCH.iterdir()):
        raise SystemExit('Use a fresh study. Keep earlier measurements.')
    trace_file = RESEARCH / 'trace.txt'
    trace_file.write_bytes(''.join(f'{(-81 if i % 2 == 0 else 50) + (i // 2) % 32}\n' for i in range(256)).encode('ascii'))
    raw = trace_file.read_bytes()
    trace_id = hashlib.sha256(raw).hexdigest()
    trace = list(map(int, raw.splitlines()))
    with Path(CSV).open('x', newline='', encoding='utf-8') as stream:
        csv.writer(stream, lineterminator='\n').writerow(('node', 'trace_file', 'trace_sha256', 'samples', 'lag', 'packing', 'bytes'))

    costs = {}

    def measure(node, lag, packing):
        cid = node['id']
        costs[cid] = payload(trace, lag, packing)
        with Path(CSV).open('a', newline='', encoding='utf-8') as stream:
            csv.writer(stream, lineterminator='\n').writerow((cid, trace_file.as_posix(), trace_id, len(trace), lag, packing, costs[cid]))
        node['result'] = {'path': CSV, 'key': {'node': cid}, 'column': 'bytes'}

    tree = {'root': {'id': 'raw'}, 'direction': 'min', 'population': {'path': 'trace_file', 'sha256': 'trace_sha256'}, 'matched': ['samples'],
            'settings': ['lag', 'packing'], 'rounds': []}
    measure(tree['root'], 0, 'literal')
    adjacent, paired = {'id': 'adjacent', 'value': '1'}, {'id': 'paired', 'value': '2'}
    first = {'parent': 'raw', 'observation': f"Without prediction the trace occupies {costs['raw']} payload bytes.",
             'predictions': ['If neighboring samples track each other, the previous sample will shorten the payload.',
                             'If only the two component streams change slowly, predicting two places back will help but the previous sample will not.'],
             'vary': 'lag', 'budget': 2, 'children': [adjacent, paired],
             'decision': {'kind': 'pending', 'reason': 'Measure both lags against the literal baseline.'}}
    tree['rounds'].append(first)
    save('branches.json', tree)
    for node in first['children']:
        measure(node, int(node['value']), 'literal')
        save('branches.json', tree)

    if not costs['paired'] < min(costs['raw'], costs['adjacent']):
        first['decision'] = {'kind': 'stop', 'reason': 'The paired predictor did not uniquely improve payload size. Do not spend the last trial on it.'}
    else:
        first['decision'] = {'kind': 'best', 'selected': 'paired', 'reason': 'Only the two-place predictor reduced the byte count.'
                             if costs['adjacent'] >= costs['raw'] else 'The two-place predictor produced the smallest payload.'}
        runs = {'id': 'runs', 'value': 'runs'}
        second = {'parent': 'paired', 'observation': f"Two-place prediction used {costs['paired']} bytes for {len(trace)} residuals. Small residuals need not repeat.",
                  'predictions': ['If small codes recur in long runs, storing their counts will reduce the payload.',
                                  'If small codes mostly alternate, count fields will add bytes without much repetition to remove.'],
                  'vary': 'packing', 'budget': 1, 'children': [runs],
                  'decision': {'kind': 'pending', 'reason': 'Use the remaining trial to encode runs.'}}
        tree['rounds'].append(second)
        save('branches.json', tree)
        measure(runs, 2, 'runs')
        second['decision'] = ({'kind': 'best', 'selected': 'runs', 'reason': 'Run counts reduced the payload on this trace.'}
                              if costs['runs'] < costs['paired'] else {'kind': 'none', 'reason': 'Run counts did not reduce the payload.'})
    save('branches.json', tree)
    save('run.json', {'status': 'completed', 'command': 'python3 run.py', 'plan_sha256': digest,
                      'outputs': [CSV, trace_file.as_posix()], 'sha256': {CSV: hashlib.sha256(Path(CSV).read_bytes()).hexdigest(), trace_file.as_posix(): trace_id}})
    claims, lines = [], ['# Encoding the interleaved counters', '', 'These are payload sizes for one synthetic trace. Both ends know the predictor and packing rule.', '']
    for i, (node, size) in enumerate(costs.items(), 1):
        statement = f'The {node} encoding used {size} bytes.'
        evidence = {'kind': 'number', 'path': CSV, 'key': {'node': node}, 'column': 'bytes', 'atol': 0, 'value': size}
        claims.append({'id': f'C{i}', 'criterion': 'payload', 'status': 'supported', 'statement': statement, 'evidence': [evidence]})
        lines.extend((f'{statement} [C{i}]', ''))
    save('claims.json', {'claims': claims})
    (RESEARCH / 'paper.md').write_text('\n'.join(lines), encoding='utf-8')
    print(', '.join(f'{node}={size}' for node, size in costs.items()) + ' bytes')


if __name__ == '__main__':
    main()
