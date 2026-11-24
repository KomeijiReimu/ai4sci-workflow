"""Count payload bytes from the signed samples; do not build an encoded file."""

import hashlib
import sys
from collections import Counter
from pathlib import Path


def width(point):
    # Only these two UTF-8 width classes occur on this trace.
    if 0 <= point < 128:
        return 1
    if 128 <= point < 2048:
        return 2
    raise ValueError(f"code point outside the range of this check: {point}")


source = Path(sys.argv[1]).read_bytes()
samples = [int(line) for line in source.splitlines()]
print(f"trace sha256={hashlib.sha256(source).hexdigest()} samples={len(samples)}")

for lag, name in enumerate(("raw", "adjacent", "paired")):
    previous = ([0] * lag + samples) if lag else [0] * len(samples)
    differences = [x - y for x, y in zip(samples, previous)]
    # Folding the sign makes +d map to 2d and -d to 2d-1.
    points = [2 * abs(d) - int(d < 0) for d in differences]
    widths = Counter(map(width, points))
    print(f"{name}: 1-byte symbols={widths[1]} 2-byte symbols={widths[2]} "
          f"payload bytes={widths[1] + 2 * widths[2]}")

    if name == "paired":
        starts = [0] + [i for i in range(1, len(points)) if points[i] != points[i-1]]
        runs = [(end - start, points[start])
                for start, end in zip(starts, starts[1:] + [len(points)])]
        count_bytes = sum(width(length) for length, _ in runs)
        value_bytes = sum(width(value) for _, value in runs)
        print(f"runs (length, code point): {runs}")
        print(f"runs: count bytes={count_bytes} code bytes={value_bytes} "
              f"payload bytes={count_bytes + value_bytes}")

        # Reverse the symbol pairs: first undo packing and sign, then undo prediction.
        signed = [(value // 2 if value % 2 == 0 else -(value // 2) - 1)
                  for length, value in runs for _ in range(length)]
        paired = signed.copy()
        for i in range(2, len(paired)):
            paired[i] += paired[i-2]
        if paired != samples:
            raise ValueError("lag-2 reconstruction does not match input")
        first = next(i for i in range(len(samples)) if signed[i] != paired[i])
        print(f"same unpacked symbols: lag 2 recovers all {len(paired)} samples; "
              f"lag 0 recovers {len(signed)} values but first differs at index {first} "
              f"(zero-based): {signed[first]} instead of {paired[first]}")
