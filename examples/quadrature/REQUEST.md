# Reproduce a quadrature experiment

How quickly does the error shrink as a uniform grid is refined? This example integrates $x^2$ on $[0,1]$ with the composite trapezoidal and left-endpoint rules. The [plan](research/plan.json) specifies the error each method should have and the tolerance for the comparison. The [paper](research/paper.md) explains the measured rates.

From this directory, run `python3 run.py` with Python 3. It recomputes [the data](research/results.csv), [the error plot](research/errors.svg) and [the run record](research/run.json) using the standard library. It compares existing files byte for byte and stops on a mismatch, leaving the originals in place.

To generate the three files from scratch, copy `run.py` into a new directory and run it there. For an automated comparison with the published files, run `python3 check_repro.py` from a writable copy of this example. The check verifies the frozen plan digest and retains its working directory if a comparison fails.
