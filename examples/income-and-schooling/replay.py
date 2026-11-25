"""Replay the matched-country and exploratory analyses using the archived WDI values."""

import csv
import math
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
GDP, ENROLLMENT, LIFE = "NY.GDP.PCAP.PP.KD", "SE.SEC.ENRR", "SP.DYN.LE00.IN"


def bootstrap(statistic, n):
    point = statistic(np.arange(n))
    rng = np.random.default_rng(1729)
    draws = np.asarray([statistic(rng.integers(n, size=n)) for _ in range(2000)])
    lower, upper = np.quantile(draws, [0.025, 0.975], axis=0)
    return list(zip(point, lower, upper))


def matched(pairs):
    # Keep the original country order and log of the endpoint-to-start ratio.
    rows = []
    for start, end in pairs:
        x0, x1 = float(start[GDP]), float(end[GDP])
        y0, y1 = float(start[ENROLLMENT]), float(end[ENROLLMENT])
        rows.append((x1, y1, math.log(x1 / x0), y1 - y0))
    x1, y, dx, dy = np.asarray(rows).T
    x = np.log(x1)

    def contrasts(ix):
        level = np.corrcoef(x[ix], y[ix])[0, 1]
        change = np.corrcoef(dx[ix], dy[ix])[0, 1]
        return [level, change, level - change]

    return (bootstrap(contrasts, len(rows)), int((dx > 0).sum()),
            int(((dx > 0) & (dy <= 0)).sum()))


def supplemental(pairs):
    rows = []
    for start, end in pairs:
        x0, y0, l0 = (float(start[key]) for key in (GDP, ENROLLMENT, LIFE))
        x1, y1, l1 = (float(end[key]) for key in (GDP, ENROLLMENT, LIFE))
        rows.append([math.log(x1), y1, math.log(x1 / x0), y1 - y0, l0, l1 - l0])
    values = np.asarray(rows)

    def stats(ix):
        x, y, dx, dy, l0, dl = values[ix].T

        def partial(u, z):
            controls = np.stack([np.ones(len(ix)), dl], axis=1)
            outcomes = np.stack([u, z], axis=1)
            residuals = outcomes - controls @ np.linalg.lstsq(controls, outcomes, rcond=None)[0]
            return np.asarray(np.corrcoef(residuals.T))[0, 1]

        level, change = partial(x, y), partial(dx, dy)
        growth, life0, life_change = [(v - v.mean()) / v.std() for v in (dx, l0, dl)]
        predictors = np.stack([np.ones(len(ix)), growth, life0, growth * life0, life_change], axis=1)
        coef = np.linalg.lstsq(predictors, dy, rcond=None)[0]
        return [np.corrcoef(x, y)[0, 1], np.corrcoef(dx, dy)[0, 1],
                level, change, level - change, coef[3]]

    return bootstrap(stats, len(rows))


def main():
    data = {}
    with (ROOT / "endpoints.csv").open(newline="") as f:
        for row in csv.DictReader(f):
            key = row["iso3"], int(row["year"])
            if key in data or key[1] not in (1995, 2015):
                raise ValueError(f"Unexpected country-year: {key}")
            data[key] = row

    countries = sorted({iso for iso, year in data})
    pairs = [(data[iso, 1995], data[iso, 2015]) for iso in countries
             if (iso, 1995) in data and (iso, 2015) in data]
    pairs = [p for p in pairs if all(row[GDP] and row[ENROLLMENT] for row in p)]
    life_pairs = [p for p in pairs if all(row[LIFE] for row in p)]
    primary, growing, growing_without_gain = matched(pairs)
    adjusted = supplemental(life_pairs)

    coverage = (len(countries), len(pairs), len(life_pairs), growing, growing_without_gain)
    if coverage != (217, 49, 49, 48, 3):
        raise ValueError(f"Coverage or direction counts differ from the paper: {coverage}")
    print(f"{len(pairs)} of {len(countries)} countries matched; {len(life_pairs)} with life expectancy.")
    print(f"GDP rose in {growing}; enrollment did not rise in {growing_without_gain} of them.\n")

    names = ["end_year_levels", "two_endpoint_changes", "levels_minus_changes",
             "sample_unadjusted_level", "sample_unadjusted_change", "partial_level",
             "partial_change", "partial_level_minus_change", "growth_by_baseline_life_interaction_pp"]
    with (ROOT / "estimates.csv").open(newline="") as f:
        reference = list(csv.DictReader(f))
    if [r["estimand"] for r in reference] != names:
        raise ValueError("Reference table does not contain the study estimands in order")
    print(f"{'Estimand':38s}  Estimate  95% bootstrap interval")
    for name, computed, ref in zip(names, primary + adjusted, reference):
        expected = [float(ref[k]) for k in ("estimate", "lower", "upper")]
        np.testing.assert_allclose(computed, expected, atol=1e-10, rtol=0, equal_nan=False, err_msg=name)
        est, lower, upper = computed
        print(f"{name:38s}  {est:8.3f}  [{lower:.3f}, {upper:.3f}]")


if __name__ == "__main__":
    main()
