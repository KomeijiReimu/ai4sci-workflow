"""German national load, 2019: frozen paired comparison (Python standard library)."""
import argparse
import csv
import hashlib
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


BASE = "https://data.open-power-system-data.org/time_series/2020-10-06/"
FILE = "time_series_60min_singleindex.csv"
INPUT_SHA = "6a7f2bc571314cbf9c321cc03437691cd4be95c3a6f075e60ff99e8035c704c8"
ACTUAL = "DE_load_actual_entsoe_transparency"
FORECAST = "DE_load_forecast_entsoe_transparency"
ZONE = ZoneInfo("Europe/Berlin")
UTC = timezone.utc
DAY = timedelta(days=1)
HOUR = timedelta(hours=1)
START = datetime(2019, 1, 1, tzinfo=ZONE).astimezone(UTC)
END = datetime(2020, 1, 1, tzinfo=ZONE).astimezone(UTC)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def pairs(path):
    if digest(path) != INPUT_SHA:
        raise ValueError(f"Not the official {FILE} (SHA-256 mismatch): {path}")
    first = START - 7 * DAY
    values = {}
    with path.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        header = next(reader)
        ix = [header.index(k) for k in ('utc_timestamp', 'cet_cest_timestamp', ACTUAL, FORECAST)]
        for row in reader:
            t = datetime.fromisoformat(row[ix[0]].replace('Z', '+00:00'))
            if not first <= t < END:
                continue
            local = datetime.fromisoformat(row[ix[1]])
            if t in values or local.isoformat() != t.astimezone(ZONE).isoformat():
                raise ValueError(f"Duplicate UTC timestamp or Berlin offset mismatch: {t}")
            values[t] = tuple(float(row[i]) if row[i] else math.nan for i in ix[2:])

    # Build the calendar from the physical hour grid, not from observed rows.
    calendar = defaultdict(list)
    t = first
    while t < END:
        calendar[t.astimezone(ZONE).replace(tzinfo=None)].append(t)
        t += HOUR
    exclusions: Counter[str] = Counter(dict.fromkeys(('ambiguous_target', 'absent_lag_hour',
                                        'ambiguous_lag_hour', 'missing_actual',
                                        'missing_forecast', 'missing_lag_actual'), 0))
    kept = []
    t = START
    while t < END:
        local = t.astimezone(ZONE).replace(tzinfo=None)
        earlier = calendar.get(local - 7 * DAY, [])
        if len(calendar[local]) != 1:
            exclusions['ambiguous_target'] += 1
        elif not earlier:
            exclusions['absent_lag_hour'] += 1
        elif len(earlier) > 1:
            exclusions['ambiguous_lag_hour'] += 1
        else:
            y, pred = values.get(t, (math.nan, math.nan))
            ref = values.get(earlier[0], (math.nan, math.nan))[0]
            for number, kind in ((y, 'missing_actual'), (pred, 'missing_forecast'), (ref, 'missing_lag_actual')):
                if not math.isfinite(number):
                    exclusions[kind] += 1
                    break
            else:
                kept.append((t, y, pred, ref))
        t += HOUR
    return kept, dict(exclusions)


def cutoff(rows):
    # ceil(9*n/10), one-based rank, inclusive of ties.
    return sorted(r[1] for r in rows)[(9 * len(rows) + 9) // 10 - 1]


def write_csv(path, header, rows):
    with path.open('w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(header)
        writer.writerows(rows)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('archive', type=Path)
    ap.add_argument('output', type=Path)
    args = ap.parse_args()
    rows, exclusions = pairs(args.archive)
    scheduled = (END - START) // HOUR
    if len(rows) + sum(exclusions.values()) != scheduled:
        raise ValueError('Coverage counts do not reconcile')
    coverage = {'scheduled': scheduled, 'paired': len(rows), 'excluded': exclusions,
                'target_ids_sha256': hashlib.sha256(''.join(r[0].isoformat()+'\n' for r in rows).encode()).hexdigest()}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output/'coverage.json').write_text(json.dumps(coverage, indent=2)+'\n')
    if len(rows) * 100 < 95 * scheduled:
        raise ValueError('Frozen coverage threshold missed; see coverage.json')
    threshold = cutoff(rows)
    out = []
    for group, subset in [('all', rows), ('high', [r for r in rows if r[1] >= threshold]),
                          ('other', [r for r in rows if r[1] < threshold])]:
        n = len(subset)
        a = math.fsum(abs(pred-y) for _, y, pred, ref in subset) / n
        b = math.fsum(abs(ref-y) for _, y, pred, ref in subset) / n
        out.append((group, n, threshold, f'{a:.9f}', f'{b:.9f}', f'{b-a:.9f}'))
    write_csv(args.output/'primary.csv', ['group', 'hours', 'cutoff_mw', 'day_ahead_mae_mw',
              'weekly_mae_mw', 'advantage_mw'], out)
    print((args.output/'primary.csv').read_text(), end='')


if __name__ == '__main__':
    main()
