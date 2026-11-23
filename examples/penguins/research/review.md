# Independent review: 2009 Palmer penguin holdout

**Finding.** On the same 119 eligible records from 2009, the pooled flipper-length model reduced mean absolute error (MAE) by **384.707 g** relative to predicting the training mean. I independently recovered every saved prediction and both MAEs. The run is complete. Claims C1–C6 and the manuscript's interpretation are supported for this holdout. I found no blocker to reporting this descriptive result.

I did not author the analysis. I read the plan, manuscript and reported results before recalculation, so this was a retrospective, nonblind check. The [plan](plan.json) discloses prior knowledge of the published association. Its SHA-256 matches the frozen digest, which establishes agreement with the stored plan, not when the authors first saw the scores.

## Source and attribution (C1–C2)

I compared the vendored CSV and license byte for byte with the files at the GitHub commit identified by the [v0.1.0 tag](https://api.github.com/repos/allisonhorst/palmerpenguins/git/ref/tags/v0.1.0). The CSV is 15,241 bytes with SHA-256 `f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93`. The [release data dictionary](https://raw.githubusercontent.com/allisonhorst/palmerpenguins/e5bfd5f2c7da95b0823e9501b9013eb2ef124fa7/man/penguins.Rd) identifies adult foraging penguins near Palmer Station and gives the units in millimeters and grams. The package credits field collection to Kristen Gorman and Palmer Station LTER. DataCite's three EDI records match the species and accessions in [the provenance record](../data/PROVENANCE.md). The archived package credits Horst, Hill and Gorman. Its license and the package article identify the data as CC0.

I checked both article DOIs against Crossref. The [field paper](https://doi.org/10.1371/journal.pone.0090081) describes taking the measurements. In the [package paper](https://journal.r-project.org/articles/RJ-2022-020/), Figure 4A plots flipper length and body mass with separate lines for the three species. The accompanying text describes an approximately linear pooled trend. Neither citation supplies the holdout errors reported here.

---
## Cohort and predictions (C3–C6)

The pinned CSV contains 110 records from 2007, 114 from 2008 and 120 from 2009. Row 4 (Adélie, 2007) and row 272 (Gentoo, 2009) each lack **both** measurements. Omitting only these two rows leaves 223 of 224 training records and 119 of 120 test records. Seven eligible training records and two test records lack sex and were retained. Both arms' recorded row-ID digests match the reconstructed cohorts.

Starting from the CSV, I calculated the slope from differences between all unordered pairs of training records, using exact rational arithmetic. The intercept is the mean of training mass minus slope times flipper length. The result is a slope of 48.394596264 g/mm, an intercept of −5477.164604778 g and a training mean of 4197.197309417 g. I aligned predictions by original row number and checked both measurements and both predictions on every test row against [predictions.csv](predictions.csv). All agree at the stored nine decimal places.

| Quantity on the same 119 rows | Independent result (g) |
|---|---:|
| Training-mean MAE | 710.455213476 |
| Flipper-length MAE | 325.748479323 |
| Mean paired difference, baseline absolute error minus model absolute error | 384.706734152 |

The paired difference was averaged **before rounding** and agrees with [results.csv](results.csv). As a check on the pooled result, the 52 Adélie, 24 Chinstrap and 43 Gentoo test records contributed mean error reductions of 240.788, 101.179 and 716.996 g, respectively. These use predictions from the same pooled fit. They describe the composition of this holdout, not performance of models fitted separately by species.

---
## Interpretation and verification

The study code fits on the earlier two years using flipper length alone, then scores measured masses in the final year. Both the code and the independent calculation use the arithmetic mean as the baseline. A median would minimize training absolute error among constant predictors, so the result compares the line specifically with the **training mean**. The manuscript limits the result to measured complete cases at the sampled sites and distinguishes pooled prediction from within-species and causal effects. The CSV identifies paired observations by row number, not by a longitudinal bird identifier. The reviewed manuscript contains no study-generated figure.

The following read-only checks ran from the repository root. The independent script does not import or execute the study's `run.py`.

| Command | Exit | Result |
|---|---:|---|
| `python3 -B examples/penguins/research/verify_independent.py` | 0 | Recovered the fitted coefficients, every paired row, the summary table and both cohort-ID hashes. |
| `python3 -B ai4sci.py audit examples/penguins` | 0 | All six marked claims passed the local evidence checks. |

Reviewed manuscript SHA-256: `780b41febeac304dbf77b5a5dfd6860fa7a24df6c3f5cc9cac5a478e34c639dd`.
