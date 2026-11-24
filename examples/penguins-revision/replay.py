"""Author replay: generate outputs from scratch and compare with both versions."""

import csv
from hashlib import sha256
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def read_rows(path):
    with open(path, newline="", encoding="utf8") as f:
        return list(csv.DictReader(f))


def main():
    scratch = Path(".scratch")
    scratch.mkdir(exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix="replay-", dir=scratch))
    print("Replay workspace (retained on failure):", stage, flush=True)
    shutil.copytree("original", stage / "original")
    (stage / "research").mkdir()
    for name in ("run.py", "original.sha256", "research/plan.json", "research/plan.sha256"):
        shutil.copyfile(name, stage / name)
    subprocess.run([sys.executable, "run.py"], cwd=stage, check=True)
    for name in ("research/predictions.csv", "research/results.csv", "research/run.json"):
        raw = Path(name).read_bytes()
        if (stage / name).read_bytes() != raw:
            raise SystemExit(f"Replay differs: {name}")
        print(f"Byte match {name}: {sha256(raw).hexdigest()}")
    old_rows = read_rows("original/research/predictions.csv")
    new_rows = read_rows("research/predictions.csv")
    projected = [{key: row[key] for key in old_rows[0]} for row in new_rows]
    if old_rows != projected:
        raise SystemExit("Original IDs, measurements or predictions differ")
    old, = read_rows("original/research/results.csv")
    new, = read_rows("research/results.csv")
    for key in ("test_year", "train_used", "test_used", "mean_mae_g", "linear_mae_g", "reduction_g"):
        if old[key] != new["mean_minus_linear_g" if key == "reduction_g" else key]:
            raise SystemExit(f"Original summary differs: {key}")
    print(f"Archive match: all {len(old_rows)} ordered IDs, measurements and both original predictions;")
    print("year, cohort sizes, both original MAEs and mean-minus-line contrast match at stored precision.")
    shutil.rmtree(stage)


if __name__ == "__main__":
    main()
