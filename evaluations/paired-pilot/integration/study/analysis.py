#!/usr/bin/env python3
"""Rerunnable analysis for the Iris vs Juniper poster-inspection comparison.

Reads scans.csv (four shift-by-device aggregate rows), computes:
  * device-specific and overall warning proportions with Wilson intervals
  * the overall risk difference with a Newcombe hybrid-score interval
  * the two-sided Fisher exact test for equal overall proportions
  * shift-stratified proportions, Mantel-Haenszel odds ratio (Robins-Breslow-
    Greenland interval) and Cochran-Mantel-Haenszel chi-square test

Outputs research/results.csv and research/tests.csv. Pure Python 3 standard
library; deterministic; no network.
"""

import csv
import math
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCANS = ROOT / "scans.csv"
RESEARCH = ROOT / "research"
Z = 1.959963984540054  # two-sided 95% normal quantile


def read_scans(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        expected = ["shift", "device", "checked", "flagged"]
        if reader.fieldnames != expected:
            raise ValueError(f"unexpected header: {reader.fieldnames!r}")
        rows = []
        for line_no, row in enumerate(reader, start=2):
            try:
                checked = int(row["checked"])
                flagged = int(row["flagged"])
            except (TypeError, ValueError) as exc:
                raise ValueError(f"line {line_no}: counts must be integers") from exc
            if checked <= 0 or flagged < 0 or flagged > checked:
                raise ValueError(f"line {line_no}: invalid counts")
            if not row["shift"].strip() or not row["device"].strip():
                raise ValueError(f"line {line_no}: blank shift or device")
            rows.append({"shift": row["shift"], "device": row["device"],
                         "checked": checked, "flagged": flagged})
    if not rows:
        raise ValueError("scans.csv has no data rows")
    seen = {(r["shift"], r["device"]) for r in rows}
    if len(seen) != len(rows):
        raise ValueError("duplicate shift-by-device row")
    return rows


def wilson(k, n, z=Z):
    p = k / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2.0 * n)) / denom
    half = (z / denom) * math.sqrt(p * (1.0 - p) / n + z * z / (4.0 * n * n))
    return max(0.0, centre - half), min(1.0, centre + half)


def newcombe_diff(k1, n1, k2, n2, z=Z):
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = wilson(k1, n1, z)
    l2, u2 = wilson(k2, n2, z)
    diff = p1 - p2
    lower = diff - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    upper = diff + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return diff, lower, upper


def fisher_two_sided(a, b, c, d):
    """Exact two-sided Fisher test; rows are devices, columns flag status."""
    n1, n2 = a + b, c + d
    m1, m2 = a + c, b + d
    n = n1 + n2
    if min(n1, n2, m1, m2) == 0:
        return 1.0
    denom = math.comb(n, n1)
    lo, hi = max(0, n1 - m2), min(n1, m1)
    probs = {}
    for x in range(lo, hi + 1):
        probs[x] = Fraction(math.comb(m1, x) * math.comb(m2, n1 - x), denom)
    observed = probs[a]
    two_sided = sum(p for p in probs.values() if p <= observed)
    return float(two_sided)


def mh_estimate_and_cmh(strata):
    """strata: list of (a,b,c,d) for Iris flagged/not, Juniper flagged/not."""
    r_sum = Fraction(0)
    s_sum = Fraction(0)
    e_sum = Fraction(0)
    var_sum = Fraction(0)
    a_sum = 0
    for a, b, c, d in strata:
        n = a + b + c + d
        r_sum += Fraction(a * d, n)
        s_sum += Fraction(b * c, n)
        a_sum += a
        e_sum += Fraction((a + b) * (a + c), n)
        var_sum += Fraction((a + b) * (c + d) * (a + c) * (b + d), n * n * (n - 1))
    # Robins-Breslow-Greenland variance terms, accumulated on complete sums.
    term1 = Fraction(0)
    term2 = Fraction(0)
    term3 = Fraction(0)
    for a, b, c, d in strata:
        n = a + b + c + d
        term1 += Fraction((a + d) * a * d, n * n)
        term2 += Fraction((a + d) * b * c + (b + c) * a * d, n * n)
        term3 += Fraction((b + c) * b * c, n * n)
    if r_sum == 0 or s_sum == 0:
        odds_ratio = None
        ci = (None, None)
    else:
        odds_ratio = float(r_sum / s_sum)
        variance = (float(term1) / (2 * float(r_sum) ** 2)
                    + float(term2) / (2 * float(r_sum) * float(s_sum))
                    + float(term3) / (2 * float(s_sum) ** 2))
        se = math.sqrt(max(0.0, variance))
        ci = (math.exp(math.log(odds_ratio) - Z * se),
              math.exp(math.log(odds_ratio) + Z * se))
    if var_sum == 0:
        chi2, p_value = 0.0, 1.0
    else:
        chi2 = float((a_sum - e_sum) ** 2 / var_sum)
        p_value = math.erfc(math.sqrt(chi2 / 2.0))
    return odds_ratio, ci, chi2, p_value


def f6(x):
    return "NA" if x is None else f"{x:.6f}"


