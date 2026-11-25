# Does GDP growth mark progress in longevity?

Across 192 reporting economies between 2000 and 2019, a 1.5-fold higher cumulative GDP per capita growth factor was associated with **1.37 more years gained in life expectancy**, conditional on starting income, starting longevity and region (HC3 95% interval: **0.45–2.29**). The association is positive; the evidence does not establish that it exceeds the prespecified six-month benchmark.

**[Read the study](research/paper.md)** · [estimates](research/estimates.csv) · [coverage](research/coverage.csv) · [claim-by-claim evidence](research/claims.json) · [handoff](research/handoff.md).

## Reproduce offline

From an ai4sci checkout with Python 3 and NumPy available, run the following at the checkout root. The release includes the [exact small analytical extract](data/analysis-frame.csv); neither a network connection nor the original packet is required. Reference environment: Linux x86_64, Python 3.11.14, NumPy 2.4.4.

```bash
S=$PWD/examples/transfer-economics
# Choose a NEW directory under an existing writable parent.
bash "$S/replay.sh" "$PWD/economics-replay"
```

The script copies the frozen plan, source notes and analytical inputs, **not** the fitted tables, to the new directory and regenerates both results tables there. The estimator checks the input digest before fitting. [run.json](research/run.json) gives the reference output hashes. Different numerical-library builds can differ at the last reported digit.

To run individual steps from the study root:

```bash
sha256sum -c provenance/frame.sha256
OPENBLAS_NUM_THREADS=1 python3 analyze.py --out research
```

### Verify against the original distribution, if available

Set `PACKET` to the directory containing the original `data.csv` and `WORK` to a separate writable directory. From the study root:

```bash
python3 prepare.py --packet "$PACKET" --out "$WORK/analysis-frame.csv"
cmp data/analysis-frame.csv "$WORK/analysis-frame.csv"
```

The extractor verifies the full panel's [input hash](provenance/inputs.sha256). [Attributions, source URLs, transformations, licenses and column dictionary](provenance/README.md) travel with the extract.
