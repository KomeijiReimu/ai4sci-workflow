"""Run the frozen development-marker study from the pinned minimal frame."""
import argparse
from collections import Counter
import csv
import hashlib
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent


def save(path, rows):
    with path.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, rows[0], lineterminator='\n'); w.writeheader()
        for row in rows:
            w.writerow({k: format(v, '.12g') if isinstance(v, float) else v for k, v in row.items()})


def sample(rows, tag, need_hdi):
    complete = [r for r in rows if r['region'] and r['growth'+tag] is not None and r['gain_le'+tag] is not None and (not need_hdi or r['gain_hdi19'] is not None)]
    counts = Counter(r['region'] for r in complete)
    return [r for r in complete if counts[r['region']] > 1], [r for r in complete if counts[r['region']] == 1]


def fit(label, rows, tag='19', *, controls=True, squares=False, hdi=False, omitted=''):
    x = np.array([r['growth'+tag] for r in rows]); y = np.array([r['gain_hdi19' if hdi else 'gain_le'+tag] for r in rows])
    regions = np.array([r['region'] for r in rows]); levels = sorted(set(regions))
    base = [np.ones(x.size)]
    if controls:
        le, log_g = (np.array([r[key] for r in rows]) for key in ('le0', 'log_gdp0'))
        base += [le - le.mean(), log_g - log_g.mean()]
        base.extend(regions == region for region in levels[1:])
        if squares:
            base.extend([base[1]**2, base[2]**2])
    X = np.column_stack([*base, x]); q, upper = np.linalg.qr(X, mode='reduced')
    if np.linalg.matrix_rank(upper) != X.shape[1]:
        raise ValueError(f'{label}: singular design')
    b = np.linalg.solve(upper, q.T @ y); residual = y-X @ b
    h = (q*q).sum(axis=1)
    if np.max(h) >= 1 - 1e-10:
        raise ValueError(f'{label}: HC3 undefined')
    score = np.linalg.solve(upper, q.T)[-1, :] * residual / (1-h)
    se = float(np.sqrt(score @ score)); beta = float(b[-1]); lo, hi = beta-1.96*se, beta+1.96*se
    reduced_y = y - q[:, :-1] @ (q[:, :-1].T @ y)
    partial = 1 - (residual @ residual) / (reduced_y @ reduced_y)
    return dict(model=label, endpoint=2000+int(tag), outcome='HDI change' if hdi else 'life-years gained', omitted_region=omitted,
                n=len(y), regions=len(levels), slope=beta, se_hc3=se, lo95=lo, hi95=hi, partial_r2=float(partial),
                lower_above_benchmark='' if hdi else int(lo > .5))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--frame', type=Path, default=ROOT / 'data/analysis-frame.csv')
    p.add_argument('--out', type=Path, required=True, help='directory for summary CSV files')
    a = p.parse_args()
    digest = hashlib.sha256(a.frame.read_bytes()).hexdigest()
    if digest != (ROOT/'provenance/frame.sha256').read_text().split()[0]:
        raise ValueError(f'frame SHA-256 mismatch: {digest}')
    with a.frame.open(encoding='utf-8', newline='') as f:
        frame = list(csv.DictReader(f))
    all_regions = sorted({row['region'] for row in frame})
    rows = [{k:(v if k in ('iso3','region') else float(v) if v else None) for k,v in row.items()} for row in frame]
    groups, coverage = {}, []
    for name, tag, need_hdi in [('primary', '19', False), ('short', '15', False), ('common', '19', True)]:
        group, singletons = sample(rows, tag, need_hdi); groups[name] = group
        used, drops = {r['iso3'] for r in group}, {r['iso3'] for r in singletons}
        for region in ['ALL', *all_regions]:
            rr = [r for r in rows if region=='ALL' or r['region']==region]
            coverage.append(dict(sample=name, region=region, frame_n=len(rr), used=sum(r['iso3'] in used for r in rr),
                missing_growth=sum(r['growth'+tag] is None for r in rr), missing_life_gain=sum(r['gain_le'+tag] is None for r in rr),
                missing_hdi_gain=sum(r['gain_hdi19'] is None for r in rr) if need_hdi else '', singleton_excluded=sum(r['iso3'] in drops for r in rr)))
    main_sample, common = groups['primary'], groups['common']
    fits = [fit('unadjusted', main_sample, controls=False), fit('adjusted', main_sample),
            fit('quadratic_baselines', main_sample, squares=True), fit('shorter_endpoint', groups['short'], tag='15'),
            fit('matched_life', common), fit('matched_hdi', common, hdi=True)]
    for i, name in enumerate(sorted({r['region'] for r in main_sample}), 1):
        fits.append(fit(f'omit_{i}', [r for r in main_sample if r['region'] != name], omitted=name))
    a.out.mkdir(parents=True, exist_ok=True)
    save(a.out/'coverage.csv', coverage); save(a.out/'estimates.csv', fits)
    row = fits[1]
    print(f'frame SHA-256 {digest}; fitted {len(fits)} models; primary n={row["n"]}, slope={row["slope"]:.6f}, HC3 95% CI [{row["lo95"]:.6f}, {row["hi95"]:.6f}]')


if __name__ == '__main__':
    main()
