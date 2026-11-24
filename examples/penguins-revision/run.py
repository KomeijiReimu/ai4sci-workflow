"""Run from the study root with Python 3.10+. No third-party dependencies."""

import csv
from fractions import Fraction
from hashlib import sha256
import io
import json
from pathlib import Path
from statistics import mean, median


def csv_bytes(header, rows):
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return buf.getvalue().encode()


def run():
    plan = Path("research/plan.json").read_bytes()
    digest = sha256(plan).hexdigest()
    if Path("research/plan.sha256").read_bytes() != (digest + "\n").encode():
        raise SystemExit("Plan differs from freeze")
    inventory = Path("original.sha256").read_bytes()
    if sha256(inventory).hexdigest() != json.loads(plan)["original_inventory_sha256"]:
        raise SystemExit("Archive inventory differs from plan")
    for entry in inventory.decode().splitlines():
        expected, name = entry.split("  ", 1)
        if sha256(Path(name).read_bytes()).hexdigest() != expected:
            raise SystemExit(f"Changed original: {name}")

    data = Path("original/data/penguins.csv").read_bytes()
    train, test = [], []
    split = {"2007": train, "2008": train, "2009": test}
    for i, row in enumerate(csv.DictReader(io.StringIO(data.decode())), 1):
        part = split[row["year"]]
        x, y = row["flipper_length_mm"], row["body_mass_g"]
        if x not in {"", "NA"} and y not in {"", "NA"}:
            part.append((i, int(x), int(y)))

    _, xs, ys = zip(*train)
    xbar = Fraction(sum(xs), len(xs))
    ybar = Fraction(sum(ys), len(ys))
    middle = median(list(map(Fraction, ys)))
    slope = (sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
             / sum((x - xbar) ** 2 for x in xs))

    def fmt(value):
        return f"{float(value):.9f}"

    paired, errors = [], []
    for i, x, y in test:
        estimates = ybar, middle, ybar + slope * (x - xbar)
        paired.append((i, x, y, *map(fmt, estimates)))
        errors.append(tuple(abs(estimate - y) for estimate in estimates))
    e_mean, e_median, e_line = map(mean, zip(*errors))
    summary = (2009, len(train), len(test), *map(fmt, (middle, e_mean, e_median, e_line,
               e_mean - e_line, e_median - e_line)))

    out = {
        "research/predictions.csv": csv_bytes(("row_id", "flipper_length_mm", "body_mass_g",
            "mean_prediction_g", "median_prediction_g", "linear_prediction_g"), paired),
        "research/results.csv": csv_bytes(("test_year", "train_used", "test_used", "train_median_g",
            "mean_mae_g", "median_mae_g", "linear_mae_g", "mean_minus_linear_g", "median_minus_linear_g"), [summary]),
    }
    shared = {"input_sha256": sha256(data).hexdigest(), "metric": "MAE (g)"}
    for name, rows in (("train", train), ("test", test)):
        ids = "".join(f"{i}\n" for i, _, _ in rows).encode()
        shared[name + "_row_ids_sha256"] = sha256(ids).hexdigest()
    receipt = {"status": "completed", "command": "python3 run.py", "plan_sha256": digest,
        "run_py_sha256": sha256(Path(__file__).read_bytes()).hexdigest(), "outputs": list(out),
        "sha256": {k: sha256(v).hexdigest() for k, v in out.items()},
        "arms": [{"id": arm, "conditions": shared} for arm in ("training_mean", "training_median", "flipper_ols")]}
    out["research/run.json"] = (json.dumps(receipt, indent=2) + "\n").encode()
    for name, raw in out.items():
        if Path(name).exists() and Path(name).read_bytes() != raw:
            raise SystemExit(f"Refusing to overwrite different artifact: {name}")
    for name, raw in out.items():
        if not Path(name).exists():
            with Path(name).open("xb") as f:
                f.write(raw)
    print(out["research/results.csv"].decode(), end="")


if __name__ == "__main__":
    run()
