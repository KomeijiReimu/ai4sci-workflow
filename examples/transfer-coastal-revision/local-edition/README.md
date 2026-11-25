# How much faster did sea level rise along the Dutch coast?

**[Read the full edited preprint](revised.md)** · [Local reply to Anonymous Referee #1, 25 November 2026](response.md) · [Period rates, contrasts and bounds](period-rates.csv)

The referee asked to see longer periods alongside the original 20-year comparisons. In all four model fits, the mean rate in **1960–2019** was higher than in **1900–1959**. For the trend-only fit, the rate rose from 1.82 to 2.26 mm/yr, a difference of **0.44 mm/yr**. Its conditional sensitivity band (−0.26 to 1.06 mm/yr) also allows a decrease. The four specifications describe the same six gauges; they are not four independent tests, and the fixed split cannot date the onset of acceleration.

## Reading the comparison

Table R1 averages the original authors’ annual fitted rates. The long-window differences range from 0.38 to 0.57 mm/yr. Omitting the 1960s from the later period gives differences of 0.52 to 0.75 mm/yr. Each difference pairs the earlier and later means within the same archived trajectory. For the trend-only fit, for example, the 100 trajectories average **4.04 mm/yr** over 1900–2019, whereas the fitted curve averages **2.04 mm/yr**. Taking raw percentiles as bounds for the fitted rate would confuse these two quantities.

For the new bands, the calculation shifts each model’s 100 period means (or paired differences) so their mean equals the fitted result, then takes the 2.5th and 97.5th percentiles. This describes the spread *if* the trajectories’ variability applies to the fitted rates. For the later-minus-earlier contrast, the bands include zero for the trend-only (Tr) and pressure-gradient (TrNcPd) fits. They lie above zero for the nodal-tide (TrNc) and zonal-wind (TrNcZw) fits; the TrNc lower bound is just 0.025 mm/yr. These are sensitivity bands, not calibrated confidence intervals.

The four left-hand columns in Table R1 give the recomputed fitted means for the original 20-year windows. The note beneath the table quotes the preprint’s own short-window brackets for TrNcZw; those brackets, the pointwise Figure 4 bands and the Table 2 tests are the original authors’ results. The new sensitivity bands apply only to the four right-hand columns. This revision did not refit the GAMs or calculate new p-values.

## Reproduce from the v1 archive

Download and unpack the [original KNMI release at the revision used](https://github.com/KNMI-sealevel/NetherlandsSeaLevelAcceleration/archive/8c4b55df2b88feb4ebaa191f6d3e8bb9a4b8c86b.zip). From the directory containing this README, run the following with Python 3 and NumPy (tested with Python 3.11.14 and NumPy 2.4.4):

```sh
release=/path/to/unpacked/NetherlandsSeaLevelAcceleration-8c4b55df2b88feb4ebaa191f6d3e8bb9a4b8c86b
work=$(mktemp -d "$HOME/dutch-coast.XXXXXXXX")
python3 ../supplement/load_inputs.py "$release" "$work/inputs"
python3 replay.py "$work/inputs" "$work/period-rates.csv"
cmp period-rates.csv "$work/period-rates.csv"
```

The [shared loader](../supplement/load_inputs.py) checks the nine scientific input files against the [source URLs and checksums](../supplement/inputs.json). The replay prints the combined Table R1, the year of minimum fitted annual rate for each model, and the observed gauge-average slopes (whole period: 1.92 mm/yr). It writes 24 full-precision rows for the longer windows and contrasts, including raw trajectory centers and percentiles. `cmp` is silent on a byte-for-byte match.

## Authorship and reuse

**Original study:** Iris Keizer, Dewi Le Bars, Cees de Valk, André Jüling, Roderik van de Wal and Sybren Drijfhout, [discussion preprint, 4 October 2022](https://doi.org/10.5194/egusphere-2022-935). **Comment:** [Anonymous Referee #1, General Comments, second bullet](https://doi.org/10.5194/egusphere-2022-935-RC1). The editable text extraction preserves the original page labels and references; see the [source PDF](https://egusphere.copernicus.org/preprints/2022/egusphere-2022-935/egusphere-2022-935.pdf) for figures, layout and mathematical typography.

**Local revision, 25 November 2026:** Qwen3-4B, running locally on CPU, selected the central 95% coverage and drafted the revised passages and referee reply. The coordinator supplied the comparison windows, paired-trajectory method and gauge check; implemented the calculations, assembled the tables and edits, and corrected factual wording. This independent edition changes the title, abstract, period methods, results and interpretation. It is not a reply from the original authors or a publisher-issued revision.

The preprint is © its authors, 2022. The manuscript adaptation and response are shared under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). The numerical summaries derive from the KNMI-sealevel release ([BSD 3-Clause notice](../supplement/LICENSE-KNMI.txt)); PSMSL and Rijkswaterstaat supplied the underlying gauge observations. See the [shared source and license credits](../REUSE.md) for data attribution and the helper-code license.
