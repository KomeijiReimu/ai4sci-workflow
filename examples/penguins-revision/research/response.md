# Response to the original review

The [reviewer](../original/research/review.md#interpretation-and-verification) did not dispute the original scores or request a new field study. The point was narrower: “A median would minimize training absolute error among constant predictors, so the result compares the line specifically with the **training mean**.”

**Choice of control.** The original Methods compared the line only with the arithmetic mean. The opening paragraph and “Data and methods” now explain why the training median is the added control. The [supplement plan](plan.json) fixed the comparison before the rerun; [predictions](predictions.csv) give each constant and the line on each eligible holdout row. The median minimizes absolute error on the training data, not necessarily on a held-out year.

**Effect on the reported advantage.** The original Results gave the mean and line MAEs; “Holdout errors” retains both and adds the median MAE and its contrast with the line. The [result row](results.csv) gives 710.455, 698.109 and 325.748 g for mean, median and line respectively. The line’s advantage over the median is 372.361 g, smaller than the original 384.707 g advantage over the mean. The [author replay](replay.stdout) matched every archived mean and line prediction, both scores and their signed difference at stored precision. Only the added control changes the size of the comparison.

**Scope.** The original Interpretation noted that the median had not been tested. “Interpretation” replaces that caveat with the observed sensitivity result. The original year split, complete-case selection and pooled-species limitations still apply. The rerun reuses a known holdout; it supplies neither independent confirmation nor evidence about another site, species mix or year.
