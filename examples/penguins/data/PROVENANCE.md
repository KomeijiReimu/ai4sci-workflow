# Origin of `penguins.csv`

Kristen B. Gorman and the Palmer Station Antarctica Long Term Ecological Research (LTER) Program collected the field observations. Allison M. Horst, Alison Presmanes Hill and Kristen B. Gorman curated the `palmerpenguins` package. This example redistributes only the package's unmodified compact CSV and its license, not the original species-specific archives or package code.

**Exact file.** `allisonhorst/palmerpenguins` release [v0.1.0](https://doi.org/10.5281/zenodo.3960218), upstream Git commit [`e5bfd5f2c7da95b0823e9501b9013eb2ef124fa7`](https://github.com/allisonhorst/palmerpenguins/tree/e5bfd5f2c7da95b0823e9501b9013eb2ef124fa7), path `inst/extdata/penguins.csv`. Retrieved directly from the [immutable raw URL](https://raw.githubusercontent.com/allisonhorst/palmerpenguins/e5bfd5f2c7da95b0823e9501b9013eb2ef124fa7/inst/extdata/penguins.csv) on 2026-11-23 UTC. Size: 15,241 bytes. SHA-256: `f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93`. No column or row transformations were applied to the downloaded bytes. GitHub's tag API returned this commit; [Zenodo's release record](https://zenodo.org/api/records/3960218) identifies the authors, title `allisonhorst/palmerpenguins: v0.1.0` and version `v0.1.0`.

**Rights.** The release's [DESCRIPTION](https://raw.githubusercontent.com/allisonhorst/palmerpenguins/e5bfd5f2c7da95b0823e9501b9013eb2ef124fa7/DESCRIPTION) states `License: CC0`. Its [`LICENSE.md`](https://raw.githubusercontent.com/allisonhorst/palmerpenguins/e5bfd5f2c7da95b0823e9501b9013eb2ef124fa7/LICENSE.md) is reproduced byte-for-byte [here](LICENSE.md), SHA-256 `8e2c443dd9aea6fcd6c293dbf66935bd5ef502fc0ca9b466c773cf9316d5e04c`. In the “Data source” section of their [package paper](https://journal.r-project.org/articles/RJ-2022-020/), the authors explicitly say that the data in the package “are available for use by CC0 license”. This CC0 1.0 Universal dedication applies to the redistributed dataset independently of the workflow repository's license.

**Source accessions.** The pinned [data dictionary and source list](https://raw.githubusercontent.com/allisonhorst/palmerpenguins/e5bfd5f2c7da95b0823e9501b9013eb2ef124fa7/man/penguins.Rd) identifies the following Environmental Data Initiative (EDI) releases by Palmer Station Antarctica LTER and K. Gorman (2020). Each DOI resolved to the matching EDI package identifier; species/title, creators, year and repository were also checked against EDI's deposited DataCite DOI metadata. The EDI landing pages requested login; the input used here was retrieved from the public package release above.

| Species | EDI package | Source DOI |
|---|---|---|
| Adélie | `knb-lter-pal.219.5` | [10.6073/pasta/98b16d7d563f265cb52372c8ca99e60f](https://doi.org/10.6073/pasta/98b16d7d563f265cb52372c8ca99e60f) |
| Gentoo | `knb-lter-pal.220.5` | [10.6073/pasta/7fca67fb28d56ee2ffa3d9370ebda689](https://doi.org/10.6073/pasta/7fca67fb28d56ee2ffa3d9370ebda689) |
| Chinstrap | `knb-lter-pal.221.6` | [10.6073/pasta/c14dfcfada8ea13a17536e73eb6fbe9e](https://doi.org/10.6073/pasta/c14dfcfada8ea13a17536e73eb6fbe9e) |

**Primary-source excerpts.** The [dictionary excerpt](dictionary-excerpt.txt) is the title in the pinned data dictionary. The same dictionary defines `flipper_length_mm` as “an integer denoting flipper length (millimeters)” and `body_mass_g` as “an integer denoting body mass (grams)”.

The [two caption excerpts](caption-excerpts.txt) come from figure 4 of Horst, Hill and Gorman, *The R Journal* (2022), [10.32614/RJ-2022-020](https://journal.r-project.org/articles/RJ-2022-020/). They are separate passages from the same caption. The [source manifest](../research/sources.json) identifies the originals and the hashes of these short transcriptions.

Original field paper: Gorman, Williams and Fraser, *PLOS ONE* (2014), [10.1371/journal.pone.0090081](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0090081). Both article DOIs, titles and author lists were checked against the publishing journals. The field paper and the package paper are context, not sources for this example's test errors.
