# Why did two-place prediction save bytes?

Two signed counters increase slowly within each stream, but the combined trace alternates between them. Which previous sample should predict the next one? Once the errors are small, do they repeat often enough to make run packing worthwhile?

| Parent | Change | Payload bytes |
|---|---|---:|
| — | Store values with no predictor | 396 |
| No predictor | Predict from one position back | 512 |
| No predictor | Predict from two positions back | 257 |
| Two positions back | Store runs of identical residual codes | 19 |

The nearest neighbor made the payload **larger**, not smaller. The two-place predictor kept the reference sample in the same stream. The next round held that predictor fixed and tested whether storing runs reduced the payload further. See the [raw byte counts and effective settings](research/bytes.csv) and the [predictions, alternatives and budget for each round](research/branches.json).

The [input trace](research/trace.txt) is synthetic. The counts are actual lengths of encoded byte strings, not simulated runtimes or estimated compression ratios. The [program](run.py) reads and hashes the same trace bytes it uses for the measurement. It maps each signed residual to a nonnegative character code and encodes the resulting string as UTF-8. Run packing emits the run length followed by its code. The decoder knows the lag and packing rule and must reconstruct all 256 values before the encoder reports a size. The table excludes headers. Both rounds reuse the same trace. This demonstrates a branch decision, not independent evidence about real telemetry or a comparison to production compressors.

## Replay and challenge the decision

From the checkout with Python 3.10 or later:

```sh
kit=$PWD
mkdir -p "$kit/.local"
study=$(mktemp -d "$kit/.local/branch-replay.XXXXXX")
mkdir "$study/research"
cp examples/branch-decision/run.py "$study/"
cp examples/branch-decision/research/plan.json "$study/research/"
python3 ai4sci.py freeze "$study"
(cd "$study" && python3 run.py)
diff -ru examples/branch-decision/research "$study/research"
python3 ai4sci.py audit "$study"
```

The program reports `raw=396, adjacent=512, paired=257, runs=19 bytes`. The diff is empty and the audit exits `0`. The [plan](research/plan.json) fixes the baseline and total allowance and requires the branch ledger. Removing `research/branches.json` from a replay makes its audit exit `2` even when all four payload sizes remain correct. The program writes each round's observation, competing predictions and attempt allowance before measuring its children. Those later choices are exploratory. Regenerate this synthetic example in a fresh study as shown above. The program refuses to replace earlier results.

Now change only the first decision **in the replay copy**. The losing sibling still has a valid measurement and the manuscript still cites the correct numbers:

```sh
python3 - "$study/research/branches.json" <<'PY'
import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
tree = json.loads(path.read_text())
tree['rounds'][0]['decision']['selected'] = 'adjacent'
path.write_text(json.dumps(tree, indent=2) + '\n')
PY
python3 ai4sci.py audit "$study"
```

This audit exits `2`. The raw scores support `paired`, not `adjacent`, as the unique improving child. The untouched archive still passes. See [the branch contract](../../checks/branches.md) for a deliberate qualitative follow-up or a round with no winner.
