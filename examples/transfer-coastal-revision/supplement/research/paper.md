# Period choice and the fitted rate of sea-level rise on the Dutch coast

**Scope.** Do the short windows highlighted in Figure 4 of Keizer et al. (2022) describe the difference between the earlier and later parts of the full record? The unit is the annual rate of a model's smooth sea-level component for the mean of the six reference gauges. This is a new summary of four archived v1 fits, not four independent replications. The raw station-level observations served only to check the panel, units and unadjusted linear slopes. The four specifications are trend only (Tr), trend plus nodal tide (TrNc), and trend plus nodal tide with either zonal wind (TrNcZw) or a pressure gradient (TrNcPd).

**Time support.** Whole = 1900–2019, early = 1900–1959 and late = 1960–2019, inclusive. The observed panel has annual levels over 1890–2020; a centered rate at year *t* uses levels at *t*−1 and *t*+1, so 2019 is a valid rate label and 2020 is not. Average all rate centers once per period. This is not a secant between the first and last reported calendar years. The shorter windows, in order below, are 1900–1919, 1920–1939, 1940–1959 and 2000–2019. “After the decade” uses 1970–2019. Subtract early from late within the same model and the same archived draw ID.

**What the intervals describe.** The [initial plan](plan.json) predates measurement of these aggregates. The point estimate is the average fitted `rate_slr` (mm/yr), checked against a centered finite difference of `trend` in cm. The frozen percentile bands are literal distributions of the archived draw means and their paired differences; their locations do not align with the fits. Their numerical properties were retained, not treated as confidence limits around a different point estimate. The [subsequent amendment](calibration-amendment.md) specifies a sensitivity analysis: transfer the annual draw deviations about the ensemble mean onto the fitted series. This assumes correct scatter and temporal dependence after a year-specific location shift. Original generation code or a verified transformation is absent from the supplied material. All ranges below use the central 95% of 100 trajectories by linear quantile interpolation; the CSVs include central 90% ranges too. Coverage for the fitted parameter is not established.

## Primary contrast

In each of the following sentences the fitted means are ordered whole, early, late. Brackets around a fitted contrast show the **centered sensitivity** range; brackets around an archive median show the **unshifted archive** range. Both are in mm/yr.

For Tr, the three fitted means are 2.04 / 1.82 / 2.26 mm/yr; later minus earlier is 0.44 [-0.26, 1.06] mm/yr under recentering. [C1]

The unshifted Tr trajectories give a median paired difference of 0.86 [0.15, 1.47] mm/yr. [C2]

For TrNc, the three fitted means are 2.08 / 1.85 / 2.30 mm/yr; later minus earlier is 0.45 [0.03, 0.89] mm/yr under recentering. [C3]

The unshifted TrNc trajectories give a median paired difference of 0.85 [0.41, 1.28] mm/yr. [C4]

For TrNcZw, the three fitted means are 1.94 / 1.66 / 2.23 mm/yr; later minus earlier is 0.57 [0.28, 0.95] mm/yr under recentering. [C5]

The unshifted TrNcZw trajectories give a median paired difference of 1.13 [0.84, 1.51] mm/yr. [C6]

For TrNcPd, the three fitted means are 1.92 / 1.73 / 2.11 mm/yr; later minus earlier is 0.38 [-0.15, 1.00] mm/yr under recentering. [C7]

The unshifted TrNcPd trajectories give a median paired difference of 0.70 [0.19, 1.35] mm/yr. [C8]

Unadjusted slopes of the gauge average for the whole, early and late windows are 1.92, 1.82 and 2.18 mm/yr, respectively. [C9]

## Short windows

These are fitted-rate means in chronological order, not the original period-specific p-values. The centered ranges for each window are displayed in manuscript Table 3b. The original preprint’s reported short-window uncertainty remains identified separately in its revised §4.3.

The four Tr short-window means are 2.15, 1.69, 1.63 and 2.69 mm/yr. [C10]

The four TrNc short-window means are 2.27, 1.67, 1.62 and 2.80 mm/yr. [C11]

The four TrNcZw short-window means are 1.82, 1.68, 1.47 and 2.97 mm/yr. [C12]

The four TrNcPd short-window means are 1.86, 1.78, 1.54 and 2.74 mm/yr. [C13]

## Excluding the transition decade

Here the later period begins in 1970; the baseline is unchanged. The ranges below are the centered sensitivity, not estimated change points.

For Tr, the after-decade mean is 2.37 mm/yr; its increase over early is 0.55 [-0.23, 1.20] mm/yr under recentering. [C14]

For TrNc, the after-decade mean is 2.43 mm/yr; its increase over early is 0.57 [0.11, 1.10] mm/yr under recentering. [C15]

For TrNcZw, the after-decade mean is 2.41 mm/yr; its increase over early is 0.75 [0.41, 1.18] mm/yr under recentering. [C16]

For TrNcPd, the after-decade mean is 2.24 mm/yr; its increase over early is 0.52 [-0.06, 1.19] mm/yr under recentering. [C17]

## Interpretation

Lengthening the windows preserves a higher later *fitted mean* for all models. Under the additive-scatter assumption the TrNcZw range is positive, TrNc is just above zero, and Tr and TrNcPd are inconclusive; omitting the transition decade does not change that classification. This is not an unconditional significance result. Only a few trajectories determine the tail limits, the models share one coastal record, and a contrast at a fixed boundary does not determine an onset year. The original p-values concern different windows and a separately constructed null; no new p-value is inferred from a percentile count. Resolving absolute uncertainty needs documented v1 rate-draw construction or correctly normalized joint trajectories, not another choice of cutoff.

[Revised article](../../revised.md) · [Reply](../../response.md) · [Input origins and SHA-256](../inputs.json) · [Unshifted numerical results](summary.csv) · [Sensitivity results](centered-sensitivity.csv) · [Research handoff](handoff.md).
