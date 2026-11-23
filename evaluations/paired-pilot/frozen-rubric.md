# Frozen independent answer key and rubric

Authored before any model run. Same criteria for both arms; one point per item, no half points. Score only delivered documents and runnable artifacts, never tool sophistication, extra workflow files or an audit exit alone. Missing report means report-dependent items score zero. One pair per task; no inference about average performance. Author subsequently scores unblinded against this key, not an independent human replication. Delta means Slate minus Amber; reversing with explicit orientation and correct signs is equivalent. Numerical tolerance ±0.05 percentage points, or equivalent in proportions. Exact fractions count.

## Tile registry: 10 points

1. All-site pooled rates Amber 114/140 = 81.42857%, Slate 81/160 = 50.625%; both correctly labelled (fractions or rates) and pooled direction favors Amber.
2. Basalt: Amber 6/20 = 30%, Slate 48/120 = 40%. Linden: Amber 108/120 = 90%, Slate 19/20 = 95%. All four labelled; within both covered sites Slate higher. Quartz: Slate 14/20 = 70% and Amber absent (scored in 4).
3. Explains structural reversal via differing site composition (Slate more heavily allocated to low-on-time Basalt, Amber to high-on-time Linden), not just asserts “Simpson”.
4. Correctly identifies missing Amber–Quartz as unobserved, not zero, and Slate–Quartz as 70%.
5. Covered target renormalizes to Basalt 5/8, Linden 3/8; Amber 52.5%, Slate 60.625%, contrast +8.125 percentage points.
6. Full target Slate 62.5%; Amber 42% to 62% from 42% + 20% times unknown Quartz success proportion in [0,1]. Correct endpoints and rationale required.
7. Tight full-target difference +0.5 to +20.5 percentage points; strictly positive sign even though exact magnitude is unidentified. Conditional on observed rates, not an assertion of known population probabilities.
8. Descriptive only, since dispatcher selected routes using queue length; quotes or precisely locates primary protocol rather than treating newsletter as authoritative.
9. Runnable offline analysis read from registry.csv (not hardcoded answers) with a documented command that reproduces the reported machine-readable outputs. Evaluator reruns on copied workspace and checks outputs, not just file existence.
10. Machine-readable table(s) report at least pooled, covered-standardized and full-target bounds corresponding to the report, including clear route/contrast and units.

## Method literature: 8 points

1. CPython `statistics.quantiles` defaults to `exclusive` in the supplied version, citing the implementation signature (or equivalently exact primary locator).
2. CPython interpolates linearly yet uses different placement than `inclusive`; inclusive endpoints are 0th and 100th percentiles, or gives correct m−1 vs m+1 rank mapping.
3. NumPy `percentile` default is `linear`, H&F type 7, with the primary method's version and a locator or excerpt.
4. Rejects guaranteed default equivalence, distinguishes interpolation from rank convention. A valid sample counterexample is welcome but not required.
5. Gives a method-aligned comparison for quartiles (e.g., CPython inclusive and NumPy linear on compatible 1-D data or CPython exclusive and NumPy weibull for ordinary interior quartiles; no unsupported universal equality across small-sample extrapolation or missing-data conventions).
6. Identifies Hyndman and Fan (1996), “Sample quantiles in statistical packages,” as metadata/secondary citation only here, not a read original or evidence for the newsletter's endorsement.
7. Annotated list gives traceable locators (stable link or actual path + version/section for both direct sources plus journal bibliographic identity); no invented quotations/findings or fabricated accessed full text.
8. Delivers reading list only, with no experimental scripts/run, paper, audit or plan; the supplied documents are excluded from this check. Mere explanation/calculation within the list is fine.
