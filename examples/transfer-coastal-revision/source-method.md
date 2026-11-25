# Why the archived Dutch sea-level rate trajectories have a different center

This post-study check uses the original KNMI notebooks to interpret the archived trajectories. It is separate from the offline manuscript’s frozen analysis.

**What a trajectory contains.** In [`gam_model.ipynb`][gam] (zero-based cell 51), `bootstrap_trend` replaces the observed residuals with simulated residuals and refits the model. `compute_rate` takes a centered two-year difference of the resulting trend, converting cm/yr to mm/yr. Its output $B_{tb}$ is the **full refitted trend rate** for year $t$ and replicate $b$, not a deviation from the original fit $r_t$. `rate_uncertainty` then adds $r_t$ to every column. Cells 67–69 save 100 such columns per model: $A_{tb}=r_t+B_{tb}$. Subtract $r_t$ **once** to recover $B_{tb}$.

Adding the same rate to every draw shifts their center but leaves their within-year spread unchanged. For a late-minus-early mean difference $D$, the stored contrast is likewise $D(A_b)=D(r)+D(B_b)$: its spread is unchanged, but its center is shifted by the fitted change. For TrNcZw over the two 60-year periods below, the mean stored contrast is 1.128 mm/yr; subtracting the fitted 0.572 gives 0.556 mm/yr across the recovered refits.

**Figure 4 and Table 2 use different uncertainties.** `rates_quantiles` computes the annual standard deviation $s_t$ across refits with pandas `std` (`ddof=1`). Cells 17 and 41 of the [figure notebook][fig] read and plot the fitted rate and its **pointwise central 90% Gaussian band**, $r_t\pm1.64485\,s_t$, rather than empirical trajectory percentiles. For a fixed-period test (cell 25; cell 22 is the single-year analogue), take each replicate’s two period means, then difference them. The test uses $\mathrm{SE}=\mathrm{SD}_{b}[D(A_b)]$ with `np.std` (`ddof=0`) and one-sided $p=1-\Phi(D(r)/\mathrm{SE})$. The numerator uses the fitted `0.5` trace: the centered derivative of the original trend, which matches `rate_slr` at every interior year in all four CSVs.

**Reference check.** Each triple compares 2000–19 with **1900–19, 1920–39 and 1940–59**, respectively. All 12 recalculations match the pinned notebook’s stored output (cell 26) to two decimals. Seven agree with [Table 2 of the original preprint][paper] at its stated precision; the five bold entries differ for reasons the available sources do not establish. The Table 2 caption also gives 0.24 for the first Tr comparison, versus 0.23 in the table itself.

| Model | Recalculated one-sided $p$ | Table 2 as printed |
|---|---|---|
| Tr | **0.25**, 0.06, **0.04** | **0.23**, 0.06, **0.05** |
| TrNc | **0.15**, 0.01, 0.01 | **0.14**, 0.01, 0.01 |
| TrNcZw | 0.00, 0.00, 0.00 (rounded) | <0.01, <0.01, <0.01 |
| TrNcPd | **0.08**, **0.04**, 0.01 | **0.05**, **0.02**, 0.01 |

**New comparison using the original test: 1960–2019 minus 1900–1959.** These results use the existing fits and draws; they were not reported in the original Table 2.

| Model | Fitted change (mm/yr) | Original-method SE (mm/yr) | One-sided $p$ |
|---|---:|---:|---:|
| Tr | 0.4392 | 0.3296 | 0.09132 |
| TrNc | 0.4517 | 0.2385 | 0.02914 |
| TrNcZw | 0.5715 | 0.1750 | 0.000547 |
| TrNcPd | 0.3794 | 0.2923 | 0.09713 |

The test compares two fixed period means. It neither estimates a change point nor establishes interval coverage from a fresh bootstrap.

**Rerun.** Extract the [pinned KNMI archive][zip] beside this repository’s `examples/` directory. From the repository root run:

```sh
python3 examples/transfer-coastal-revision/source_method.py NetherlandsSeaLevelAcceleration-8c4b55df2b88feb4ebaa191f6d3e8bb9a4b8c86b/outputs
```

The [standalone script with SHA-256 digests](source_method.py) reads only the four `results_*.csv` and four `rates_*.csv` files in the [public outputs directory][outputs]; it does not execute the notebooks.

[gam]: https://github.com/KNMI-sealevel/NetherlandsSeaLevelAcceleration/blob/8c4b55df2b88feb4ebaa191f6d3e8bb9a4b8c86b/gam_model.ipynb
[fig]: https://github.com/KNMI-sealevel/NetherlandsSeaLevelAcceleration/blob/8c4b55df2b88feb4ebaa191f6d3e8bb9a4b8c86b/make_figures%26tables.ipynb
[outputs]: https://github.com/KNMI-sealevel/NetherlandsSeaLevelAcceleration/tree/8c4b55df2b88feb4ebaa191f6d3e8bb9a4b8c86b/outputs
[zip]: https://github.com/KNMI-sealevel/NetherlandsSeaLevelAcceleration/archive/8c4b55df2b88feb4ebaa191f6d3e8bb9a4b8c86b.zip
[paper]: https://egusphere.copernicus.org/preprints/2022/egusphere-2022-935/egusphere-2022-935.pdf#page=11