def main():
    rows = read_scans(SCANS)
    shifts = sorted({r["shift"] for r in rows})
    devices = sorted({r["device"] for r in rows})
    if devices != ["Iris", "Juniper"]:
        raise ValueError(f"expected devices Iris and Juniper, found {devices}")
    for shift in shifts:
        present = {r["device"] for r in rows if r["shift"] == shift}
        if present != set(devices):
            raise ValueError(f"shift {shift!r} lacks both devices")

    by_cell = {(r["shift"], r["device"]): r for r in rows}
    totals = {dev: {"checked": 0, "flagged": 0} for dev in devices}
    for r in rows:
        totals[r["device"]]["checked"] += r["checked"]
        totals[r["device"]]["flagged"] += r["flagged"]

    results = []
    # Total row.
    grand_checked = sum(t["checked"] for t in totals.values())
    grand_flagged = sum(t["flagged"] for t in totals.values())
    lo, hi = wilson(grand_flagged, grand_checked)
    results.append({
        "analysis": "total", "device": "both", "shift": "all",
        "checked": grand_checked, "flagged": grand_flagged,
        "rate": grand_flagged / grand_checked,
        "ci_low": lo, "ci_high": hi,
    })
    # Overall device rows.
    for dev in devices:
        n, k = totals[dev]["checked"], totals[dev]["flagged"]
        lo, hi = wilson(k, n)
        results.append({
            "analysis": "overall", "device": dev, "shift": "all",
            "checked": n, "flagged": k, "rate": k / n,
            "ci_low": lo, "ci_high": hi,
        })
    # Shift-specific rows.
    for shift in shifts:
        for dev in devices:
            r = by_cell[(shift, dev)]
            lo, hi = wilson(r["flagged"], r["checked"])
            results.append({
                "analysis": "shift", "device": dev, "shift": shift,
                "checked": r["checked"], "flagged": r["flagged"],
                "rate": r["flagged"] / r["checked"],
                "ci_low": lo, "ci_high": hi,
            })

    RESULT_FIELDS = ["analysis", "device", "shift", "checked", "flagged",
                     "rate", "ci_low", "ci_high"]
    RESEARCH.mkdir(parents=True, exist_ok=True)
    with (RESEARCH / "results.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        for row in results:
            writer.writerow({
                "analysis": row["analysis"], "device": row["device"],
                "shift": row["shift"], "checked": row["checked"],
                "flagged": row["flagged"], "rate": f6(row["rate"]),
                "ci_low": f6(row["ci_low"]), "ci_high": f6(row["ci_high"]),
            })

    a = totals["Iris"]["flagged"]
    b = totals["Iris"]["checked"] - a
    c = totals["Juniper"]["flagged"]
    d = totals["Juniper"]["checked"] - c
    diff, diff_lo, diff_hi = newcombe_diff(a, a + b, c, c + d)
    fisher_p = fisher_two_sided(a, b, c, d)

    strata = []
    for shift in shifts:
        ri, rj = by_cell[(shift, "Iris")], by_cell[(shift, "Juniper")]
        ai, bi = ri["flagged"], ri["checked"] - ri["flagged"]
        aj, bj = rj["flagged"], rj["checked"] - rj["flagged"]
        strata.append((ai, bi, aj, bj))
    or_mh, or_ci, chi2, cmh_p = mh_estimate_and_cmh(strata)

    tests = [
        {"test": "overall_risk_difference", "estimate": diff,
         "ci_low": diff_lo, "ci_high": diff_hi,
         "statistic": "NA", "df": "NA", "p_value": "NA",
         "method": "Newcombe hybrid-score interval for difference in proportions"},
        {"test": "overall_fisher_exact", "estimate": "NA",
         "ci_low": "NA", "ci_high": "NA",
         "statistic": "NA", "df": "NA", "p_value": f6(fisher_p),
         "method": "Two-sided Fisher exact test on the 2x2 device-by-flag table"},
        {"test": "mh_odds_ratio", "estimate": f6(or_mh) if or_mh is not None else "NA",
         "ci_low": f6(or_ci[0]) if or_ci[0] is not None else "NA",
         "ci_high": f6(or_ci[1]) if or_ci[1] is not None else "NA",
         "statistic": "NA", "df": "NA", "p_value": "NA",
         "method": "Mantel-Haenszel common odds ratio; Robins-Breslow-Greenland interval"},
        {"test": "cmh_test", "estimate": "NA", "ci_low": "NA", "ci_high": "NA",
         "statistic": f6(chi2), "df": "1", "p_value": f6(cmh_p),
         "method": "Cochran-Mantel-Haenszel chi-square without continuity correction"},
    ]
    TEST_FIELDS = ["test", "estimate", "ci_low", "ci_high", "statistic", "df",
                   "p_value", "method"]
    with (RESEARCH / "tests.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=TEST_FIELDS)
        writer.writeheader()
        for row in tests:
            writer.writerow({key: (f6(row[key]) if isinstance(row[key], float) else row[key])
                             for key in TEST_FIELDS})

    print(f"read {len(rows)} rows from {SCANS}")
    print(f"total: {grand_flagged}/{grand_checked}")
    for dev in devices:
        n, k = totals[dev]["checked"], totals[dev]["flagged"]
        print(f"{dev}: {k}/{n} = {k/n:.6f}")
    print(f"risk difference (Iris-Juniper): {diff:.6f} "
          f"[{diff_lo:.6f}, {diff_hi:.6f}]; Fisher two-sided p={fisher_p:.6f}")
    print(f"MH odds ratio: {or_mh:.6f} [{or_ci[0]:.6f}, {or_ci[1]:.6f}]; "
          f"CMH chi2={chi2:.6f}, df=1, p={cmh_p:.6f}")
    print(f"wrote {RESEARCH / 'results.csv'} and {RESEARCH / 'tests.csv'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
