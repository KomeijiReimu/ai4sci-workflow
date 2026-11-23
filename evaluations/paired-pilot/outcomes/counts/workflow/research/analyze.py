#!/usr/bin/env python3
"""Recompute protocol R-17 on-time tile rates from registry.csv.

Run from the study root:  python3 research/analyze.py

Reads the local registry and the signed protocol, uses inspected tiles as the
denominator, and writes research/results.csv. No network or extra data.
"""
from __future__ import annotations

import csv
import re
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry.csv"
PROTOCOL = ROOT / "registry-protocol.md"
OUT = ROOT / "research" / "results.csv"

ROUTES = ("Slate", "Amber")
FIELDS = ["metric_id", "scope", "site", "route", "n_inspected", "n_on_time",
          "rate", "share", "weight", "lower", "upper", "note"]


def dec(x: Fraction) -> str:
    """Compact decimal string, exact to 12 significant digits."""
    return format(float(x), ".12g")


def read_registry():
    cells: dict[tuple[str, str], list[int]] = {}
    with REGISTRY.open(encoding="utf-8", newline="") as stream:
        for i, row in enumerate(csv.DictReader(stream), start=2):
            site, route = row["site"].strip(), row["route"].strip()
            if route not in ROUTES:
                raise ValueError(f"{REGISTRY}:{i}: unknown route {route!r}")
            n, k = int(row["inspected"]), int(row["on_time"])
            if n <= 0 or not 0 <= k <= n:
                raise ValueError(f"{REGISTRY}:{i}: invalid tile counts")
            cell = cells.setdefault((site, route), [0, 0])
            cell[0] += n
            cell[1] += k
    return cells


def read_weights():
    text = PROTOCOL.read_text(encoding="utf-8")
    match = re.search(
        r"(\d+) percent Basalt, (\d+) percent Linden and (\d+) percent Quartz", text)
    if not match:
        raise ValueError("protocol: target weights not found in paragraph B")
    names = ("Basalt", "Linden", "Quartz")
    weights = {name: Fraction(int(value), 100)
               for name, value in zip(names, match.groups())}
    if sum(weights.values()) != 1:
        raise ValueError("protocol target weights do not sum to one")
    return weights


def rate(cell) -> Fraction:
    n, k = cell
    return Fraction(k, n)


def row(metric_id, scope, site="", route="", cell=None, rate_value=None,
        share=None, weight=None, lower=None, upper=None, note=""):
    return {
        "metric_id": metric_id,
        "scope": scope,
        "site": site,
        "route": route,
        "n_inspected": "" if cell is None else cell[0],
        "n_on_time": "" if cell is None else cell[1],
        "rate": "" if rate_value is None else dec(rate_value),
        "share": "" if share is None else dec(share),
        "weight": "" if weight is None else dec(weight),
        "lower": "" if lower is None else dec(lower),
        "upper": "" if upper is None else dec(upper),
        "note": note,
    }


