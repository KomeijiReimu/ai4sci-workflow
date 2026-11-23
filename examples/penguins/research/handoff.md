# Palmer penguins: study handoff

Start with the [paper](paper.md) and the [separate review](review.md). This is a completed, observational prediction demonstration. It compares two prespecified training-only predictors on the same recorded birds, not a physical experiment, new ecological discovery or model leaderboard.

**Result.** Of 224 records from 2007–08, 223 had both flipper length and body mass. Of 120 records from 2009, 119 had both. On those 119 birds, MAE was 710.455213476 g for the training mean and 325.748479323 g for the pooled line. The baseline-minus-linear difference, computed before decimal formatting, was 384.706734152 g. The comparison is limited to complete cases, the observed species mix and that held-out year.

## Evidence map

- [Frozen plan](plan.json) and [digest](plan.sha256): the split, missing-data rule, paired arms, outcome, direction and reproduction tolerances were fixed before fitting or computing holdout scores. The public dataset description and authors' earlier plots were already known. The digest is local, not an external timestamp. No scientific criteria were amended after the run.
- [Provenance](../data/PROVENANCE.md): the unmodified [input CSV](../data/penguins.csv), release-specific Zenodo DOI, pinned Git commit, original EDI accessions, attribution and upstream CC0 license. Raw input SHA-256: `f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93`.
- [Run receipt](run.json): exact command (study-root working directory), script/plan/output hashes and matched conditions. The row-set hashes are SHA-256 over ordered ASCII row numbers with one LF after each ID. After the formal run, the receipt was augmented with the script and plan hashes; both result files were retained and checked byte-for-byte when regenerating the receipt.
- [Predictions](predictions.csv): one row per eligible held-out observation. `row_id=1` is the first data row after the header in the pinned file; this is not an individual tracking tag. [Summary](results.csv): counts, training estimates and paired MAEs. [Claims](claims.json) bind the manuscript to the summary and to the two registered [source excerpts](sources.json).

## Reproduce offline

From the workflow checkout, with Python 3.10+ and its standard library (author run: CPython 3.11.14 on Linux):

```sh
(cd examples/penguins && python3 run.py)
python3 examples/penguins/check_repro.py
python3 ai4sci.py audit examples/penguins
```

All three commands returned **0**. The first checks the plan and input digests before fitting, fills absent outputs and refuses to overwrite differing artifacts. The plan had already been frozen with `python3 ai4sci.py freeze examples/penguins` (exit 0) before the first fit; do not replace it on resume.

`check_repro.py` generates new outputs in a fresh private subdirectory, invokes `checks/compare.py` on **all numeric columns** (`--id row_id` and `--id test_year` respectively, `--atol 0 --rtol 0`), and compares the run receipts. The comparator returned `match` with 119 aligned prediction IDs and `match` with one aligned summary ID (both exit 0, zero diagnostics). The checker then re-read the raw CSV and used `statistics.linear_regression` and `statistics.fmean`, rather than importing the study's rational normal-equation fit. The counts, ID set and measurements matched exactly; every prediction, fitted coefficient and aggregate error matched within the frozen tolerance. It retains its scratch directory if a check fails.

The focused audit reported `scientific_run: completed`, `deliverability: ready`, all six marked claims supported, two source records, no errors and no incomplete reasons. This verifies local bindings, not the meaning of a source or generalizability to other birds. The [review](review.md) is the place to check the scientific interpretation and any reviewer qualifications. A new split, subgroup comparison or stronger baseline would be a separate study, not a reason to change these files.
