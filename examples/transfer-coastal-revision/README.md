# Dutch coastal sea-level rise: a period-choice revision

**[Read the complete revised manuscript](revised.md)** · [Response to the referee](response.md) · [Exact change locations](changes.md) · [Supplement](supplement/research/paper.md) · [Independent review](independent-review.md)

The manuscript used the supplied data. A [subsequent check of the original v1 notebook](source-method.md) explains the offset in the archived rate trajectories and tests the new period contrast using the original dispersion method.

In each of the four original GAM fits, Dutch coastal sea level rose faster on average in 1960–2019 than in 1900–1959. The fitted differences range from 0.38 to 0.57 mm/yr. This is a statement about fitted curves, not four independent tests. The archived rate trajectories do not center on the fitted rates, and their discrepancy varies through time. Table 3 separates fitted means, unshifted archive distributions and uncertainty **conditional** on transferring the archived scatter to the fitted rates. Under that assumption the ranges include zero for the trend-only and pressure-gradient models; the nodal-only lower limit is just above zero. The two-period comparison cannot date the onset of acceleration.

This is an independent derivative of the 4 October 2022 discussion preprint by Iris Keizer, Dewi Le Bars, Cees de Valk, André Jüling, Roderik van de Wal and Sybren Drijfhout, [doi:10.5194/egusphere-2022-935](https://doi.org/10.5194/egusphere-2022-935). It is **not approved by the original authors**. The returned Markdown preserves the supplied full text extraction, including the unaffected pages and references; it is not a reconstruction of the original figures or PDF layout. [Attribution, changes and license notices](REUSE.md).

## Reproduce or verify

The revised manuscript is included; it does **not** have to be rebuilt to be read. The following are independent checks, run from the directory containing this README:

```sh
python3 check_tables.py
python3 rebuild.py /path/to/supplied/original.md revised.md --check
```

The second check requires the exact editable original, not the PDF (SHA-256 in [changes.md](changes.md)). To reconstruct rather than compare, omit `--check` and select a new destination. All unedited byte ranges come directly from that original.

For the numerical analysis, use the nine v1 scientific CSVs named in the [input manifest](supplement/inputs.json). The `origin` field gives the exact source object and the `sha256` field pins its bytes. With the original author's release at commit `8c4b55df2b88feb4ebaa191f6d3e8bb9a4b8c86b` already available locally, stage the named inputs as shown below. No network access, later release, raw data redistribution or original GAM fitting is required. If the named files are already available, skip the loader and point `COASTAL_INPUTS` at their directory.

```sh
python3 supplement/load_inputs.py /path/to/v1-release /path/to/new-staged-inputs
export COASTAL_INPUTS=/path/to/new-staged-inputs
(cd supplement && python3 analyze.py "$COASTAL_INPUTS" && python3 verify.py "$COASTAL_INPUTS")
python3 /path/to/ai4sci/ai4sci.py audit supplement
```

The analysis and loader use Python’s standard library. Only the separate numerical verification needs NumPy. The audit checks the **supplement**, not the original preprint, the truth of an uncertainty assumption or editorial acceptance. See the [handoff](supplement/research/handoff.md) for the run record, numerical review and limits.
