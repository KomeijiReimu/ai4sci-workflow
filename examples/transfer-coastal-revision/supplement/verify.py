#!/usr/bin/env python3
"""Independent numerical implementation; NumPy needed only for this check."""
import argparse
import csv
import hashlib
import json
from pathlib import Path
import numpy as np

root = Path(__file__).resolve().parent
cli = argparse.ArgumentParser(description=__doc__)
cli.add_argument('inputs', type=Path)
args = cli.parse_args()
with (root/'research/centered-sensitivity.csv').open() as f:
    summary = {(r['model'], r['period']): r for r in csv.DictReader(f)}
with (root/'research/centered-period-draws.csv').open() as f:
    output_draws = {(r['model'], r['draw']): r for r in csv.DictReader(f)}
manifest = json.loads((root/'inputs.json').read_text())
with (root/'research/summary.csv').open() as f:
    raw_summary = {(r['model'], r['period']): r for r in csv.DictReader(f)}
with (root/'research/period-draws.csv').open() as f:
    raw_by_id = {(r['model'], r['draw']):r for r in csv.DictReader(f)}
with (root/'research/support.csv').open() as f:
    support={r['model']:r for r in csv.DictReader(f)}
windows = {'whole':(1900,2019), 'early':(1900,1959), 'late':(1960,2019), 'after-decade':(1970,2019),
           **{f'{y}-{y+19}':(y,y+19) for y in [1900,1920,1940,2000]}}
max_err=0.0
for suffix,model in zip('abcd', ['Tr','TrNc','TrNcZw','TrNcPd']):
    files = [args.inputs/f'original-{k}-{suffix}.csv' for k in ['curve','rate-draws']]
    for path in files:
        assert hashlib.sha256(path.read_bytes()).hexdigest() == manifest[path.name]['sha256']
    curve=np.genfromtxt(files[0],delimiter=',',names=True)
    ensemble=np.genfromtxt(files[1],delimiter=',',skip_header=1)
    y=curve['time'][1:-1]; level=dict(zip(curve['time'],curve['trend']))
    np.testing.assert_array_equal(y, np.arange(1891,2020)); np.testing.assert_array_equal(ensemble[:,0],curve['time'])
    from_levels=5*(curve['trend'][2:]-curve['trend'][:-2]); ix=np.argmin(from_levels)
    assert int(y[ix])==int(support[model]['minimum_fitted_rate_year'])
    np.testing.assert_allclose(from_levels[ix],float(support[model]['minimum_fitted_mm_per_year']),rtol=0,atol=2e-12)
    annual_draws=ensemble[1:-1,1:]; assert annual_draws.shape==(129,100)
    # Center each *year*, before any time averaging; get the fitted multi-year mean
    # independently by telescoping the centered derivative at its four boundary levels.
    residual=annual_draws-np.mean(annual_draws,axis=1,keepdims=True)
    periods={}; unshifted={}
    for period,(a,b) in windows.items():
        estimate=5*(level[b+1]+level[b]-level[a]-level[a-1])/(b-a+1)
        periods[period]=(estimate,estimate+residual[(y>=a)&(y<=b)].mean(axis=0))
        unshifted[period]=annual_draws[(y>=a)&(y<=b)].mean(axis=0)
    for label in ['late','after-decade']:
        periods[label+'-minus-early']=tuple(b-a for a,b in zip(periods['early'],periods[label]))
        unshifted[label+'-minus-early']=unshifted[label]-unshifted['early']
    for p,(point,draws) in periods.items():
        row=summary[model,p]; actual=np.array([float(row[k]) for k in ['estimate','lo95','lo90','draw_median','hi90','hi95']]);
        expected=np.r_[point,np.quantile(draws,[.025,.05,.5,.95,.975])];
        max_err=max(max_err,float(np.abs(expected-actual).max()))
        np.testing.assert_allclose(actual,expected,rtol=0,atol=2e-12)
        np.testing.assert_allclose([float(output_draws[model,str(i)][p]) for i in range(100)],draws,rtol=0,atol=2e-12)
        raw=raw_summary[model,p]; raw_expected=np.r_[point,np.quantile(unshifted[p],[.025,.05,.5,.95,.975])]; raw_actual=[float(raw[k]) for k in ['estimate','lo95','lo90','draw_median','hi90','hi95']]
        np.testing.assert_allclose(raw_actual,raw_expected,rtol=0,atol=2e-12)
        np.testing.assert_allclose([float(raw_by_id[model,str(i)][p]) for i in range(100)],unshifted[p],rtol=0,atol=2e-12)
        max_err=max(max_err,float(np.abs(raw_expected-raw_actual).max()))
    np.testing.assert_allclose(periods['whole'][1], (periods['early'][1]+periods['late'][1])/2,rtol=0,atol=2e-12)
assert len(summary)==40 and len(output_draws)==400
gauge=np.genfromtxt(args.inputs/'gauge-observations.csv',delimiter=',',skip_header=1)
np.testing.assert_allclose(gauge[:,-1],gauge[:,1:7].mean(axis=1),rtol=0,atol=1e-9)
with (root/'research/gauge-check.csv').open() as f:
    for r in csv.DictReader(f):
        subset=gauge[(gauge[:,0]>=int(r['first']))&(gauge[:,0]<=int(r['last']))]
        slope=np.polyfit(subset[:,0],subset[:,-1],1)[0]*10
        np.testing.assert_allclose(slope,float(r['raw_OLS_mm_per_year']),rtol=0,atol=2e-12)
print(f'OK: 40 fitted summaries, unshifted and centered percentiles, 8000 paired draw summaries, 3 raw panel slopes; max absolute summary discrepancy {max_err:.3g} mm/yr.')
