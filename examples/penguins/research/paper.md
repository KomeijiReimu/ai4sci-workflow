# Predicting Palmer penguin body mass from flipper length: a 2009 holdout

**Abstract.** When flipper length is known but body mass is not, does a fitted line give a better estimate than the average mass of previously measured birds? We compared these predictors on the final year of an existing field dataset, fitting both on the two earlier years.

Using measured flipper length reduced mean absolute error by 384.707 g on this test set. [C6]

## Data and question

The source data describe adult foraging penguins near Palmer Station, Antarctica. [C1]

Horst and colleagues plotted flipper length against body mass with separate lines by species. [C2]

Here the task is prediction across years: we fit **one pooled line**, then ask how far its predictions fall from the masses actually recorded the following year. This is a worked analysis of public measurements, not a new field experiment.

## Methods

We used the curated `penguins.csv` from `palmerpenguins` v0.1.0. The [frozen plan](plan.json) reserved 2007–08 for fitting and 2009 for scoring. In each partition we required nonmissing `flipper_length_mm` and `body_mass_g`, whether or not sex or another unused field was missing. There was no imputation. Each eligible row contributed once to both arms; file row numbers identify the pairs in [predictions.csv](predictions.csv).

The baseline was the arithmetic mean of training masses. For the linear model, we minimized the sum of squared deviations of training mass from an intercept plus a slope times measured flipper length. The year determined the split but was not a predictor. Neither model used species, island, bill measurements or sex. No test masses entered fitting or model selection. We scored the mean absolute difference between predicted and recorded mass in grams. The prespecified contrast was baseline MAE minus model MAE, computed before rounding.

## Results

Of 224 training rows, 223 had both measurements and 1 was excluded. [C3]

Of 120 held-out rows, 119 had both measurements and 1 was excluded. [C4]

On the same held-out birds, mean absolute error was 710.455 g for the training mean and 325.748 g for the flipper-length model. [C5]

## Interpretation and limits

These errors describe the observed complete cases, not a random sample from a defined target population. A bird without a measured flipper cannot receive this prediction, and a bird without a measured mass cannot contribute a test error. If measurement availability is related to size, the scored records may not represent the omitted ones.

Pooling Adélie, Chinstrap and Gentoo penguins lets species differences contribute to the prediction. The comparison does not isolate an association within species or establish that changing flipper length changes mass. It also compares against the arithmetic mean, not the median that minimizes training absolute error among constant predictors. A single held-out year in the Palmer Archipelago does not measure performance under a different species mix, elsewhere, or in future years. We therefore give the observed paired contrast without a population confidence interval.

## Sources

- Gorman KB, Williams TD, Fraser WR (2014). *Ecological Sexual Dimorphism and Environmental Variability within a Community of Antarctic Penguins (Genus Pygoscelis).* PLOS ONE. [Original field study](https://doi.org/10.1371/journal.pone.0090081).
- Horst AM, Hill AP, Gorman KB (2020). *palmerpenguins*, v0.1.0. [Archived package release](https://doi.org/10.5281/zenodo.3960218). The [provenance record](../data/PROVENANCE.md) gives the original EDI dataset DOIs, attribution, CC0 notice and exact input checksum.
- Horst AM, Hill AP, Gorman KB (2022). *Palmer Archipelago Penguins Data in the palmerpenguins R Package – An Alternative to Anderson's Irises.* The R Journal. [Package paper](https://doi.org/10.32614/RJ-2022-020).
