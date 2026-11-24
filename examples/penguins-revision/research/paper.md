# Predicting penguin body mass against a training-median baseline

The earlier Palmer penguin analysis compared a line fitted to flipper length with a constant prediction of body mass. The reviewer noted that the mean was not the constant that minimized absolute error on the training data. We kept the mean for comparison and added the training median. The line had the lowest mean absolute error (MAE) on the same held-out records.

## Data and methods

We used the [palmerpenguins release](https://doi.org/10.5281/zenodo.3960218) curated by Horst, Hill and Gorman, from field observations collected by Gorman and Palmer Station LTER. We trained on 2007 and 2008 and scored on 2009. Each record needed a measured flipper length and body mass; missing values in unused fields did not exclude a record.

The training set contained 223 eligible records. [C1]

The holdout contained 119 eligible records. [C2]

We fitted one least-squares line with an intercept across species, predicting mass in grams from flipper length in millimeters. The constant predictors used only training masses. Each held-out record contributed once to each MAE. We calculated differences before rounding. The supplement plan preceded the median rerun, but the original comparison on this holdout was already known.

## Holdout errors

The training median was 4050 g. [C3]

The training mean had an MAE of 710.455 g. [C4]

The training median had an MAE of 698.109 g. [C5]

The flipper-length line had an MAE of 325.748 g. [C6]

Relative to the training mean, the line reduced MAE by 384.707 g. [C7]

Relative to the training median, the line reduced MAE by 372.361 g. [C8]

## Interpretation

The original mean and line predictions were unchanged on every scored record. The median was the better constant here, so using it narrowed the line’s advantage without reversing it. This is a retrospective sensitivity analysis, not confirmation on fresh data. The comparison describes complete records from one year near Palmer Station. Species composition can contribute to the pooled result; it does not establish a within-species or causal effect, or predict accuracy in another year.
