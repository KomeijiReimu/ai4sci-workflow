#!/usr/bin/env bash
# Reproduce a standalone study from its inputs; never copy the fitted tables.
set -euo pipefail
study=$(cd "$(dirname "$0")" && pwd)
target=${1:?usage: bash replay.sh NEW_DIRECTORY}
mkdir -- "$target"  # refuses an existing path
dest=$(cd "$target" && pwd)
mkdir "$dest/research"
cp -R "$study/data" "$study/provenance" "$dest/"
cp "$study/"{prepare.py,analyze.py,replay.sh,README.md} "$dest/"
cp "$study/research/"{plan.json,plan.sha256,run.json,paper.md,handoff.md,claims.json,sources.json,independent-review.md} "$dest/research/"
(
  cd "$dest"
  export OPENBLAS_NUM_THREADS=1
  python3 analyze.py --out research
)
