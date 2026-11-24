# Palmer penguin regression: revision handoff

Read the [Word manuscript](../paper/final.docx), [editable audit copy](paper.md) and [reply](response.md). This worked regression revisits a known holdout; the median rerun does not confirm the result on new birds. Against the training median, the pooled line reduced MAE by 372.361 g. Against the training mean, the original 384.707 g reduction was unchanged.

**What was preserved.** The [original inventory](../original.sha256) pins byte copies of the earlier paper, review, plan, freeze, script, raw input and reference outputs. The full original study remains in `examples/penguins/`. The [supplement plan](plan.json) pins that inventory and states what was already known. The [local freeze time](freeze.utc) precedes the [formal run start](run-start.utc); neither is an external timestamp. The [release provenance](../original/data/PROVENANCE.md) includes data credits and licensing.

**What ran.** The [run receipt](run.json) pins the script, plan, results and paired predictions. Each arm shares the input and ordered training and test ID digests (one ASCII row number plus LF per record). The [result row](results.csv) reports grams; [paired predictions](predictions.csv) use one-based CSV data-row IDs. The [ledger](claims.json) binds the manuscript values to the summary. [File digests](../artifacts.sha256) cover the author-stage artifacts.

## Commands and receipts

From the checkout root, with CPython 3.11.14 and Pandoc 3.1.11.1:

```sh
study=examples/penguins-revision
mkdir -p "$study/.scratch"
export TMPDIR="$PWD/$study/.scratch" PYTHONDONTWRITEBYTECODE=1
python3 ai4sci.py freeze examples/penguins-revision
(cd "$study" && sha256sum --check original.sha256)
(cd "$study" && python3 run.py)
(cd "$study" && python3 replay.py)
(cd "$study" && python3 render.py)
python3 ai4sci.py audit examples/penguins-revision
```

All returned 0 at the author stage. Freeze ran before scoring; repeating it checks the same bytes. Raw stdout: [freeze](freeze.stdout), [formal run](run.stdout), [clean replay](replay.stdout), [study audit](audit.stdout). Replay regenerated both CSVs and the receipt byte for byte and compared all common predictions and scores with the archived versions. The audit verified all eight marked claims and eight planned cells with no errors. It checked local evidence, not scientific interpretation or the rendering. No TeX engine was found on PATH; Pandoc generated the editable DOCX directly.

**Review boundary.** Reproduction and the recorded audit above are author checks. The archived review concerns only the original study. The coordinator owns independent review of the revision and the delivery manifest; neither an author approval nor a submission decision is implied by this handoff.
