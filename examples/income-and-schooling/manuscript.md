# GDP per capita and secondary gross enrollment in 49 economies: levels and changes, 1995–2015

Richer countries may have higher school enrollment than poorer ones without countries whose incomes grow faster also experiencing larger enrollment gains. Comparing both associations in the same economies helps separate a cross-sectional ranking from evidence about change. It does not turn an observational comparison into a causal test.

Scherbov and Gietel-Basten (Introduction; Materials and methods) examined within-country heterogeneity, including US state life tables; their finding is not an estimate of schooling responses to GDP. UNDP’s technical notes (2025, pp. 2–4) combine normalized health, education and income dimensions geometrically, using log GNI, not PPP GDP; gross enrollment is not HDI’s schooling-years dimension. We therefore test a distinct association using a non-income observation rather than using the composite HDI as an independent outcome. Gross secondary enrollment counts enrolled students of any age relative to the official secondary-school-age population. It can exceed 100% and measures neither completion nor unique age-specific participation.

## Sample and comparison

Of 217 country codes represented at either endpoint, 49 had both GDP and education measurements at both dates; 168 were excluded rather than imputed. One independent sampling unit here is a country, not a country-year. The comparison is descriptive for these observed countries. The dataset includes secondary gross enrollment rates and GDP per capita (PPP) at both endpoints (1995 and 2015). Life expectancy at both endpoints is also included. The study retains the original endpoints, GDP definition, enrollment outcome, and country-level complete-case sampling. All 49 also had both life-expectancy observations, so the supplemental adjustment retained the same countries. The analysis includes the computation of unadjusted benchmarks on this analysis set. Partial correlations are computed by partialing out an intercept and change in life expectancy in years from both 2015 log GDP and gross secondary enrollment, then correlating the residuals. Repeat for log-income growth and enrollment change. The difference of the two partial correlations is reported. For descriptive moderation, enrollment change (percentage points) is regressed on standardized log-income growth, standardized baseline life expectancy in 1995, their product, and standardized life-expectancy change. The interaction coefficient shows the difference in enrollment slopes per extra baseline-life-expectancy SD. Paired percentile intervals with 2,000 country bootstrap draws, seed 1729, are estimated.

## Matched-country results

In 2015, log GDP per capita was positively associated with secondary gross enrollment across countries (Pearson r = 0.772, 95% country-bootstrap interval [0.654, 0.851]). The correlation between the 1995–2015 change in log GDP per capita and the percentage-point change in gross enrollment had a smaller positive point estimate (r = 0.185, interval [−0.068, 0.431]). The change interval includes zero and does not establish the sign of that association.

| Estimand | Estimate | 95% country-bootstrap bounds |
|---|---:|---:|
| end year levels | 0.772 | [0.654, 0.851] |
| two endpoint changes | 0.185 | [-0.068, 0.431] |
| levels minus changes | 0.587 | [0.324, 0.856] |

A change correlation as strong as the end-year level correlation would have weakened a persistent-country-differences account. Instead, the paired level-minus-change gap was 0.587 correlation units [0.324, 0.856], an interval entirely above zero. Log GDP per capita increased in 48 of the 49 countries; in three of those 48, gross enrollment did not rise. The separate verbal prediction that higher **initial** GDP per capita predicts larger school gains was not tested: a change in log GDP per capita, rather than its initial level, was related to enrollment change. This is a comparison of two dates, not a test of a GDP intervention.

## Exploratory life-expectancy adjustment

Adjusting both variables for **change** in life expectancy gave a partial level correlation of 0.732 [0.590, 0.826] and a partial change correlation of 0.168 [−0.087, 0.409]. The latter point estimate is positive, but its interval does not establish its sign. The paired difference between partial correlations was 0.564 [0.281, 0.841]; like the unadjusted gap, its interval excludes zero.

**Baseline** life expectancy, not its change, was the proposed moderator. The estimated interaction was +0.990 percentage points of enrollment change per standard deviation (SD) of log-income growth per SD of baseline life expectancy [−1.849, +4.589]. This interval is compatible with weaker or stronger growth slopes at higher baseline life expectancy. It does not establish the predicted weaker slope.

| Supplemental estimand | Estimate | 95% country-bootstrap bounds |
|---|---:|---:|
| sample unadjusted level | 0.772 | [0.654, 0.851] |
| sample unadjusted change | 0.185 | [-0.068, 0.431] |
| partial level | 0.732 | [0.590, 0.826] |
| partial change | 0.168 | [-0.087, 0.409] |
| partial level minus change | 0.564 | [0.281, 0.841] |
| growth by baseline life interaction pp | 0.990 | [-1.849, 4.589] |

## Limitations

The study is limited to the use of GDP per capita as a proxy for material wellbeing and secondary gross enrollment as a proxy for non-material wellbeing. The use of aggregated data may mask sub-national heterogeneity. The study also does not account for other factors that may influence educational access and health outcomes, such as political stability, cultural factors, and historical context. The findings are not causal or globally representative. The structured design specified a 0.05 correlation gap, while the simultaneous prose specified “0.5 percentage points” with a different decision direction. A correlation difference is not an enrollment percentage-point change. We report the gap and its interval without claiming a confirmatory pass under either interpretation. The adjusted estimators were specified after the unadjusted results were known and are exploratory.

## Conclusion

Log GDP per capita and gross enrollment were positively associated across the 49 economies in 2015. The estimated association between the 1995–2015 change in log GDP per capita and enrollment change was weaker; neither the unadjusted nor adjusted interval established its sign. Both paired gap intervals were above zero. Persistent differences between countries remain a plausible explanation for the stronger level association; these estimates do not identify the mechanism. The findings are limited by national aggregation, incomplete coverage, and unmeasured factors that may influence education and health.

## Supplied sources

The CORE Team, Doing Economics, empirical project 4, Introduction. https://books.core-econ.org/doing-economics/book/text/04-01.html

Scherbov Sergei, Gietel-Basten Stuart. Measuring inequalities of development at the sub-national level: From the human development index to the human life indicator. https://doi.org/10.1371/journal.pone.0232014. CC BY. Original publisher text; prose excerpts by section; figures, tables, displayed equations and bibliography omitted.

UNDP, Human Development Report 2025: Technical Notes, PDF pages 2–4. https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Technical_Notes.pdf
