"""Compare numeric columns and/or a clustering partition after exact ID alignment."""

import argparse
from collections import Counter
from fractions import Fraction
import json
from pathlib import Path
import sys
import csv

from common import Findings, number, table


def indexed(path, id_col, fields):
    header, rows = table(path)
    if not {id_col, *fields} <= set(header):
        raise ValueError(f"{path}: missing requested column")
    by_id = {}
    for row in rows:
        rid = row[id_col]
        if not rid.strip() or rid in by_id:
            raise ValueError(f"{path}: blank or duplicate ID {rid!r}")
        by_id[rid] = row
    return by_id


def ari(pairs):
    # Count matching sample pairs without constructing a quadratic pair matrix.
    def pair_count(counts):
        return sum(n * (n - 1) // 2 for n in counts.values())

    both = pair_count(Counter(pairs))
    left = pair_count(Counter(a for a, _ in pairs))
    right = pair_count(Counter(b for _, b in pairs))
    all_pairs = len(pairs) * (len(pairs) - 1) // 2
    numerator = 2 * (all_pairs * both - left * right)
    denominator = all_pairs * (left + right) - 2 * left * right
    return Fraction(numerator, denominator) if denominator else Fraction(1)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected", type=Path)
    parser.add_argument("actual", type=Path)
    parser.add_argument("--id", required=True, dest="id_col")
    parser.add_argument("--column", action="append", default=[])
    parser.add_argument("--atol", default="0")
    parser.add_argument("--rtol", default="0")
    parser.add_argument("--labels", help="compare partitions in this column by adjusted Rand index")
    parser.add_argument("--min-ari", default="1")
    args = parser.parse_args()
    problems = Findings()
    score = None
    count = None
    try:
        fields = args.column + ([args.labels] if args.labels is not None else [])
        if not fields or args.id_col in fields or len(fields) != len(set(fields)):
            raise ValueError("select distinct output column(s), different from the ID")
        atol, rtol, floor = map(number, (args.atol, args.rtol, args.min_ari))
        if min(atol, rtol) < 0 or not -1 <= floor <= 1:
            raise ValueError("invalid tolerance or ARI threshold")
        if args.expected.samefile(args.actual):
            raise ValueError("reference and actual must be distinct files")
        a = indexed(args.expected, args.id_col, fields)
        b = indexed(args.actual, args.id_col, fields)
        if a.keys() != b.keys():
            for rid in sorted(a.keys() - b.keys()):
                problems.add(f"missing ID: {rid}")
            for rid in sorted(b.keys() - a.keys()):
                problems.add(f"extra ID: {rid}")
        else:
            count = len(a)
            pairs = []
            for rid, row in a.items():
                for col in args.column:
                    try:
                        ref, actual = number(row[col]), number(b[rid][col])
                    except ValueError as exc:
                        raise ValueError(f"ID {rid}, column {col}: {exc}") from exc
                    if abs(ref - actual) > atol + rtol * abs(ref):
                        problems.add(f"ID {rid}, {col}: expected {row[col]}, got {b[rid][col]}")
                if args.labels:
                    pair = row[args.labels], b[rid][args.labels]
                    if not all(label.strip() for label in pair):
                        raise ValueError(f"ID {rid}: blank cluster label")
                    pairs.append(pair)
            if pairs:
                index = ari(pairs)
                score = float(index)
                if index < floor:
                    problems.add(f"adjusted Rand index below {args.min_ari}")
        code = int(bool(problems.count))
    except (ValueError, csv.Error, OSError) as exc:
        problems.add(exc)
        code = 2
    print(json.dumps({"result": ("match", "different", "invalid")[code], "aligned_ids": count,
                      "ari": score, "diagnostic_count": problems.count, "diagnostics": problems.messages}))
    return code


if __name__ == "__main__":
    sys.exit(main())
