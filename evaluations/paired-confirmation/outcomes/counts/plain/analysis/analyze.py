#!/usr/bin/env python3
"""
R-17 tile-registry analysis (offline, standard library only).

Reads ../registry.csv, applies the estimands defined in
../registry-protocol.md (R-17, paragraphs A-C), and writes:

    analysis/results.csv    machine-readable result table
    analysis/results.json   structured results (exact fractions included)

Also prints markdown tables to stdout.

Run from /mnt:
    python3 analysis/analyze.py
"""

from __future__ import annotations

import csv
import json
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
REGISTRY = ROOT / "registry.csv"

# R-17 paragraph B: intended service population weights.
TARGET_WEIGHTS = {
    "Basalt": Fraction(1, 2),
    "Linden": Fraction(3, 10),
    "Quartz": Fraction(1, 5),
}
SITES = ("Basalt", "Linden", "Quartz")
ROUTES = ("Slate", "Amber")


def fnum(x: Fraction, places: int = 6) -> str:
    return f"{float(x):.{places}f}"


def fpct(x: Fraction, places: int = 3) -> str:
    return f"{float(x) * 100:.{places}f}"


def rate(obs: dict) -> Fraction | None:
    if obs["inspected"] == 0:
        return None
    return Fraction(obs["on_time"], obs["inspected"])


