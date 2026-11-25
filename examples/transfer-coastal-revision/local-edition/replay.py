"""Reproduce Table R1, period-rates.csv, fitted minimum years and observed gauge-average slopes."""

import argparse
import csv
from pathlib import Path

import numpy as np


PERIODS = {"whole_1900_2019": (1900, 2019), "pre_1900_1959": (1900, 1959),
           "post_1960_2019": (1960, 2019), "late_1970_2019": (1970, 2019)}


def read_csv(path):
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", type=Path, help="v1 inputs staged by ../supplement/load_inputs.py")
    parser.add_argument("output", type=Path, help="write the result table to a new CSV file")
    args = parser.parse_args()
    results = []
    table = ["| v1 GAM | 1900–19 | 1920–39 | 1940–59 | 2000–19 | 1900–2019 | 1900–1959 | 1960–2019 | Post minus pre |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    minima = {}

    for suffix, model in zip("abcd", ("Tr", "TrNc", "TrNcZw", "TrNcPd")):
        curve = read_csv(args.inputs / f"original-curve-{suffix}.csv")
        draws = read_csv(args.inputs / f"original-rate-draws-{suffix}.csv")
        years = np.array([int(r["time"]) for r in curve])
        np.testing.assert_array_equal(years, [int(r["time"]) for r in draws])
        np.testing.assert_array_equal(years, np.arange(1890, 2021))
        trend = np.array([float(r["trend"]) for r in curve])
        rate = np.array([float(r["rate_slr"] or "nan") for r in curve])
        np.testing.assert_allclose(rate[1:-1], 5 * (trend[2:] - trend[:-2]), atol=1e-8)
        valid = np.isfinite(rate)
        np.testing.assert_array_equal(years[valid], np.arange(1891, 2020))
        minima[model] = years[valid][np.argmin(rate[valid])]

        cells = []
        for first in (1900, 1920, 1940, 2000):
            last = first + 19
            window_mean = rate[(years >= first) & (years <= last)].mean()
            cells.append(f"{window_mean:.2f}")

        fit, sims = {}, {}
        for period, (first, last) in PERIODS.items():
            use = (years >= first) & (years <= last)
            trajectories = np.array([[float(draws[j][str(z)]) for z in range(100)]
                                     for j in np.where(use)[0]])
            fit[period] = float(rate[use].mean())
            sims[period] = trajectories.mean(axis=0)

        for label, later in (("post_minus_pre", "post_1960_2019"), ("late_minus_pre", "late_1970_2019")):
            fit[label] = fit[later] - fit["pre_1900_1959"]
            # The same trajectory supplies both window means in each difference.
            sims[label] = sims[later] - sims["pre_1900_1959"]

        for period, value in fit.items():
            ensemble = sims[period]
            center = ensemble.mean()
            raw_lo, raw_hi = np.quantile(ensemble, [0.025, 0.975])
            lower, upper = value + raw_lo - center, value + raw_hi - center
            if period in ("whole_1900_2019", "pre_1900_1959", "post_1960_2019", "post_minus_pre"):
                cells.append(f"{value:.2f} [{lower:.2f}, {upper:.2f}]")
            results.append(dict(model=model, period=period, rate_or_difference_mm_per_yr=value,
                                lower=lower, upper=upper,
                                raw_draw_mean=center, raw_draw_lower=raw_lo, raw_draw_upper=raw_hi,
                                center_offset_draw_minus_fit=center - value,
                                draw_sd=np.std(ensemble, ddof=1), realizations=100))
        table.append("| " + " | ".join([model, *cells]) + " |")

    print("Table R1 (mm/yr)\n\n" + "\n".join(table))
    print("\nYears of minimum fitted rate (1891–2019): "
          + ", ".join(f"{model}: {year}" for model, year in minima.items()))

    # Gauge averages are observed levels (cm); the regression produces a slope in mm/yr.
    gauges = read_csv(args.inputs / "gauge-observations.csv")
    for period, (first, last) in PERIODS.items():
        rows = [r for r in gauges if first <= int(r["time"]) <= last and r["Average"].strip()]
        t = np.array([int(r["time"]) for r in rows])
        obs = np.array([float(r["Average"]) for r in rows])
        slope = float(10 * np.polyfit(t - t.mean(), obs, 1)[0])
        print(f"{period}: observed gauge-average slope {slope:.6f} mm/yr ({len(rows)} years)")

    with args.output.open("x", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)


if __name__ == "__main__":
    main()
