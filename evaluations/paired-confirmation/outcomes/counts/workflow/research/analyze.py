#!/usr/bin/env python3
"""Protocol R-17 on-time analysis.

Reads registry.csv from the study root and writes research/results.csv.
Pure Python standard library; exact rational arithmetic; deterministic.
Run from the study root:  python3 research/analyze.py
"""
import csv
from decimal import Decimal, ROUND_HALF_UP
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REGISTRY = ROOT / "registry.csv"
OUTPUT = ROOT / "research" / "results.csv"

SITES = ("Basalt", "Linden", "Quartz")
ROUTES = ("Slate", "Amber")
TARGET = {
    "Basalt": Fraction(1, 2),
    "Linden": Fraction(3, 10),
    "Quartz": Fraction(1, 5),
}


def fmt(value):
    """Six-decimal fixed spelling, or blank for an unobserved value."""
    if value is None:
        return ""
    dec = Decimal(value.numerator) / Decimal(value.denominator)
    return format(dec.quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP), "f")


def read_cells():
    """Combine disjoint batch rows into (site, route) cells."""
    cells, batches = {}, 0
    with REGISTRY.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        expected = {"batch", "site", "route", "inspected", "on_time"}
        if set(reader.fieldnames or ()) != expected:
            raise ValueError(f"unexpected registry columns: {reader.fieldnames}")
        for row in reader:
            batches += 1
            site, route = row["site"], row["route"]
            if site not in SITES or route not in ROUTES:
                raise ValueError(f"unknown site or route: {row}")
            inspected, on_time = int(row["inspected"]), int(row["on_time"])
            if inspected < 0 or not 0 <= on_time <= inspected:
                raise ValueError(f"invalid counts: {row}")
            cell = cells.setdefault((site, route), [0, 0])
            cell[0] += inspected
            cell[1] += on_time
    return cells, batches


def rate(cells, site, route):
    inspected, on_time = cells.get((site, route), (0, 0))
    return None if inspected == 0 else Fraction(on_time, inspected)


def main():
    cells, batches = read_cells()
    total_inspected = sum(v[0] for v in cells.values())
    total_on_time = sum(v[1] for v in cells.values())
    rows = []

    def add(section, estimand, site, route, inspected="", on_time="",
            value=None, lower=None, upper=None, note=""):
        rows.append({
            "section": section,
            "estimand": estimand,
            "site": site,
            "route": route,
            "inspected": inspected,
            "on_time": on_time,
            "value": fmt(value),
            "lower": fmt(lower),
            "upper": fmt(upper),
            "note": note,
        })

    # Observed all-site pooled rates: every inspected tile, regardless of site.
    pooled = {}
    for route in ROUTES:
        inspected = sum(cells.get((s, route), (0, 0))[0] for s in SITES)
        on_time = sum(cells.get((s, route), (0, 0))[1] for s in SITES)
        pooled[route] = Fraction(on_time, inspected)
        add("pooled", "pooled_rate", "ALL", route, inspected, on_time,
            pooled[route], note="all inspected tiles pooled over sites")
    add("pooled", "pooled_contrast", "ALL", "Slate-minus-Amber", value=pooled["Slate"] - pooled["Amber"],
        note="naive marginal difference, not target weighted")
    add("pooled", "overall_rate", "ALL", "Both", total_inspected, total_on_time,
        Fraction(total_on_time, total_inspected), note="all routes and sites")

    # Within-site rates for every observed cell.
    for site in SITES:
        for route in ROUTES:
            inspected, on_time = cells.get((site, route), (0, 0))
            if inspected:
                add("within_site", "site_rate", site, route, inspected, on_time,
                    Fraction(on_time, inspected), note="inspected tiles as denominator")
            else:
                add("within_site", "site_rate", site, route, note="unobserved cell: no observations collected (protocol C)")

    # Covered sites: both routes observed. Renormalize the target weights.
    covered = [s for s in SITES if rate(cells, s, "Slate") is not None and rate(cells, s, "Amber") is not None]
    weight_sum = sum(TARGET[s] for s in covered)
    weights = {s: TARGET[s] / weight_sum for s in covered}
    covered_slate = sum(weights[s] * rate(cells, s, "Slate") for s in covered)
    covered_amber = sum(weights[s] * rate(cells, s, "Amber") for s in covered)
    add("covered_target", "target_rate", "Covered", "Slate", value=covered_slate,
        note="target weights renormalized over " + "+".join(covered))
    add("covered_target", "target_rate", "Covered", "Amber", value=covered_amber,
        note="target weights renormalized over " + "+".join(covered))
    add("covered_target", "target_contrast", "Covered", "Slate-minus-Amber", value=covered_slate - covered_amber,
        note="covered-site target-weighted contrast")

    # Full target: Quartz Amber is unobserved. Bound only over its logical range.
    full_slate = sum(TARGET[s] * rate(cells, s, "Slate") for s in SITES)
    known_amber = sum(TARGET[s] * rate(cells, s, "Amber")
                      for s in SITES if rate(cells, s, "Amber") is not None)
    missing_weight = TARGET["Quartz"]
    amber_low = known_amber
    amber_high = known_amber + missing_weight
    add("full_target", "target_rate", "Full", "Slate", value=full_slate,
        note="50/30/20 target weights; inspected-tile counts are site-weighted")
    add("full_target", "target_rate_bounds", "Full", "Amber", lower=amber_low, upper=amber_high,
        note="missing Quartz Amber rate at zero and one")
    add("full_target", "target_contrast_bounds", "Full", "Slate-minus-Amber",
        lower=full_slate - amber_high, upper=full_slate - amber_low,
        note="tight bounds over missing rate in the unit interval")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    if total_inspected != 300 or total_on_time != 195:
        raise ValueError("registry totals changed")
    if covered != ["Basalt", "Linden"]:
        raise ValueError(f"unexpected covered sites: {covered}")

    print(f"batches={batches} inspected={total_inspected} on_time={total_on_time}")
    print(f"pooled Slate={fmt(pooled['Slate'])} Amber={fmt(pooled['Amber'])} diff={fmt(pooled['Slate'] - pooled['Amber'])}")
    print(f"covered Slate={fmt(covered_slate)} Amber={fmt(covered_amber)} diff={fmt(covered_slate - covered_amber)}")
    print(f"full Slate={fmt(full_slate)} Amber=[{fmt(amber_low)}, {fmt(amber_high)}] diff=[{fmt(full_slate - amber_high)}, {fmt(full_slate - amber_low)}]")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
