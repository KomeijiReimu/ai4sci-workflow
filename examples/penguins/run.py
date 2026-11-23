"""Recreate the two CSV tables and the run manifest; run from the study root."""

import csv
from fractions import Fraction
from hashlib import sha256
import io
import json
from pathlib import Path


def table(header, rows):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def main():
    root = Path("research")
    raw_plan = (root / "plan.json").read_bytes()
    plan_digest = sha256(raw_plan).hexdigest()
    if (root / "plan.sha256").read_bytes() != (plan_digest + "\n").encode():
        raise SystemExit("Plan digest mismatch")
    source = json.loads(raw_plan)["input"]
    data = Path(source["path"]).read_bytes()
    digest = sha256(data).hexdigest()
    if digest != source["sha256"]:
        raise SystemExit("Input digest mismatch")

    groups = {"train": [], "test": []}
    totals = {"train": 0, "test": 0}
    split = {"2007": "train", "2008": "train", "2009": "test"}
    for i, row in enumerate(csv.DictReader(io.StringIO(data.decode("utf-8"))), start=1):
        group = split[row["year"]]
        totals[group] += 1
        x, y = row["flipper_length_mm"], row["body_mass_g"]
        if x not in ("NA", "") and y not in ("NA", ""):
            groups[group].append((i, int(x), int(y)))

    # Pooled ordinary least squares with intercept, using training sums only.
    train, test = groups["train"], groups["test"]
    n = len(train)
    sx = sum(x for _, x, _ in train)
    sy = sum(y for _, _, y in train)
    sxx = sum(x * x for _, x, _ in train)
    sxy = sum(x * y for _, x, y in train)
    slope = Fraction(n * sxy - sx * sy, n * sxx - sx * sx)
    mean = Fraction(sy, n)
    intercept = mean - slope * Fraction(sx, n)

    paired = []
    mean_error = linear_error = Fraction(0)
    for i, x, y in test:
        prediction = intercept + slope * x
        paired.append((i, x, y, f"{float(mean):.9f}", f"{float(prediction):.9f}"))
        mean_error += abs(mean - y)
        linear_error += abs(prediction - y)
    mean_mae, linear_mae = mean_error / len(test), linear_error / len(test)
    estimates = (mean, intercept, slope, mean_mae, linear_mae, mean_mae - linear_mae)
    summary = (2009, totals["train"], n, totals["train"] - n,
               totals["test"], len(test), totals["test"] - len(test),
               *(f"{float(v):.9f}" for v in estimates))
    outputs = {
        "research/predictions.csv": table(
            ("row_id", "flipper_length_mm", "body_mass_g", "mean_prediction_g", "linear_prediction_g"), paired),
        "research/results.csv": table(
            ("test_year", "train_total", "train_used", "train_excluded", "test_total", "test_used", "test_excluded",
             "train_mean_g", "intercept_g", "slope_g_per_mm", "mean_mae_g", "linear_mae_g", "reduction_g"), [summary]),
    }
    conditions = {"input_sha256": digest, "metric": "MAE (g)"}
    for group, rows in groups.items():
        ids = "".join(f"{i}\n" for i, _, _ in rows).encode("ascii")
        conditions[group + "_row_ids_sha256"] = sha256(ids).hexdigest()
    manifest = {
        "status": "completed", "command": "python3 run.py", "plan_sha256": plan_digest,
        "run_py_sha256": sha256(Path(__file__).read_bytes()).hexdigest(), "outputs": list(outputs),
        "sha256": {name: sha256(raw).hexdigest() for name, raw in outputs.items()},
        "arms": [{"id": name, "conditions": conditions} for name in ("training_mean", "flipper_ols")],
    }
    outputs["research/run.json"] = (json.dumps(manifest, indent=2) + "\n").encode()
    for name, raw in outputs.items():
        if Path(name).exists() and Path(name).read_bytes() != raw:
            raise SystemExit(f"Refusing to replace differing artifact: {name}")
    for name, raw in outputs.items():
        if not Path(name).exists():
            with Path(name).open("xb") as f:
                f.write(raw)
    print(outputs["research/results.csv"].decode(), end="")


if __name__ == "__main__":
    main()
