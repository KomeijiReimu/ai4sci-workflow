"""Render three paired MAE comparisons from primary.csv; no plotting dependency."""
import csv
import math
import sys
from pathlib import Path


def render(table, destination):
    with table.open() as f:
        rows = list(csv.DictReader(f))
    keys = ['day_ahead_mae_mw', 'weekly_mae_mw']
    maximum = max(float(r[key]) for r in rows for key in keys)
    step = 1000 if maximum < 6000 else 2000
    xmax = step * math.ceil(maximum / step)
    x = lambda value: 178 + 475 * value / xmax
    labels = {'all': 'All paired hours', 'high': 'High demand', 'other': 'Remaining hours'}
    colors = ['#106d70', '#77487f']
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="750" height="344" viewBox="0 0 750 344" role="img" aria-labelledby="title desc">',
             '<title id="title">Mean absolute error of two forecasts for German load in 2019</title>',
             '<desc id="desc">Horizontal paired bars compare the archived day-ahead forecast with the previous week at the same local time. Smaller errors are better. High demand is classified by realized load.</desc>',
             '<rect width="750" height="344" fill="#fff"/><g font-family="system-ui, sans-serif" fill="#132a37">',
             '<text x="18" y="27" font-size="20" font-weight="bold">How far off was each forecast?</text>',
             '<text x="18" y="51" font-size="14">Mean absolute error (MW) · German national load, 2019</text>']
    for i, name in enumerate(['Archived day-ahead', 'Same hour last week']):
        xx = 178 + 218*i
        parts.append(f'<rect x="{xx}" y="67" width="14" height="12" fill="{colors[i]}"/><text x="{xx+21}" y="78" font-size="13">{name}</text>')
    for value in range(0, xmax+1, step):
        xx = x(value)
        parts.append(f'<path d="M{xx:.2f} 91V303" stroke="#d1dadd"/><text x="{xx:.2f}" y="326" text-anchor="middle" font-size="12">{value:,}</text>')
    for i, r in enumerate(rows):
        yy = 103 + i*72
        parts.append(f'<text x="18" y="{yy+13}" font-size="16" font-weight="bold">{labels[r["group"]]}</text><text x="18" y="{yy+33}" font-size="13">{int(r["hours"]):,} hours</text>')
        for j, key in enumerate(keys):
            v = float(r[key]); y = yy + 22*j
            parts.append(f'<rect x="178" y="{y}" width="{x(v)-178:.2f}" height="15" fill="{colors[j]}"/><text x="{x(v)+6:.2f}" y="{y+13}" font-size="13">{v:,.0f}</text>')
    destination.write_text('\n'.join(parts+['</g></svg>'])+'\n', encoding='utf-8')


if __name__ == '__main__':
    render(Path(sys.argv[1]), Path(sys.argv[2]))
