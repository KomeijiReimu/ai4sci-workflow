"""Reproduce the uniform-mesh quadrature study using only the standard library."""

import csv
import hashlib
import io
import json
import math
from pathlib import Path


def compute_csv():
    stream = io.StringIO()
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(("n", "estimate", "trap_error", "trap_order", "left_estimate",
                     "left_error", "left_order"))
    previous = None
    for n in (4, 8, 16, 32, 64):
        h = 1 / n
        values = [(i * h) ** 2 for i in range(n + 1)]
        trap = h * (values[0] / 2 + sum(values[1:-1]) + values[-1] / 2)
        left = h * sum(values[:-1])
        et, el = abs(trap - 1 / 3), abs(left - 1 / 3)
        pt = pl = ""
        if abs((trap - 1 / 3) - 1 / (6 * n**2)) > 1e-14:
            raise ValueError(f"K1: trapezoid bias differs from derivation at n={n}")
        if not left < 1 / 3:
            raise ValueError(f"K3: left sum is not below the reference at n={n}")
        if previous is not None:
            pt, pl = math.log2(previous[0] / et), math.log2(previous[1] / el)
            if abs(pt - 2) > 1e-9:
                raise ValueError(f"K2: trapezoid order outside tolerance at n={n}")
            if not (el < previous[1] and 0.9 <= pl <= 1.1):
                raise ValueError(f"K3: left error decay outside bounds at n={n}")
        writer.writerow((n, trap, et, pt, left, el, pl))
        previous = et, el
    return stream.getvalue()


def plot_csv(text):
    rows = list(csv.DictReader(io.StringIO(text)))
    # Log2 coordinates: equal horizontal spacing means step doubling.
    xs = [86 + 108 * (math.log2(int(r['n'])) - 2) for r in rows]
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 590 365">',
           '<title>Absolute integration error versus panel count</title>',
           '<desc>Log-log plot of trapezoid (solid) and left sums (dashed) from results.csv.</desc>',
           '<rect width="590" height="365" fill="white"/>',
           '<g font-family="sans-serif" font-size="13" fill="#18232d">',
           '<text x="25" y="25" font-size="17">Absolute error on the uniform mesh</text>']
    for exponent in range(-15, -2, 2):
        y = 75 + 18 * (-3 - exponent)
        svg.extend([f'<path d="M80 {y}H530" stroke="#dadee2"/>',
                    f'<text x="70" y="{y+4}" text-anchor="end">2^{exponent}</text>'])
    for x, row in zip(xs, rows):
        svg.append(f'<text x="{x:.1f}" y="318" text-anchor="middle">{row["n"]}</text>')
    svg.append('<text x="303" y="346" text-anchor="middle">Panel count (n)</text>')
    for field, color, dash, legend, label in (
        ('trap_error', '#155c99', '', 86, 'Trapezoid'),
        ('left_error', '#994318', ' stroke-dasharray="5 4"', 245, 'Left endpoints'),
    ):
        ys = [75 + 18 * (-3 - math.log2(float(row[field]))) for row in rows]
        points = ' '.join(f'{x:.2f},{y:.2f}' for x, y in zip(xs, ys))
        svg.extend([f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"{dash}/>',
                    f'<path d="M{legend} 48h25" stroke="{color}" stroke-width="2"{dash}/>',
                    f'<text x="{legend+32}" y="52">{label}</text>'])
        for x, y in zip(xs, ys):
            svg.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="3.5" fill="{color}"/>')
    return '\n'.join(svg + ['</g></svg>', ''])


def main():
    root = Path(__file__).resolve().parent
    (root / 'research').mkdir(exist_ok=True)
    text = compute_csv()
    artifacts = {'research/results.csv': text.encode(),
                 'research/errors.svg': plot_csv(text).encode()}
    record = {'status': 'completed', 'command': 'python3 run.py',
              'outputs': list(artifacts),
              'sha256': {name: hashlib.sha256(data).hexdigest()
                         for name, data in artifacts.items()}}
    artifacts['research/run.json'] = (json.dumps(record, indent=2) + '\n').encode()
    for name, data in artifacts.items():
        path = root / name
        if path.exists() and path.read_bytes() != data:
            raise SystemExit(f'Refusing to replace differing artifact: {name}')
    for name, data in artifacts.items():
        path = root / name
        if path.exists():
            print(f'verified {name}')
        else:
            with path.open('xb') as output:
                output.write(data)
            print(f'created {name}')


if __name__ == '__main__':
    main()
