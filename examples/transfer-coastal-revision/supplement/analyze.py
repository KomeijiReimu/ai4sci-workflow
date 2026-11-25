#!/usr/bin/env python3
"""Aggregate archived annual rate trajectories. No fitting, simulation or network access."""
import argparse
import csv
import hashlib
import json
import math
import platform
from pathlib import Path
from statistics import fmean

ROOT = Path(__file__).resolve().parent
MODELS = {'a': 'Tr', 'b': 'TrNc', 'c': 'TrNcZw', 'd': 'TrNcPd'}
WINDOWS = {'whole': (1900, 2019), 'early': (1900, 1959), 'late': (1960, 2019),
           '1900-1919': (1900, 1919), '1920-1939': (1920, 1939),
           '1940-1959': (1940, 1959), '2000-2019': (2000, 2019),
           'after-decade': (1970, 2019)}
IDS = [str(i) for i in range(100)]
YEARS = list(range(1890, 2021))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(inputs, name, manifest):
    path = inputs / name
    if digest(path) != manifest[name]['sha256']:
        raise ValueError(f'{name}: input checksum mismatch')
    with path.open(newline='') as stream:
        rows = list(csv.DictReader(stream))
    if [int(r['time']) for r in rows] != YEARS:
        raise ValueError(f'{name}: missing, reordered or duplicate year')
    return {int(r['time']): r for r in rows}


def quantile(sorted_values, p):
    h = p * (len(sorted_values) - 1)
    left = int(h)
    return sorted_values[left] + (h-left)*(sorted_values[math.ceil(h)]-sorted_values[left])


