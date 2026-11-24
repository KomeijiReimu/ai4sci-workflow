"""Exploratory sensitivity specified in research/followup-decision.md after the primary run."""
import math
import sys
from pathlib import Path

from study import cutoff, pairs, write_csv


def main(archive, output):
    rows, _ = pairs(archive)
    realized_cutoff = cutoff(rows)
    scores = [(p+w)/2 for _, y, p, w in rows]
    threshold = sorted(scores)[(9*len(scores)+9)//10 - 1]
    results = []
    for name, high in [('midpoint_high', True), ('midpoint_other', False)]:
        subset = [r for r, score in zip(rows, scores) if (score >= threshold) == high]
        n = len(subset)
        a = math.fsum(abs(pred-y) for _, y, pred, ref in subset) / n
        b = math.fsum(abs(ref-y) for _, y, pred, ref in subset) / n
        results.append((name, n, threshold, sum(y >= realized_cutoff for _, y, _, _ in subset),
                        f'{a:.9f}', f'{b:.9f}', f'{b-a:.9f}'))
    write_csv(output/'followup.csv', ['group', 'hours', 'midpoint_cutoff_mw', 'realized_high_hours',
              'day_ahead_mae_mw', 'weekly_mae_mw', 'advantage_mw'], results)
    print((output/'followup.csv').read_text(), end='')


if __name__ == '__main__':
    main(Path(sys.argv[1]), Path(sys.argv[2]))
