#!/usr/bin/env python3
"""R-17 registry analysis: Slate vs Amber on-time processing.

Reads ../registry.csv (the only outcome evidence), aggregates inspected tiles
(the protocol's denominator), and reports:
  1. site-route rates
  2. observed all-site pooled rates (naive, ignoring site)
  3. target-weighted comparison on covered sites (both routes used,
     renormalized target weights), per protocol B
  4. full-target contrast bounds given the absent Quartz-Amber cell
     (protocol C: no external rate for the missing combination)

Stdlib only; no network, no installs.
"""
import csv
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.join(HERE, "..", "registry.csv")

# Protocol B: intended service population site weights.
TARGET_WEIGHTS = {"Basalt": 0.50, "Linden": 0.30, "Quartz": 0.20}
ROUTES = ("Slate", "Amber")


def load():
    with open(REGISTRY, newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["inspected"] = int(r["inspected"])
        r["on_time"] = int(r["on_time"])
    return rows


def main():
    rows = load()
    sites = ["Basalt", "Linden", "Quartz"]

    # Aggregate tiles by site-route. Batch totals are disjoint and each tile is
    # inspected once (protocol A), so inspected/on_time add directly.
    agg = {}
    for r in rows:
        key = (r["site"], r["route"])
        insp, ot = agg.get(key, (0, 0))
        agg[key] = (insp + r["inspected"], ot + r["on_time"])

    site_route = []
    for site in sites:
        for route in ROUTES:
            insp, ot = agg.get((site, route), (0, 0))
            rate = (ot / insp) if insp else None
            site_route.append({
                "site": site,
                "route": route,
                "inspected": insp,
                "on_time": ot,
                "rate": rate,
            })

    def rate(site, route):
        insp, ot = agg.get((site, route), (0, 0))
        return ot / insp if insp else None

    # 2. Observed all-site pooled (tiles pooled across sites; ignores target
    #    weights and site composition -- kept only to expose the confound).
    pooled = {}
    for route in ROUTES:
        insp = sum(agg.get((s, route), (0, 0))[0] for s in sites)
        ot = sum(agg.get((s, route), (0, 0))[1] for s in sites)
        pooled[route] = {"inspected": insp, "on_time": ot,
                         "rate": (ot / insp) if insp else None}
    pooled_diff = pooled["Slate"]["rate"] - pooled["Amber"]["rate"]

    # 3. Covered sites: both routes used. Renormalize target weights.
    covered = [s for s in sites
               if rate(s, "Slate") is not None and rate(s, "Amber") is not None]
    wsum = sum(TARGET_WEIGHTS[s] for s in covered)
    covered_weights = {s: TARGET_WEIGHTS[s] / wsum for s in covered}

    def weighted_rate(route, weights, sites_used):
        return sum(weights[s] * rate(s, route) for s in sites_used)

    cov_slate = weighted_rate("Slate", covered_weights, covered)
    cov_amber = weighted_rate("Amber", covered_weights, covered)
    covered_diff = cov_slate - cov_amber

    # 4. Full target. Quartz-Amber rate x is unobserved; protocol C forbids an
    #    external value, so the tightest admissible range is x in [0, 1].
    full_slate = sum(TARGET_WEIGHTS[s] * rate(s, "Slate") for s in sites)
    amber_base = sum(TARGET_WEIGHTS[s] * rate(s, "Amber")
                     for s in sites if rate(s, "Amber") is not None)
    q_weight = TARGET_WEIGHTS["Quartz"]  # weight on the missing cell
    amber_lo = amber_base + q_weight * 0.0
    amber_hi = amber_base + q_weight * 1.0
    # contrast = full_slate - amber; linear decreasing in x
    diff_hi = full_slate - amber_lo   # x = 0
    diff_lo = full_slate - amber_hi   # x = 1
    sign_stable = diff_lo > 0

    result = {
        "source": os.path.relpath(REGISTRY, HERE),
        "denominator": "inspected tiles",
        "target_weights": TARGET_WEIGHTS,
        "site_route": site_route,
        "pooled_all_sites": pooled,
        "pooled_difference_slate_minus_amber": pooled_diff,
        "covered_sites": covered,
        "covered_weights_renormalized": covered_weights,
        "covered_slate": cov_slate,
        "covered_amber": cov_amber,
        "covered_difference_slate_minus_amber": covered_diff,
        "full_target": {
            "slate": full_slate,
            "amber_base_observed_sites": amber_base,
            "amber_quartz_weight": q_weight,
            "amber_bounds": [amber_lo, amber_hi],
            "difference_bounds": [diff_lo, diff_hi],
            "difference_bounds_pp": [diff_lo * 100, diff_hi * 100],
            "sign_stable_positive": sign_stable,
            "missing_cell": "Quartz/Amber",
            "assumption": "Quartz-Amber on-time rate in [0,1]; no external rate (protocol C)",
        },
    }

    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(result, f, indent=2, sort_keys=True)

    # Machine-readable flat table.
    with open(os.path.join(HERE, "results.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["metric", "site", "route", "inspected", "on_time",
                    "rate", "weight", "notes"])
        for sr in site_route:
            w.writerow(["site_route", sr["site"], sr["route"],
                        sr["inspected"], sr["on_time"],
                        "" if sr["rate"] is None else f"{sr['rate']:.6f}",
                        "", "unobserved" if sr["rate"] is None else ""])
        for route in ROUTES:
            p = pooled[route]
            w.writerow(["pooled_all_sites", "all", route, p["inspected"],
                        p["on_time"], f"{p['rate']:.6f}", "",
                        "tile-pooled; confounded by site mix"])
        w.writerow(["covered_weighted", "covered", "Slate", "", "",
                    f"{cov_slate:.6f}",
                    ";".join(f"{s}={covered_weights[s]:.4f}" for s in covered),
                    "Basalt+Linden only"])
        w.writerow(["covered_weighted", "covered", "Amber", "", "",
                    f"{cov_amber:.6f}",
                    ";".join(f"{s}={covered_weights[s]:.4f}" for s in covered),
                    "Basalt+Linden only"])
        w.writerow(["covered_diff", "covered", "Slate-Amber", "", "",
                    f"{covered_diff:.6f}", "", "positive => Slate higher"])
        w.writerow(["full_target", "all", "Slate", "", "",
                    f"{full_slate:.6f}", "1.0000", "fully observed"])
        w.writerow(["full_target_bound", "all", "Amber", "", "",
                    f"{amber_lo:.6f}", "", "Quartz-Amber=0 lower bound"])
        w.writerow(["full_target_bound", "all", "Amber", "", "",
                    f"{amber_hi:.6f}", "", "Quartz-Amber=1 upper bound"])
        w.writerow(["full_target_diff_bound", "all", "Slate-Amber", "", "",
                    f"{diff_lo:.6f}", "", "at Quartz-Amber=1 (tightest low end)"])
        w.writerow(["full_target_diff_bound", "all", "Slate-Amber", "", "",
                    f"{diff_hi:.6f}", "", "at Quartz-Amber=0 (tightest high end)"])

    # Human-readable console summary of the actual run.
    print("R-17 registry analysis (denominator: inspected tiles)")
    print(f"{'site':8} {'route':6} {'insp':>6} {'on_time':>8} {'rate':>8}")
    for sr in site_route:
        rr = "  n/a" if sr["rate"] is None else f"{sr['rate']*100:6.2f}%"
        print(f"{sr['site']:8} {sr['route']:6} {sr['inspected']:6d} "
              f"{sr['on_time']:8d} {rr:>8}")
    print()
    print(f"all-site pooled  Slate {pooled['Slate']['rate']*100:6.2f}%  "
          f"Amber {pooled['Amber']['rate']*100:6.2f}%  "
          f"diff {pooled_diff*100:+6.2f} pp")
    print(f"covered weighted Slate {cov_slate*100:6.2f}%  "
          f"Amber {cov_amber*100:6.2f}%  "
          f"diff {covered_diff*100:+6.2f} pp  "
          f"(weights {', '.join(f'{s}={covered_weights[s]:.3f}' for s in covered)})")
    print(f"full target      Slate {full_slate*100:6.2f}%  "
          f"Amber [{amber_lo*100:.2f}%, {amber_hi*100:.2f}%]  "
          f"diff [{diff_lo*100:+.2f}, {diff_hi*100:+.2f}] pp  "
          f"sign stable positive: {sign_stable}")
    print("wrote results.csv, results.json")


if __name__ == "__main__":
    main()