def write_rows(path, rows):
    with path.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator='\n')
        writer.writeheader()
        for row in rows:
            writer.writerow({k: format(v, '.12f') if isinstance(v, float) else v for k,v in row.items()})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('inputs', type=Path, help='directory of named v1 CSVs (read-only)')
    args = parser.parse_args()
    research = ROOT/'research'
    plan_hash = digest(research/'plan.json')
    if (research/'plan.sha256').read_text() != plan_hash+'\n':
        raise ValueError('plan digest mismatch')
    amendment_hash = digest(research/'calibration-amendment.md')
    if (research/'calibration-amendment.sha256').read_text() != amendment_hash+'  calibration-amendment.md\n':
        raise ValueError('amendment digest mismatch')
    manifest = json.loads((ROOT/'inputs.json').read_text())
    gauge = load(args.inputs, 'gauge-observations.csv', manifest)
    stations = ['20','22','23','24','25','32']
    obs = {}
    for year,r in gauge.items():
        values = [float(r[s]) for s in stations]; obs[year] = float(r['Average'])
        if not all(map(math.isfinite, values)) or abs(fmean(values)-obs[year]) > 1e-9 or not math.isfinite(obs[year]):
            raise ValueError(f'incomplete gauge panel or inconsistent Average at {year}')
    gauge_rows = []
    for period in ['whole', 'early', 'late']:
        start, end = WINDOWS[period]; ys=range(start, end+1); mid=fmean(ys)
        slope = 10 * math.fsum((y-mid)*obs[y] for y in ys)/math.fsum((y-mid)**2 for y in ys)
        gauge_rows.append(dict(period=period,first=start,last=end,n_years=len(ys),stations=len(stations),raw_OLS_mm_per_year=slope))

    summary, draws, checks, raw_summary, raw_draws = [], [], [], [], []
    for suffix, model in MODELS.items():
        curve = load(args.inputs, f'original-curve-{suffix}.csv', manifest)
        rates = load(args.inputs, f'original-rate-draws-{suffix}.csv', manifest)
        if list(rates[1900]) != ['time']+IDS:
            raise ValueError(f'{model}: expected draw IDs 0 through 99')
        endpoints = [curve[y]['rate_slr'] for y in (1890, 2020)] + [rates[y][d] for y in (1890,2020) for d in IDS]
        if any(x.strip().lower() not in {'', 'nan','na'} for x in endpoints):
            raise ValueError(f'{model}: unexpected nonmissing endpoint rate')
        point = {y:float(curve[y]['rate_slr']) for y in YEARS[1:-1]}
        by_year = {y:[float(rates[y][d]) for d in IDS] for y in point}
        if not all(math.isfinite(v) for y,r in by_year.items() for v in [point[y],*r]):
            raise ValueError(f'{model}: missing or invalid interior rate')
        err = max(abs(point[y]-5*(float(curve[y+1]['trend'])-float(curve[y-1]['trend']))) for y in point)
        if err > 1e-9:
            raise ValueError(f'{model}: rate units or time alignment inconsistent with centered derivative')
        minimum=min(point,key=point.__getitem__)
        checks.append(dict(model=model,first_rate_year=min(point),last_rate_year=max(point),n_rate_years=len(point),n_draws=len(IDS),max_derivative_error_mm_per_year=err,minimum_fitted_rate_year=minimum,minimum_fitted_mm_per_year=point[minimum]))
        periods = {}
        for label, (first,last) in WINDOWS.items():
            years = range(first,last+1)
            periods[label] = (fmean(point[y] for y in years), [fmean(by_year[y][j] for y in years) for j in range(len(IDS))])
        for late in ('late', 'after-decade'):
            pe, de = periods['early']; pl, dl = periods[late]
            periods[late+'-minus-early'] = (pl-pe, [b-a for b,a in zip(dl,de)])
        adjusted = {}
        for label,(estimate, ensemble) in periods.items():
            raw_quantiles = [quantile(sorted(ensemble),p) for p in (.025,.05,.50,.95,.975)]
            rlo, rl, rm, ru, rhi = raw_quantiles
            raw_summary.append(dict(model=model,period=label,estimate=estimate,lo95=rlo,hi95=rhi,lo90=rl,hi90=ru,draw_median=rm))
            raw_mean = fmean(ensemble); shift = estimate-raw_mean
            adjusted[label] = [v+shift for v in ensemble]
            seq = sorted(adjusted[label]); lo, l, m, u, hi = [quantile(seq,p) for p in (.025,.05,.50,.95,.975)]
            summary.append(dict(model=model,period=label,estimate=estimate,lo95=lo,hi95=hi,lo90=l,hi90=u,draw_median=m,uncalibrated_draw_mean=raw_mean,additive_shift=shift))
        for j, d in enumerate(IDS):
            draws.append(dict(model=model, draw=d, **{k:v[j] for k,v in adjusted.items()}))
            raw_draws.append(dict(model=model, draw=d, **{k:v[1][j] for k,v in periods.items()}))

    # Preserve the raw frozen estimands at their declared paths. The additional,
    # assumption-dependent sensitivity has its own clearly named files.
    outputs = {'research/summary.csv':raw_summary,'research/period-draws.csv':raw_draws,
               'research/centered-sensitivity.csv':summary,'research/centered-period-draws.csv':draws,
               'research/gauge-check.csv':gauge_rows,'research/support.csv':checks}
    for name, rows in outputs.items():
        write_rows(ROOT/name, rows)
    conditions = dict(archive='8c4b55df2b88feb4ebaa191f6d3e8bb9a4b8c86b', primary_years='1900-2019 inclusive',draws=len(IDS),interval='linear empirical percentile')
    (research/'run.json').write_text(json.dumps(dict(status='completed',command='python3 analyze.py "$COASTAL_INPUTS"',
        exit_code=0,plan_sha256=plan_hash,python=platform.python_version(),software='Python standard library only',
        code_sha256=digest(Path(__file__)),input_manifest_sha256=digest(ROOT/'inputs.json'),amendment_sha256=amendment_hash,
        outputs=list(outputs),sha256={p:digest(ROOT/p) for p in outputs},
        arms=[dict(id=model,conditions=conditions) for model in MODELS.values()]),indent=2)+'\n')
    print('Computed 40 model-period summaries; 400 model-specific draw rows; 3 observation checks.')


if __name__ == '__main__':
    main()
