"""Run the frozen uniform-grid integration study from the project root."""

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import shlex
import subprocess
import sys


RESEARCH = Path("research")
RUN = RESEARCH / "run.json"
REFERENCE = 1 / 3
TARGET_ORDERS = {"trapezoid": 2, "left": 1}
ORDER_TOLERANCE = 0.01
CONSISTENCY_TOLERANCE = 1e-14
OUTPUTS = [RESEARCH / name for name in ("results.csv", "consistency.csv", "error.svg")]


def quadrature(method, n):
    h = 1 / n
    if method == "trapezoid":
        return math.fsum(
            h * ((i * h) ** 2 + ((i + 1) * h) ** 2) / 2 for i in range(n)
        )
    return math.fsum(h * (i * h) ** 2 for i in range(n))


def write_run(record):
    RUN.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot", action="store_true", help="run only the frozen pilot")
    args = parser.parse_args()
    raw_plan = (RESEARCH / "plan.json").read_bytes()
    digest = hashlib.sha256(raw_plan).hexdigest()
    if (RESEARCH / "plan.sha256").read_bytes() != (digest + "\n").encode("ascii"):
        parser.exit(1, "Frozen plan digest does not match the raw plan bytes.\n")
    plan = json.loads(raw_plan)
    invocation = Path(sys.executable).name
    command = shlex.join([invocation, *sys.argv])

    if args.pilot:
        spec = plan["pilot"]
        n = spec["panels"]
        tolerance = spec["absolute_tolerance"]
        results = {}
        for method, expected_sign in (("trapezoid", 1), ("left", -1)):
            estimate = quadrature(method, n)
            expected = spec[f"expected_{method}"]
            error = estimate - REFERENCE
            results[method] = {
                "estimate": estimate,
                "expected": expected,
                "signed_error": error,
                "expected_error_sign": expected_sign,
                "estimate_matches": abs(estimate - expected) <= tolerance,
                "error_sign_matches": expected_sign * error > 0,
            }
        passed = all(r["estimate_matches"] and r["error_sign_matches"] for r in results.values())
        pilot = {
            "command": command,
            "panels": n,
            "reference": "1/3",
            "absolute_tolerance": tolerance,
            "results": results,
            "passed": passed,
            "exit_code": 0 if passed else 1,
        }
        write_run({
            "status": "blocked" if passed else "failed",
            "reason": "Formal run not yet executed." if passed else "Frozen pilot check failed.",
            "plan_sha256": digest,
            "pilot": pilot,
        })
        print(json.dumps(pilot, ensure_ascii=False))
        return pilot["exit_code"]

    if not RUN.is_file():
        parser.exit(1, "Run the frozen pilot first.\n")
    record = json.loads(RUN.read_text(encoding="utf-8"))
    if (record["status"] != "blocked" or record["plan_sha256"] != digest
            or not record["pilot"]["passed"]):
        parser.exit(1, "Formal run requires a passing pilot for this frozen plan.\n")

    panel_counts = plan["formal_panels"]
    conditions = {
        "integrand": "x^2",
        "interval": "[0,1]",
        "panel_counts": ",".join(map(str, panel_counts)),
        "reference": "1/3",
    }
    plot_command = [sys.executable, "research/plot_errors.py"]
    record.update({
        "command": command,
        "plot_command": shlex.join(plot_command),
        "environment": {"python": sys.version, "device": "CPU", "dependencies": "Python standard library"},
        "arms": [{"id": method, "conditions": conditions} for method in TARGET_ORDERS],
    })

    try:
        measurements = []
        summaries = []
        for method, target_order in TARGET_ORDERS.items():
            previous_error = None
            order = None
            discrepancies = []
            all_signs_match = True
            for n in panel_counts:
                estimate = quadrature(method, n)
                signed_error = estimate - REFERENCE
                abs_error = abs(signed_error)
                order = None if previous_error is None else math.log2(previous_error / abs_error)
                measurements.append((method, n, 1 / n, estimate, signed_error, abs_error, order))
                previous_error = abs_error

                analytical_error = 1 / (6 * n ** 2)
                if method == "left":
                    analytical_error -= 1 / (2 * n)
                discrepancies.append(abs(signed_error - analytical_error))
                all_signs_match &= signed_error * analytical_error > 0

            if order is None:
                raise ValueError("At least two grid sizes are required to compute the final order.")
            max_discrepancy = max(discrepancies)
            consistency_pass = max_discrepancy <= CONSISTENCY_TOLERANCE and all_signs_match
            order_pass = abs(order - target_order) <= ORDER_TOLERANCE
            summaries.append((method, max_discrepancy, all_signs_match, consistency_pass,
                              order, target_order, order_pass))

        for path, columns, rows in (
            (OUTPUTS[0], "method,n,h,estimate,signed_error,abs_error,order", measurements),
            (OUTPUTS[1], "method,max_abs_discrepancy,all_signs_match,consistency_pass,"
             "final_order,target_order,order_pass", summaries),
        ):
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.writer(stream, lineterminator="\n")
                writer.writerow(columns.split(","))
                writer.writerows(rows)
        subprocess.run(plot_command, check=True)
        record["sha256"] = {path.as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in OUTPUTS}
    except Exception as exc:
        record.update(status="failed", reason=f"{type(exc).__name__}: {exc}")
        write_run(record)
        raise

    record.update(status="completed", outputs=[path.as_posix() for path in OUTPUTS])
    del record["reason"]
    write_run(record)
    print("Wrote " + ", ".join(record["outputs"]) + " and research/run.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
