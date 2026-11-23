"""Check a clean rerun and independently recompute the published numbers (Python 3.10+)."""

import csv
import math
from pathlib import Path
import shutil
from statistics import fmean, linear_regression
import subprocess
import sys
import tempfile


def rows(path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def main():
    study = Path(__file__).resolve().parent
    stage = Path(tempfile.mkdtemp(prefix=".penguins-rerun-", dir=study))
    print(f"Clean rerun: {stage} (retained on failure)", flush=True)
    for name in ("run.py", "data/penguins.csv", "research/plan.json", "research/plan.sha256"):
        (stage / name).parent.mkdir(exist_ok=True)
        shutil.copyfile(study / name, stage / name)
    subprocess.run([sys.executable, "run.py"], cwd=stage, check=True)
    for name, key in (("predictions", "row_id"), ("results", "test_year")):
        path = Path("research") / (name + ".csv")
        columns = [k for k in rows(study / path)[0] if k != key]
        cmd = [sys.executable, str(study.parents[1] / "checks/compare.py"), str(study / path), str(stage / path),
               "--id", key, "--atol", "0", "--rtol", "0"]
        for column in columns:
            cmd.extend(["--column", column])
        subprocess.run(cmd, check=True)
    run = Path("research/run.json")
    if (stage / run).read_bytes() != (study / run).read_bytes():
        raise SystemExit("Rerun manifest differs, including output or cohort hashes")

    # Separate path: stdlib centered regression and floating-point means, no run.py import.
    raw = rows(study / "data/penguins.csv")
    eligible = {str(i): (float(r["flipper_length_mm"]), float(r["body_mass_g"]))
                for i, r in enumerate(raw, 1)
                if all(r[k] not in {"NA", ""} for k in ("flipper_length_mm", "body_mass_g"))}
    train_ids = {str(i) for i, r in enumerate(raw, 1) if r["year"] in {"2007", "2008"}}
    test_ids = {str(i) for i, r in enumerate(raw, 1) if r["year"] == "2009"}
    x, y = zip(*(point for i, point in eligible.items() if i in train_ids))
    slope, intercept = linear_regression(x, y)
    baseline = fmean(y)
    predictions = rows(study / "research/predictions.csv")
    test = test_ids.intersection(eligible)
    if len(predictions) != len(test) or {p["row_id"] for p in predictions} != test:
        raise SystemExit("Recorded IDs do not match the complete-case holdout")
    absolute_errors = []
    for p in predictions:
        flipper, mass = eligible[p["row_id"]]
        linear = intercept + slope * flipper
        if (float(p["flipper_length_mm"]), float(p["body_mass_g"])) != (flipper, mass):
            raise SystemExit(f"Held-out measurements differ at row {p['row_id']}")
        for key, value in (("mean_prediction_g", baseline), ("linear_prediction_g", linear)):
            if not math.isclose(float(p[key]), value, rel_tol=0, abs_tol=1e-8):
                raise SystemExit(f"Independent prediction differs at row {p['row_id']}: {key}")
        absolute_errors.append((abs(mass - baseline), abs(mass - linear)))
    mean_mae, linear_mae = map(fmean, zip(*absolute_errors))
    summary, = rows(study / "research/results.csv")
    counts = {"test_year": 2009, "train_total": len(train_ids), "train_used": len(x),
              "train_excluded": len(train_ids) - len(x), "test_total": len(test_ids),
              "test_used": len(test), "test_excluded": len(test_ids) - len(test)}
    estimates = {"slope_g_per_mm": slope, "intercept_g": intercept, "train_mean_g": baseline,
                 "mean_mae_g": mean_mae, "linear_mae_g": linear_mae, "reduction_g": mean_mae - linear_mae}
    for k, v in counts.items():
        if int(summary[k]) != v:
            raise SystemExit(f"Independent count differs: {k}")
    for k, v in estimates.items():
        if not math.isclose(float(summary[k]), v, rel_tol=0, abs_tol=1e-8):
            raise SystemExit(f"Independent estimate differs: {k}")
    print(f"Independent MAE (g): mean={mean_mae:.9f}, linear={linear_mae:.9f}, "
          f"difference={mean_mae-linear_mae:.9f}; checked {len(test)} paired rows")
    shutil.rmtree(stage)


if __name__ == "__main__":
    main()
