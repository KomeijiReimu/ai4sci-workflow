# Input provenance and data rights

The offline input was a joined panel of WDI economies by ISO3 and year, 1990–2022. [Input hashes](inputs.sha256) identify the full panel and its accompanying scientific source material; `prepare.py` verifies `data.csv` before extraction. The complete panel and reading packet are not distributed.

The public replay input, [`data/analysis-frame.csv`](../data/analysis-frame.csv), is a transformed extract, pinned by [frame.sha256](frame.sha256). It contains 217 labeled economy rows, no source prose, no annual panel and no enrollment series. It includes the denominator and blanks so the analysis—not a prefiltered data release—determines eligibility. It is sufficient for *every* frozen comparison. A second checkout can use it directly. An owner of the original packet can regenerate it and compare bytes using the [replay instructions](../README.md).

## Data sources and attribution

| Source | Variables and public source locator | Reuse and changes here |
|---|---|---|
| World Bank, World Development Indicators and country classifications | [Real PPP GDP per capita, NY.GDP.PCAP.PP.KD](https://api.worldbank.org/v2/country/all/indicator/NY.GDP.PCAP.PP.KD?source=2&date=1990:2022&format=json&per_page=20000); [life expectancy, SP.DYN.LE00.IN](https://api.worldbank.org/v2/country/all/indicator/SP.DYN.LE00.IN?source=2&date=1990:2022&format=json&per_page=20000); [economy classifications](https://api.worldbank.org/v2/country?format=json&per_page=500) | Supplied source note identifies WDI as [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) ([World Bank licenses](https://datacatalog.worldbank.org/public-licenses)). Selected endpoints, trimmed region labels, transformed GDP and differenced life expectancy. No World Bank endorsement is implied. |
| UNDP, Human Development Report (2025); minor processing by Our World in Data, “Human Development Index – UNDP” | [HDI series](https://ourworldindata.org/grapher/human-development-index); [UNDP terms](https://hdr.undp.org/copyright-and-terms-use) | Supplied source note identifies [CC BY 3.0 IGO](https://creativecommons.org/licenses/by/3.0/igo/). Joined in the supplied vintage; this release retains only the 2000–2019 difference. No UNDP endorsement is implied. |

Source links identify the underlying public series. Later releases can revise values or classifications; a fresh API download is not evidence of byte identity with this vintage. The digest-checked transformed CSV supplies that identity for analysis.

## Frame dictionary

| Column | Definition |
|---|---|
| `iso3`, `region` | Supplied economy key; World Bank region with surrounding whitespace removed. Equal weight per key. |
| `log_gdp0`, `le0` | Natural logarithm of real PPP GDP per capita (constant 2021 international dollars), and period life expectancy at birth (years), both in 2000. |
| `growth15`, `growth19` | Natural log of the endpoint-to-2000 GDP per capita ratio, divided by log(1.5). Endpoints are 2015 and 2019 respectively. |
| `gain_le15`, `gain_le19` | Endpoint life expectancy minus its 2000 level, years. |
| `gain_hdi19` | HDI in 2019 minus HDI in 2000, in index points on the 0–1 scale. |

Blank cells are unavailable, never zero-filled. GDP must be positive to enter a log; the archived vintage and parser determine the exact cells. The ISO3-sorted UTF-8 CSV uses LF endings. `prepare.py` documents the complete transformation.

## Literature and originating question

The [CORE Team project introduction](https://books.core-econ.org/doing-economics/book/text/04-01.html) (CC BY-NC-ND 4.0) is credited by reference only; none of its text is included. The two brief source notes [on HLI](scherbov-note.md) and [on HDI construction](undp-note.md) identify article/technical-note passages and distinguish quotations from this study's interpretation. No literature or data outside the supplied material informed estimation.
