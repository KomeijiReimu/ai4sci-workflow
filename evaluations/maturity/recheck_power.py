"""Independently compare the two electricity tables with the original OPSD CSV (SQLite)."""
import argparse
import csv
import hashlib
import math
from datetime import datetime
from pathlib import Path
import sqlite3


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv', type=Path, help='OPSD 2020-10-06 hourly single-index archive')
    parser.add_argument('results', type=Path, help='power-forecast/research directory')
    args = parser.parse_args()
    digest = hashlib.sha256()
    with args.csv.open('rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            digest.update(block)
    if digest.hexdigest() != '6a7f2bc571314cbf9c321cc03437691cd4be95c3a6f075e60ff99e8035c704c8':
        raise SystemExit('not the frozen OPSD hourly archive')

    # Use the supplied offset-bearing wall time, not the author's UTC/zoneinfo code.
    db = sqlite3.connect(':memory:')
    db.execute('CREATE TABLE readings(w TEXT, obs REAL, fc REAL)')
    with args.csv.open(newline='', encoding='utf-8') as f:
        rows = csv.reader(f)
        header = next(rows)
        wall, actual, forecast = (header.index(c) for c in ('cet_cest_timestamp',
                                 'DE_load_actual_entsoe_transparency', 'DE_load_forecast_entsoe_transparency'))
        db.executemany('INSERT INTO readings VALUES (?,?,?)', (
            (datetime.fromisoformat(r[wall]).replace(tzinfo=None).isoformat(sep=' '),
             float(r[actual]) if r[actual] else None, float(r[forecast]) if r[forecast] else None)
            for r in rows if '2018-12-25' <= r[wall][:10] < '2020-01-01'))
    db.executescript("""
        CREATE TABLE civil AS SELECT w, MIN(obs) obs, MIN(fc) fc FROM readings GROUP BY w HAVING COUNT(*)=1;
        CREATE UNIQUE INDEX by_time ON civil(w);
        CREATE TABLE pairs AS SELECT a.w, a.obs, a.fc, b.obs lag, (a.fc+b.obs)/2 midpoint
            FROM civil a JOIN civil b ON b.w=DATETIME(a.w,'-7 days')
            WHERE a.w>='2019-01-01' AND a.obs IS NOT NULL AND a.fc IS NOT NULL AND b.obs IS NOT NULL;
    """)
    high = db.execute('SELECT MIN(v) FROM (SELECT obs v,CUME_DIST() OVER(ORDER BY obs) prob FROM pairs) WHERE prob>=0.9').fetchone()[0]
    for name, selector, cutoff_key in [('primary', 'obs', 'cutoff_mw'), ('followup', 'midpoint', 'midpoint_cutoff_mw')]:
        cutoff = db.execute(f'SELECT MIN(v) FROM (SELECT {selector} v,CUME_DIST() OVER(ORDER BY {selector}) prob FROM pairs) WHERE prob>=0.9').fetchone()[0]
        with (args.results / f'{name}.csv').open(newline='', encoding='utf-8') as f:
            seen = set()
            for row in csv.DictReader(f):
                group = row['group']
                if group in seen:
                    raise SystemExit(f'{name}: duplicate {group}')
                seen.add(group)
                filters = {'all': '1', 'high': f'{selector}>={cutoff}', 'other': f'{selector}<{cutoff}',
                           'midpoint_high': f'{selector}>={cutoff}', 'midpoint_other': f'{selector}<{cutoff}'}
                n, d, w, overlap = db.execute('SELECT COUNT(*),AVG(ABS(obs-fc)),AVG(ABS(obs-lag)),SUM(obs>=?) FROM pairs WHERE '+filters[group], (high,)).fetchone()
                expected = {'hours': n, cutoff_key: cutoff, 'day_ahead_mae_mw': d, 'weekly_mae_mw': w, 'advantage_mw': w-d}
                if name == 'followup':
                    expected['realized_high_hours'] = overlap
                for col, v in expected.items():
                    if not math.isclose(float(row[col]), v, rel_tol=0, abs_tol=1e-6):
                        raise SystemExit(f'{name}/{group}/{col}: {row[col]} != {v}')
                print(f'{name} {group}: n={n}, day-ahead={d:.6f}, weekly={w:.6f}, advantage={w-d:.6f} MW')
            required = {'all','high','other'} if name == 'primary' else {'midpoint_high','midpoint_other'}
            if seen != required:
                raise SystemExit(f'{name}: unexpected groups {seen}, expected {required}')
    db.close()


if __name__ == '__main__':
    main()
