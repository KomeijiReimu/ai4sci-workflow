# Did faster-growing economies gain more years of life?

**A comparison of changes in real GDP per capita and life expectancy, 2000–2019**

Faster economic growth went together with larger longevity gains, even among economies with similar starting incomes and life expectancies in the same region. The evidence is clearer about the direction than the size: the primary interval includes an advantage smaller than the six months chosen in advance as a meaningful difference. GDP growth belongs beside a direct health measure on a development dashboard; on its own it tells us little about how much longevity improved in a particular economy.

## Why test change rather than levels?

The [CORE Team](https://books.core-econ.org/doing-economics/book/text/04-01.html) asks whether material prosperity implies better non-material living standards. Life expectancy gives that question a measurable health dimension. In the closest supplied empirical study, [Scherbov and Gietel-Basten](https://doi.org/10.1371/journal.pone.0232014) used life tables to construct a Human Life Indicator (HLI) that penalizes inequality in ages at death.

They reported a correlation of 0.87 between the HLI and the Human Development Index across US states in 2016. [C1]

That comparison ranks places at one time. A dashboard tracking *progress* needs to know whether the places growing faster also make greater health gains. Starting conditions offer a rival explanation: a country starting with low life expectancy may have more scope to reduce preventable deaths, and regional health improvements may reach countries growing at different rates.

The official HDI combines health, education and income; its standard-of-living indicator is gross national income per capita. [C2]

GDP and GNI are related but not identical. A change in GDP that accompanies a change in HDI may therefore partly reflect the construction of the index. This motivates a direct longevity outcome and a same-economy HDI comparison. The two supplied readings inform this design; they are not an exhaustive survey of growth and health.

## Comparison

Each economy contributes one pair of endpoints. The outcome is the change in World Development Indicators (WDI) life expectancy at birth, in years. The exposure is the log change in WDI real PPP GDP per capita (constant 2021 international dollars), scaled by $\log(1.5)$. A one-unit exposure contrast could compare a GDP growth factor of 1.8 with one of 1.2: both economies grew, but the first factor is 1.5 times the second. It does not mean an extra 50 percentage points of annual growth.

Of 217 economies in the frame, 192 entered the primary comparison; 25 lacked the required GDP observations and 0 lacked a life-expectancy change. [C3]

The primary ordinary least squares regression relates longevity change to scaled GDP growth, starting life expectancy, log starting GDP per capita and region indicators. It gives each economy equal weight, leaves missing endpoints missing and ends in 2019 to keep pandemic mortality out of the contrast. A second regression on the same economies omits all controls. If starting position and region accounted for the apparent relationship, the adjusted growth gradient should be small.

The [frozen decision rule](plan.json) asks whether the *adjusted* gradient exceeds half a year per unit of exposure. Six months is a reporting benchmark, not a biological cutoff. A 95% interval wholly above it favors a material positive association; an interval wholly below it rules out one that large under the model. An interval spanning the benchmark leaves the size unresolved. We also compare the interval with zero. Intervals use HC3 heteroskedasticity-robust standard errors with a normal critical value.

## Results

The adjusted growth contrast corresponded to 1.37 additional life-years gained, with an interval from 0.45 to 2.29 years that crosses the six-month benchmark. [C4]

The unadjusted gradient was 0.91 years versus 1.37 after adjustment; controlling for starting position and region strengthened rather than erased the association. [C5]

The fraction of variation in longevity gains accounted for by growth alone was 0.042; after removing the variation explained by starting position and region, growth accounted for 0.102 of what remained. [C6]

Thus a model based on initial conditions and regional means misses a positive association. The lower limit falls just below six months. The results support using growth as a directional marker in this period, but not the stronger claim that the adjusted difference clears the benchmark.

### How dependent is the result on the comparison?

Allowing curvature in the two baseline variables gave a gradient of 1.49 years, with an interval from 0.61 to 2.38. [C7]

Ending the comparison in 2015 instead gave a gradient of 1.08 years, with an interval from 0.44 to 1.73. [C8]

Leaving out one region at a time gave point estimates from 1.166 to 1.816 years; omitting East Asia and Pacific gave an interval from −0.27 to 2.61. [C9]

The curvature check clears the benchmark that the primary specification misses. The region omissions all preserve the sign of the *estimate*, not the precision of the finding. These comparisons reuse observations; they show sensitivity, not replication across independent samples.

### What changes when the outcome is HDI?

On the 166 economies with both outcomes, the adjusted growth contrast was associated with a longevity gain of 1.53 years and an HDI gain of 0.0373 index points. [C10]

The corresponding partial R-squared values were 0.116 for longevity and 0.490 for HDI. [C11]

These are comparisons of residual variation on the same rows and with the same controls. The stronger link with HDI is consistent with income entering the composite; it cannot tell us how much of the association runs through its income component. The [results table](estimates.csv) gives every slope, interval, denominator and partial R-squared; [coverage by region](coverage.csv) shows where endpoints were missing.

## What the gradient can and cannot tell a dashboard reader

The unit is an economy, not a person. A common slope averages over places with different mortality histories; it gives neither an economy-specific prediction interval nor the experience of a typical world resident. It does not measure healthy life expectancy, inequality in ages at death, or within-country distribution. Those questions need data beyond two national averages.

The timing does not identify a causal direction. Improved health can support income growth; health policy, conflict or disease can move both series. Conditioning on measured starting life expectancy can also introduce regression to the mean if baseline mortality is measured with error. Region indicators absorb regional mean differences but not correlated shocks in the remaining errors. HC3 intervals describe model uncertainty treating economies as independent, not design-based uncertainty for a random sample of the world. Missing GDP and HDI endpoints further limit the comparison to the reporting economies.

The practical distinction is between **tracking a tendency** and **measuring progress**. Growth tracked a favorable tendency through 2019. To report the size and distribution of health improvements, measure them directly.

## Sources and reproducibility

- The CORE Team. *Doing Economics*, empirical project 4, [introduction](https://books.core-econ.org/doing-economics/book/text/04-01.html). Source of the broad question.
- Scherbov, S., and Gietel-Basten, S. *Measuring inequalities of development at the sub-national level: From the human development index to the human life indicator*. [DOI](https://doi.org/10.1371/journal.pone.0232014), Materials and methods; Results and discussion, Fig. 6; Conclusions. Source of the HLI–HDI comparison.
- United Nations Development Programme. *Human Development Report 2025*, [Technical note 1](https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Technical_Notes.pdf), steps 1–2. Source of the HDI definition.
- World Bank, *World Development Indicators* (GDP and longevity); UNDP, *Human Development Report* (2025), HDI series with minor processing by Our World in Data. [Data provenance, licenses and transformations](../provenance/README.md). [Offline reproduction](../README.md).