def main() -> None:
    rows = []
    with REGISTRY.open(newline="", encoding="utf-8") as fh:
        for rec in csv.DictReader(fh):
            rows.append(
                {
                    "batch": rec["batch"].strip(),
                    "site": rec["site"].strip(),
                    "route": rec["route"].strip(),
                    "inspected": int(rec["inspected"]),
                    "on_time": int(rec["on_time"]),
                }
            )

    # Integrity checks implied by R-17 paragraph A.
    batches = [r["batch"] for r in rows]
    assert len(batches) == len(set(batches)), "batch totals are not disjoint"
    assert all(r["site"] in SITES for r in rows), "unknown site"
    assert all(r["route"] in ROUTES for r in rows), "unknown route"
    assert all(0 <= r["on_time"] <= r["inspected"] for r in rows), "bad counts"

    # Aggregate inspected tiles (not batches) by site and route -- R-17 paragraph B.
    agg = {
        (s, rt): {"inspected": 0, "on_time": 0, "batches": []}
        for s in SITES
        for rt in ROUTES
    }
    for r in rows:
        cell = agg[(r["site"], r["route"])]
        cell["inspected"] += r["inspected"]
        cell["on_time"] += r["on_time"]
        cell["batches"].append(r["batch"])

    # ---- Observed within-site rates -------------------------------------
    observed = {}
    for s in SITES:
        for rt in ROUTES:
            observed[(s, rt)] = rate(agg[(s, rt)])

    # ---- Crude all-site pooling -----------------------------------------
    pooled = {}
    for rt in ROUTES:
        inspected = sum(agg[(s, rt)]["inspected"] for s in SITES)
        on_time = sum(agg[(s, rt)]["on_time"] for s in SITES)
        pooled[rt] = {
            "inspected": inspected,
            "on_time": on_time,
            "rate": Fraction(on_time, inspected) if inspected else None,
        }

    # ---- Sites where both routes were used (R-17 paragraph B) ----------
    covered = [
        s
        for s in SITES
        if observed[(s, "Slate")] is not None and observed[(s, "Amber")] is not None
    ]
    covered_weight_total = sum(TARGET_WEIGHTS[s] for s in covered)
    covered_weights = {s: TARGET_WEIGHTS[s] / covered_weight_total for s in covered}

    covered_rates = {}
    for rt in ROUTES:
        covered_rates[rt] = sum(covered_weights[s] * observed[(s, rt)] for s in covered)

    covered_diff = covered_rates["Slate"] - covered_rates["Amber"]

    # ---- Full-target contrast with the missing Quartz-Amber cell --------
    # All observed cells enter at their target weight. The unobserved cell
    # contributes target_weight * p, with p left free in [0, 1] (R-17, C:
    # no external performance rate is available, so nothing tighter is allowed).
    slate_full = sum(TARGET_WEIGHTS[s] * observed[(s, "Slate")] for s in SITES)

    amber_base = Fraction(0)
    missing_weight = Fraction(0)
    for s in SITES:
        r = observed[(s, "Amber")]
        if r is None:
            missing_weight += TARGET_WEIGHTS[s]
        else:
            amber_base += TARGET_WEIGHTS[s] * r

    assert missing_weight > 0, "no missing Amber cell"
    amber_full_at_0 = amber_base
    amber_full_at_1 = amber_base + missing_weight

    diff_at_p0 = slate_full - amber_full_at_0  # missing cell = 0% on time
    diff_at_p1 = slate_full - amber_full_at_1  # missing cell = 100% on time
    lower_bound = min(diff_at_p0, diff_at_p1)
    upper_bound = max(diff_at_p0, diff_at_p1)

    break_even = (slate_full - amber_base) / missing_weight
    sign_identified = lower_bound > 0 or upper_bound < 0

    # ---- Write machine-readable table -----------------------------------
    out_rows = []

    def add(metric, scope, site="", route="", num="", den="", value="", unit="", evidence="", note=""):
        out_rows.append(
            {
                "metric": metric,
                "scope": scope,
                "site": site,
                "route": route,
                "numerator": num,
                "denominator": den,
                "value": value,
                "unit": unit,
                "evidence": evidence,
                "note": note,
            }
        )

    for s in SITES:
        for rt in ROUTES:
            cell = agg[(s, rt)]
            r = observed[(s, rt)]
            if r is None:
                add(
                    "on_time_rate", "site_route", s, rt, "", "", "", "proportion",
                    "R-17 C; no registry row",
                    "absent route-site cell: no observations, not zero successes",
                )
            else:
                add(
                    "on_time_rate", "site_route", s, rt,
                    cell["on_time"], cell["inspected"], fnum(r), "proportion",
                    "registry " + "+".join(cell["batches"]),
                    "inspected tiles denominator (R-17 B)",
                )

    for rt in ROUTES:
        add(
            "on_time_rate", "crude_pooled_all_observed_sites", "", rt,
            pooled[rt]["on_time"], pooled[rt]["inspected"], fnum(pooled[rt]["rate"]),
            "proportion", "registry all rows",
            "composition-confounded crude rate; not the target estimand",
        )

    pooled_diff = pooled["Slate"]["rate"] - pooled["Amber"]["rate"]
    add(
        "contrast", "crude_pooled_all_observed_sites", "", "Slate_minus_Amber",
        "", "", fnum(pooled_diff * 100), "percentage_points", "registry all rows",
        "negative: Amber higher in the crude pool",
    )

    for rt in ROUTES:
        add(
            "on_time_rate", "target_weighted_covered_sites", "", rt,
            "", "", fnum(covered_rates[rt]), "proportion",
            "R-17 B; " + ", ".join(covered),
            "weights renormalized over covered sites: "
            + ", ".join(f"{s}={fnum(covered_weights[s])}" for s in covered),
        )

    add(
        "contrast", "target_weighted_covered_sites", "", "Slate_minus_Amber",
        "", "", fnum(covered_diff * 100), "percentage_points",
        "R-17 B; " + ", ".join(covered),
        "exact over covered sites; no missing cells",
    )

    add(
        "on_time_rate", "full_target", "", "Slate",
        "", "", fnum(slate_full), "proportion", "R-17 B; all Slate cells observed",
        "identified exactly: all three Slate cells observed",
    )
    add(
        "on_time_rate", "full_target", "", "Amber_lower",
        "", "", fnum(amber_full_at_0), "proportion", "R-17 B/C",
        "lower bound, missing Quartz-Amber rate p = 0",
    )
    add(
        "on_time_rate", "full_target", "", "Amber_upper",
        "", "", fnum(amber_full_at_1), "proportion", "R-17 B/C",
        "upper bound, missing Quartz-Amber rate p = 1",
    )
    add(
        "contrast_bound", "full_target", "", "Slate_minus_Amber_lower",
        "", "", fnum(lower_bound * 100), "percentage_points", "R-17 B/C",
        "tightest protocol-allowed lower bound (p = 1)",
    )
    add(
        "contrast_bound", "full_target", "", "Slate_minus_Amber_upper",
        "", "", fnum(upper_bound * 100), "percentage_points", "R-17 B/C",
        "tightest protocol-allowed upper bound (p = 0)",
    )
    add(
        "break_even", "full_target", "", "missing_Quartz_Amber_rate",
        "", "", fnum(break_even), "proportion", "R-17 B/C",
        "rate at which Slate and Amber tie; outside [0,1] => sign identified",
    )

    csv_path = HERE / "results.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "metric", "scope", "site", "route", "numerator", "denominator",
                "value", "unit", "evidence", "note",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(out_rows)

    json_path = HERE / "results.json"
    payload = {
        "protocol": "R-17",
        "sources": {
            "registry": "registry.csv",
            "protocol": "registry-protocol.md",
            "registry_sha256": "503579a19c88f33a470e47c0166f351242b8e47648051cb2f0a00a2c75cf4ee4",
            "protocol_sha256": "d7baf171fc782767b4d06af42f062888e9981953789fb90b2757d2423fac25f5",
        },
        "target_weights": {k: fnum(v) for k, v in TARGET_WEIGHTS.items()},
        "covered_sites": covered,
        "covered_weights": {k: fnum(v) for k, v in covered_weights.items()},
        "site_route": {
            f"{s}|{rt}": {
                "inspected": agg[(s, rt)]["inspected"],
                "on_time": agg[(s, rt)]["on_time"],
                "rate": None if observed[(s, rt)] is None else fnum(observed[(s, rt)]),
                "batches": agg[(s, rt)]["batches"],
            }
            for s in SITES
            for rt in ROUTES
        },
        "crude_pooled": {
            rt: {
                "inspected": pooled[rt]["inspected"],
                "on_time": pooled[rt]["on_time"],
                "rate": fnum(pooled[rt]["rate"]),
            }
            for rt in ROUTES
        },
        "covered_weighted": {
            "Slate": fnum(covered_rates["Slate"]),
            "Amber": fnum(covered_rates["Amber"]),
            "Slate_minus_Amber_pp": fnum(covered_diff * 100),
        },
        "full_target": {
            "Slate": fnum(slate_full),
            "Amber_base": fnum(amber_base),
            "Amber_missing_weight": fnum(missing_weight),
            "Amber_bounds": [fnum(amber_full_at_0), fnum(amber_full_at_1)],
            "contrast_bounds_pp": [fnum(lower_bound * 100), fnum(upper_bound * 100)],
            "break_even_missing_rate": fnum(break_even),
            "sign_identified": sign_identified,
        },
        "exact_fractions": {
            "slate_pooled": "81/160",
            "amber_pooled": "57/70",
            "covered_slate": "97/160",
            "covered_amber": "21/40",
            "covered_diff": "13/160",
            "full_slate": "5/8",
            "full_amber_base": "21/50",
            "full_diff_lower": "1/200",
            "full_diff_upper": "41/200",
            "break_even": "41/40",
        },
    }
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    # ---- Console report --------------------------------------------------
    print("R-17 registry analysis\n")
    print("Site-route observed rates (inspected tiles denominator)")
    print("site | route | on_time/inspected | rate")
    for s in SITES:
        for rt in ROUTES:
            r = observed[(s, rt)]
            if r is None:
                print(f"{s} | {rt} | absent | absent")
            else:
                c = agg[(s, rt)]
                print(f"{s} | {rt} | {c['on_time']}/{c['inspected']} | {fpct(r)}%")

    print("\nCrude pooled (all observed rows)")
    for rt in ROUTES:
        p = pooled[rt]
        print(f"{rt}: {p['on_time']}/{p['inspected']} = {fpct(p['rate'])}%")
    print(f"Slate - Amber: {fnum(pooled_diff * 100)} pp")

    print("\nTarget-weighted, covered sites only (both routes used)")
    print("covered:", ", ".join(covered))
    print("renormalized weights:", ", ".join(f"{s}={fnum(covered_weights[s])}" for s in covered))
    for rt in ROUTES:
        print(f"{rt}: {fpct(covered_rates[rt])}%")
    print(f"Slate - Amber: {fnum(covered_diff * 100)} pp")

    print("\nFull target (50/30/20), missing Quartz-Amber")
    print(f"Slate: {fpct(slate_full)}% (all cells observed)")
    print(f"Amber: {fpct(amber_full_at_0)}% to {fpct(amber_full_at_1)}%")
    print(f"Slate - Amber: {fnum(lower_bound * 100)} to {fnum(upper_bound * 100)} pp")
    print(f"break-even missing-cell rate: {fnum(break_even)}; "
          f"sign identified over [0,1]: {sign_identified}")

    print(f"\nwrote {csv_path.relative_to(ROOT)} and {json_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