def main():
    cells = read_registry()
    weights = read_weights()
    sites = list(weights)
    unknown = {site for site, _ in cells} - set(sites)
    if unknown:
        raise ValueError(f"registry contains sites outside the target: {sorted(unknown)}")

    observed = [s for s in sites if any((s, r) in cells for r in ROUTES)]
    covered = [s for s in sites if all((s, r) in cells for r in ROUTES)]
    missing = [(s, r) for s in sites for r in ROUTES if (s, r) not in cells]
    if missing != [("Quartz", "Amber")]:
        raise ValueError(f"unexpected missing cells: {missing}")

    out = []
    for site in sites:
        for route in ROUTES:
            key = (site, route)
            if key in cells:
                out.append(row(f"site_{site.lower()}_{route.lower()}", "site", site,
                               route, cells[key], rate(cells[key]),
                               weight=weights[site],
                               note="inspected tiles summed across disjoint batches"))
            else:
                out.append(row(f"site_{site.lower()}_{route.lower()}", "site", site,
                               route, note="absent cell: no observations (protocol C)"))

    pooled = {}
    for route in ROUTES:
        cell = [sum(c[0] for (s, r), c in cells.items() if r == route),
                sum(c[1] for (s, r), c in cells.items() if r == route)]
        pooled[route] = cell
        out.append(row(f"pooled_{route.lower()}", "all_sites_pooled", "All observed",
                       route, cell, rate(cell),
                       note="pooled over observed sites only; site mix is not the target mix"))

    for site in sites:
        for route in ROUTES:
            if (site, route) in cells:
                share = Fraction(cells[(site, route)][0], pooled[route][0])
                out.append(row(f"mix_{route.lower()}_{site.lower()}", "site_mix", site,
                               route, share=share,
                               note=f"share of {route} inspected tiles at {site}"))

    covered_total = sum(weights[s] for s in covered)
    covered_weights = {s: weights[s] / covered_total for s in covered}
    for site in covered:
        out.append(row(f"covered_weight_{site.lower()}", "covered_site_weight", site,
                       weight=covered_weights[site],
                       note="target weight renormalized over covered sites"))

    covered_rates = {}
    for route in ROUTES:
        covered_rates[route] = sum(covered_weights[s] * rate(cells[(s, route)])
                                   for s in covered)
        out.append(row(f"covered_weighted_{route.lower()}", "covered_target_weighted",
                       "Covered sites", route, rate_value=covered_rates[route],
                       note="target weights renormalized over Basalt and Linden"))

    covered_contrast = covered_rates["Slate"] - covered_rates["Amber"]
    out.append(row("covered_contrast", "covered_target_weighted", "Covered sites",
                   "Slate minus Amber", rate_value=covered_contrast,
                   note="renormalized target-weighted descriptive contrast"))

    full = {}
    for route in ROUTES:
        full[route] = sum(weights[s] * rate(cells[(s, route)]) for s in sites
                          if (s, route) in cells)
    out.append(row("full_slate", "full_target_weighted", "All target sites", "Slate",
                   rate_value=full["Slate"], lower=full["Slate"], upper=full["Slate"],
                   note="all Quartz Slate observed"))

    amber_partial = sum(weights[s] * rate(cells[(s, "Amber")]) for s in sites
                        if (s, "Amber") in cells)
    amber_low, amber_high = amber_partial, amber_partial + weights["Quartz"]
    out.append(row("full_amber", "full_target_weighted", "All target sites", "Amber",
                   lower=amber_low, upper=amber_high,
                   note="Quartz Amber unobserved; bound uses rate in [0, 1] only"))

    contrast_low = full["Slate"] - amber_high
    contrast_high = full["Slate"] - amber_low
    out.append(row("full_contrast", "full_target_weighted", "All target sites",
                   "Slate minus Amber", lower=contrast_low, upper=contrast_high,
                   note="tightest bounds allowed by protocol paragraphs B and C"))

    parity = (full["Slate"] - amber_partial) / weights["Quartz"]
    out.append(row("parity_quartz_amber_rate", "threshold", "Quartz", "Amber",
                   rate_value=parity,
                   note="Quartz Amber rate needed for full-target parity"))
    out.append(row("quartz_amber_permitted", "permitted_range", "Quartz", "Amber",
                   lower=Fraction(0), upper=Fraction(1),
                   note="protocol C supplies no external rate; rate must lie in [0, 1]"))

    with OUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(out)
    print(f"wrote {OUT.relative_to(ROOT)} ({len(out)} rows)")
    print(f"pooled Slate {pooled['Slate'][1]}/{pooled['Slate'][0]} = {dec(rate(pooled['Slate']))}")
    print(f"pooled Amber {pooled['Amber'][1]}/{pooled['Amber'][0]} = {dec(rate(pooled['Amber']))}")
    print(f"covered weighted: Slate {dec(covered_rates['Slate'])}, "
          f"Amber {dec(covered_rates['Amber'])}, diff {dec(covered_contrast)}")
    print(f"full-target contrast bounds: [{dec(contrast_low)}, {dec(contrast_high)}]")
    print(f"parity Quartz Amber rate: {dec(parity)}")


if __name__ == "__main__":
    main()
