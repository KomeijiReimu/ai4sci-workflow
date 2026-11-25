"""Recompute v1 fixed-period rate tests from eight pinned CSVs (standard library only)."""

import argparse
import csv
import hashlib
import io
import math
from pathlib import Path
from statistics import fmean, pstdev


# Archive basename, manuscript label, SHA-256 of results_*.csv and rates_*.csv,
# and the three two-decimal outputs of make_figures&tables.ipynb, cell 26.
MODELS = [
    ("NoRegressor", "Tr", "6ecf45ce849e730097e127e55de8caa39ec57d3830f9d7d7d1f68537d13bab17",
     "571088bd492cab765935f42721f75a1a27f5dcf9563cb6adb929d1f9c3fdddee", ("0.25", "0.06", "0.04")),
    ("NodalTide", "TrNc", "d6c5af8777b0a374a0e75e87b27231f288538c4295666e1193c4925cc09df1f2",
     "8e5079c6032c82d07d16fac2e006e333a27e8d35750a168ff7aa5f84c97a8db0", ("0.15", "0.01", "0.01")),
    ("NearestPointAverage", "TrNcZw", "8dbc11815fd6c907140f43432505e655a4f8fdd0503d695907677ac43922ac54",
     "53878e72d08530a14ee7d1aad34447c4332e0241662d294232e1414b9bfd13de", ("0.00", "0.00", "0.00")),
    ("PressureDifference", "TrNcPd", "50a70c3ba63b7fbc65a94bf7e8172bed6428d934711340aaf59b4e28216ed70a",
     "ed74589d5f4b8c2a79d6b592cd18566922e6a23120639004b981ebe2d09eb6a5", ("0.08", "0.04", "0.01")),
]


def load(path, digest):
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != digest:
        raise ValueError(f"SHA-256 mismatch: {path}")
    return {int(row["time"]): row for row in csv.DictReader(io.StringIO(raw.decode("utf-8")))}


def compare(curve, draws, early, late, years):
    def change(rows, column):
        return (fmean(float(rows[y][column]) for y in range(late, late + years))
                - fmean(float(rows[y][column]) for y in range(early, early + years)))

    fitted = change(curve, "rate_slr")
    paired = [change(draws, str(b)) for b in range(100)]
    se = pstdev(paired)  # np.std, ddof=0, as in fixed-period test (not annual band)
    p = 0.5 * math.erfc(fitted / (se * math.sqrt(2)))  # 1 - Phi(fitted / se)
    return fitted, se, p, fmean(paired), fmean(x - fitted for x in paired)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_dir", type=Path, help="outputs/ from the pinned KNMI archive")
    parser.add_argument("--study-names", action="store_true", help="read byte-identical original-{curve,rate-draws}-{a,b,c,d}.csv instead")
    args = parser.parse_args()
    data = {}
    print("v1 short periods: 2000–19 minus the 20 years starting in each named year (one-sided p)")
    print("model     1900         1920         1940")
    for letter, (name, label, curve_hash, draw_hash, reference) in zip("abcd", MODELS):
        curve_name, draw_name = ((f"original-curve-{letter}.csv", f"original-rate-draws-{letter}.csv")
                                 if args.study_names else (f"results_{name}.csv", f"rates_{name}.csv"))
        curve = load(args.input_dir / curve_name, curve_hash)
        draws = load(args.input_dir / draw_name, draw_hash)
        for y, row in curve.items():
            if row["rate_slr"] and float(row["rate_slr"]) != 5 * (float(curve[y + 1]["trend"]) - float(curve[y - 1]["trend"])):
                raise ValueError(f"{label} {y}: fitted rate differs from centered two-year trend derivative")
        ps = [compare(curve, draws, t, 2000, 20)[2] for t in (1900, 1920, 1940)]
        print(f"{label:7}", *(f"{p:.8f}" for p in ps))
        if tuple(f"{p:.2f}" for p in ps) != reference:
            raise ValueError(f"{label}: does not reproduce the archived notebook output {reference}")
        data[label] = curve, draws

    print("\nNew: 1960–2019 minus 1900–1959 (rates in mm/yr; means across 100 paired contrasts)")
    print("model    fitted_change   SE(ddof=0)    one-sided_p    stored_mean    recovered_mean")
    for label, (curve, draws) in data.items():
        delta, se, p, stored, recovered = compare(curve, draws, 1900, 1960, 60)
        print(f"{label:7}  {delta:12.6f}  {se:11.6f}   {p:12.8g}   {stored:12.6f}   {recovered:12.6f}")


if __name__ == "__main__":
    main()
