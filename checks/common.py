"""Strict input readers shared by the offline checks."""

import csv
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import re


DECIMAL = r"[+-]?(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?"


def number(text):
    text = str(text)
    if len(text) > 100 or not re.fullmatch(DECIMAL, text):
        raise ValueError("expected a finite decimal number")
    try:
        value = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError("invalid decimal number") from exc
    exponent = value.as_tuple().exponent
    if not isinstance(exponent, int) or abs(exponent) > 1000:
        raise ValueError("decimal exponent out of range")
    return Fraction(value)


def table(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.reader(stream, strict=True)
        header = next(reader, [])
        if not header or any(not h.strip() for h in header) or len(set(header)) != len(header):
            raise ValueError("CSV requires nonblank, unique headers")
        rows = []
        for row in reader:
            if len(row) != len(header):
                raise ValueError(f"CSV line {reader.line_num}: wrong field count")
            rows.append(dict(zip(header, row)))
        if not rows:
            raise ValueError("CSV contains no data rows")
        return header, rows


class Findings:
    def __init__(self):
        self.count = 0
        self.messages = []

    def add(self, message):
        self.count += 1
        if len(self.messages) < 20:
            self.messages.append(str(message)[:300])
