# A weekly benchmark for Germany's day-ahead load forecast

The archived forecast had **540 MW lower mean absolute error** than repeating last week's load across 2019. During the top tenth of hours by realized demand, it had **159 MW higher error**. Both comparisons use the same German national series and the same local-clock definition of a week.

[Read the short paper and figure](research/paper.md) · [Primary table](research/primary.csv) · [Why the follow-up was chosen](research/followup-decision.md)

## Reproduce

From the repository root, with Python 3.10+ and the IANA `Europe/Berlin` time zone:

```sh
python3 -B examples/power-forecast/check_repro.py --download
```

The first run downloads the [versioned hourly CSV](https://data.open-power-system-data.org/time_series/2020-10-06/time_series_60min_singleindex.csv) into `.local/power-forecast/` (130,339,665 bytes uncompressed). It verifies the SHA-256 from the [official package manifest](https://data.open-power-system-data.org/time_series/2020-10-06/datapackage.json): `6a7f2bc571314cbf9c321cc03437691cd4be95c3a6f075e60ff99e8035c704c8`. Subsequent runs use the cache; `--archive PATH` selects an existing copy. The script recomputes both comparisons and the SVG in `.local/power-forecast/replay/`, checks them and the coverage report against the published files, then audits the study. All computations use the Python standard library.

To audit the saved evidence offline without downloading the hourly input:

```sh
python3 -B ai4sci.py audit examples/power-forecast
```

## Source and reuse

Open Power System Data. 2020. *Data Package Time series*, version 2020-10-06. [DOI: 10.25832/time_series/2020-10-06](https://doi.org/10.25832/time_series/2020-10-06). Primary data: [ENTSO-E Transparency Platform](https://transparency.entsoe.eu/); OPSD calculated the hourly national actual and day-ahead series. This example distributes calculated summary errors, counts, a threshold and a figure. Obtain the hourly readings from the release under the [source terms](https://transparencyplatform.zendesk.com/hc/en-us/articles/40921911218961-Legal-Terms-and-Conditions); the OPSD site's CC BY notice for **text** is not a blanket license for all primary data.

The [frozen plan](research/plan.json) sets out exclusions and the primary metric; the [run receipt](research/run.json) identifies exact inputs and outputs. The [review](research/review.md) records a separate arithmetic reconstruction of the results.
