# Poster print-inspection warning rates for Iris and Juniper

## Summary

Using the four logged shift-by-device rows in `scans.csv`, the crude print-inspection warning rate was identical for Iris and Juniper. Neither the overall exact test nor the shift-stratified sensitivity analysis indicated an association between device and warning. Because only ten flags were logged and device allocation was not randomized, this is a descriptive null result rather than evidence of equivalence or a causal device effect.

## Question

Among the logged poster inspections in `scans.csv`, did Iris have a different overall print-inspection warning rate from Juniper? The comparison is observational: the log records which device inspected each poster, but it does not arise from an experiment that assigned posters or technicians to devices.

## Data and methods

`scans.csv` contains four aggregate rows, one for each shift-by-device combination, with `checked` inspections and `flagged` inspections. Each poster appears in exactly one row. The unit of analysis is a logged poster inspection; `checked` is the denominator and `flagged` the numerator. There are no missing counts and no duplicate shift-by-device rows.

The outcome is defined by the primary record, `field-note.md`: a flag is a print-inspection warning, not a confirmed defect. The same record states that technicians assigned devices by availability, without randomization. These two facts bound the interpretation: the analysis describes logged warnings under the observed allocation, not defect rates under a randomized device comparison.

The primary analysis compares the overall warning proportion for Iris with that for Juniper. It reports counts, proportions, Wilson 95% confidence intervals for each proportion, the risk difference (Iris minus Juniper) with a Newcombe hybrid-score 95% interval, and a two-sided Fisher exact test of equal proportions. The prespecified sensitivity analysis stratifies by shift, reporting shift-specific proportions, the Mantel-Haenszel common odds ratio with a Robins-Breslow-Greenland 95% interval, and the Cochran-Mantel-Haenszel chi-square test with one degree of freedom and no continuity correction. Tests are interpreted two-sided at the 0.05 level. No subgroup search or model selection was performed.

The analysis plan was written to `research/plan.json` and frozen with the workflow before the formal computation; the frozen digest is recorded in `research/plan.sha256`. The plan is retrospective in the limited sense that the four data rows and the field note had already been read when it was written, and this is disclosed in the plan. The analysis is deterministic and uses only the Python 3.13.5 standard library. The script is `analysis.py`; it writes `research/results.csv` and `research/tests.csv`.

## Results

Table 1 gives the logged counts and crude warning proportions. The two devices have the same overall proportion: four flags among 80 Iris inspections and six flags among 120 Juniper inspections, or 0.05 in each case. The total is ten flags among 200 inspections.

**Table 1.** Logged inspections, warning flags and crude warning proportions.

| Group | Checked | Flagged | Proportion | Wilson 95% interval |
|---|---:|---:|---:|---:|
| All inspections | 200 | 10 | 0.050 | 0.027 to 0.090 |
| Iris, overall | 80 | 4 | 0.050 | 0.020 to 0.122 |
| Juniper, overall | 120 | 6 | 0.050 | 0.023 to 0.105 |
| Iris, dawn | 20 | 3 | 0.150 | 0.052 to 0.360 |
| Juniper, dawn | 40 | 2 | 0.050 | 0.014 to 0.165 |
| Iris, dusk | 60 | 1 | 0.017 | 0.003 to 0.089 |
| Juniper, dusk | 80 | 4 | 0.050 | 0.020 to 0.122 |

Across 200 logged inspections there were 10 warning flags; Iris recorded 4 among 80 and Juniper 6 among 120, and both overall warning rates were 0.05. [C1]

The overall risk difference (Iris minus Juniper) was 0.0, with a Newcombe interval from -0.0627 to 0.0765, and the two-sided Fisher exact test gave p=1.0. [C2]

The shift-specific proportions do not point in a single direction: Iris was higher at dawn and lower at dusk, while Juniper was at 0.05 in both shifts. The stratified summary is correspondingly close to the null.

Within shifts, the warning rate was 0.15 for Iris and 0.05 for Juniper at dawn, and 0.0167 for Iris and 0.05 for Juniper at dusk; the Mantel-Haenszel odds ratio was 1.0846 with interval 0.3033 to 3.8777, and the Cochran-Mantel-Haenszel p-value was 0.8984. [C3]

## Discussion

The answer to the study question is that the logged data show no difference in the overall warning rate: the observed proportions are equal, the exact test is uninformative against equality, and the interval for the risk difference includes both modest negative and modest positive differences. The shift-stratified analysis is consistent with no common association. The apparent equality of the crude rates is therefore an observed marginal result, not a demonstration that the devices have equal warning rates.

The result is fragile in the ways small observational counts usually are. Only ten flags were observed, so the intervals are wide and compatible with differences that could matter operationally. The shift-specific proportions differ in direction, which makes a single common odds ratio a summary of sparse strata rather than a stable effect. The rows are aggregated by shift and device, so the analysis cannot adjust for poster characteristics, technician experience, inspection order or other covariates. The log records each poster once, but the four rows do not provide inspection-level identifiers. No external data or literature were used, and there is no independent confirmation set.

A flag means a print-inspection warning, not a confirmed defect, and technicians assigned devices by availability, without randomization. [C4]

That definition and allocation rule limit what can be concluded. A difference in warning rates would not by itself establish a difference in defect rates, and the absence of a difference in warnings would not establish equivalent print quality. Because device assignment was not randomized and shift is associated with both device mix and warning rate, the contrast is vulnerable to confounding. The appropriate conclusion is descriptive: under the observed allocation, the logged overall warning rates were equal, with no evidence of an association in either the primary or the stratified analysis.

## Limitations

- The dataset is very small: four aggregate rows and ten warning events. Exact and asymptotic tests have limited power, and the confidence intervals are wide.
- Allocation was by technician availability, not randomization, so the comparison does not identify a causal device effect.
- Shift may confound the device contrast; the stratified analysis addresses this only coarsely, with two strata and sparse cells.
- Flags are warnings rather than confirmed defects; the outcome is not a defect rate.
- The aggregate rows prevent adjustment for poster, technician or inspection-level covariates.
- The plan was written after the data had been inspected, so the analysis is retrospective and not a preregistered confirmation.

## Reproducibility

Run `python3 /mnt/analysis.py` from any working directory. The script reads `/mnt/scans.csv`, validates the four rows, recomputes every reported statistic with the Python standard library, and rewrites `research/results.csv` and `research/tests.csv`. The frozen plan digest is in `research/plan.sha256`, and the run receipt, including output and input digests, is `research/run.json`.

## Primary records

1. `field-note.md`. Print inspection — signed store log (synthetic primary record). Local study file; defines the flag outcome and the non-random allocation.
2. `scans.csv`. Logged poster inspections by shift and device. Local study file; the four aggregate rows analysed here.
