"""Build the three-wave analysis frame from the hash-identified packet (no downloads)."""
import argparse
import csv
import hashlib
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
YEARS = (2000, 2015, 2019)
GDP, LE = 'NY.GDP.PCAP.PP.KD', 'SP.DYN.LE00.IN'


def number(row, name):
    text = row.get(name, '').strip()
    if not text:
        return None
    value = float(text)
    if not math.isfinite(value):
        raise ValueError(f'nonfinite {name} at {row["iso3"]}, {row["year"]}')
    return value


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--packet', type=Path, required=True, help='directory containing the original data.csv')
    p.add_argument('--out', type=Path, required=True, help='new/replaceable output CSV path')
    a = p.parse_args()
    digests = {name: digest for digest, name in (line.split() for line in (ROOT/'provenance/inputs.sha256').read_text().splitlines())}
    if hashlib.sha256((a.packet/'data.csv').read_bytes()).hexdigest() != digests['data.csv']:
        raise ValueError('unexpected data.csv digest')
    panel, regions = {}, {}
    with (a.packet / 'data.csv').open(newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            iso, year, region = r['iso3'], int(r['year']), r['region'].strip()
            if regions.setdefault(iso, region) != region:
                raise ValueError(f'region not stable: {iso}')
            if year in YEARS:
                if (iso, year) in panel:
                    raise ValueError(f'duplicate endpoint: {iso} {year}')
                panel[iso, year] = r
    fields = ['iso3', 'region', 'log_gdp0', 'le0', 'growth15', 'gain_le15', 'growth19', 'gain_le19', 'gain_hdi19']
    a.out.parent.mkdir(parents=True, exist_ok=True)
    with a.out.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fields, lineterminator='\n'); w.writeheader()
        for iso, region in sorted(regions.items()):
            start = panel.get((iso, 2000), {})
            g0, l0, h0 = (number(start, k) for k in (GDP, LE, 'HDI'))
            row = dict(iso3=iso, region=region, log_gdp0=math.log(g0) if g0 is not None and g0 > 0 else None, le0=l0)
            for year, tag in [(2015, '15'), (2019, '19')]:
                end = panel.get((iso, year), {})
                g1, l1 = number(end, GDP), number(end, LE)
                if g0 is not None and g0 > 0 and g1 is not None and g1 > 0:
                    row['growth'+tag] = math.log(g1/g0) / math.log(1.5)
                if l1 is not None and l0 is not None:
                    row['gain_le'+tag] = l1 - l0
                if year == 2019:
                    h1 = number(end, 'HDI')
                    if h1 is not None and h0 is not None:
                        row['gain_hdi19'] = h1 - h0
            w.writerow(row)
    print(f'data.csv hash verified; {len(regions)} economy rows; frame SHA-256 {hashlib.sha256(a.out.read_bytes()).hexdigest()}')


if __name__ == '__main__':
    main()
