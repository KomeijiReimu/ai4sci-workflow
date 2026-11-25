# Did countries with faster income growth also see bigger gains in secondary enrollment?

In 2015, the richer countries in this sample tended to have higher gross secondary enrollment: the correlation with log GDP per capita was **0.772**. Yet from 1995 to 2015, countries where GDP per capita grew faster did not consistently see larger enrollment gains. The correlation between the two changes was **0.185** (95% country-bootstrap interval **−0.068 to 0.431**). Comparing the same 49 countries both ways gives a gap of **0.587 correlation units** (0.324 to 0.856). The gap describes an association, not the effect of raising a country's income.

[Read the manuscript](manuscript.md) · [View the full-precision estimates and intervals](estimates.csv)

## What was compared

Each country contributed one pair of observations. Of 217 country codes at either endpoint, 49 had GDP and enrollment at both dates; all 49 also had both life-expectancy observations. The 168 excluded codes remain in the [archived data](endpoints.csv), with missing values left blank. The results describe the 49 observed countries. Gross enrollment counts secondary students of **any age** relative to the official secondary-school-age population; it can exceed 100%.

The first Pearson correlation compares 2015 log GDP per capita with 2015 enrollment. The second compares the natural log of the 2015-to-1995 GDP per capita ratio with the change in enrollment **in percentage points**. For each of 2,000 bootstrap draws (seed 1729), the analysis resamples whole countries with replacement, uses the same draw for both correlations and subtracts them within the draw. The intervals use the 2.5th and 97.5th percentiles. The design gave conflicting thresholds in different units, so the gap and its interval are reported without a threshold verdict.

An exploratory follow-up adjusts each correlation for change in life expectancy. The adjusted change correlation was 0.168 (−0.087 to 0.409), again with an interval spanning zero. The adjusted level-minus-change gap was 0.564 (0.281 to 0.841). A separate test asks whether starting life expectancy modifies the growth–enrollment slope. For each extra standard deviation of starting life expectancy, the estimated slope was **0.990 enrollment percentage points steeper per standard deviation of log GDP per capita growth** (−1.849 to 4.589), controlling for life-expectancy change. Both directions fit the interval; the point estimate is opposite to the predicted weaker slope.

## Replay the analysis offline

From this directory, with Python 3 and NumPy (tested with Python 3.11.14 and NumPy 2.4.4):

```sh
python3 replay.py
```

The script selects the paired observations from `endpoints.csv`, prints the coverage, estimates and bootstrap intervals, and stops on a disagreement with the archived results. In each supplemental draw it refits the life-expectancy adjustments and restandardizes the regression predictors.

## Data and authorship

The three series are from the World Bank's *World Development Indicators*, API vintage **2026-11-11**, under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) ([World Bank data licenses](https://datacatalog.worldbank.org/public-licenses)). The extract keeps the original country codes, values and blanks from a 1990–2022 panel, selecting only 1995 and 2015 and the following measures:

| Series | Measurement |
|---|---|
| [NY.GDP.PCAP.PP.KD](https://data.worldbank.org/indicator/NY.GDP.PCAP.PP.KD) | GDP per capita at purchasing power parity, constant 2021 international dollars |
| [SE.SEC.ENRR](https://data.worldbank.org/indicator/SE.SEC.ENRR) | Gross secondary enrollment, percent (UNESCO Institute for Statistics, via WDI) |
| [SP.DYN.LE00.IN](https://data.worldbank.org/indicator/SP.DYN.LE00.IN) | Life expectancy at birth, total, in years |

UNDP's [2025 Human Development Report technical notes](https://hdr.undp.org/sites/default/files/2025_HDR/HDR25_Technical_Notes.pdf) explain the index that motivated the question. The analysis uses the three WDI measures rather than the composite HDI.

Qwen3-4B, running locally on CPU, chose the schooling question, the Pearson metric and the 1995–2015 endpoints, and drafted both the main study and the life-expectancy follow-up. The coordinator supplied the log-GDP and paired-country-bootstrap framework, implemented and ran the computations, and corrected factual wording in the manuscript.
