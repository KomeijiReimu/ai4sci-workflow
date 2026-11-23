# Slate versus Amber for on-time processing: R-17 registry analysis

**Prepared:** 24 November 2026  
**Evidence (only):** `/mnt/registry.csv`; `/mnt/registry-protocol.md` (protocol R-17, §§A–C); `/mnt/briefing.txt` (claim under test). Offline analysis; no external data.

## Bottom line

- **Descriptively, yes—but only descriptively.** Under R-17's target weights, Slate's observed on-time share is higher on the sites where both routes operated: **60.6% vs 52.5% (+8.1 pp)** after target-weighting Basalt and Linden. On the full 50/30/20 target, Slate's standardized rate is **62.5%**; Amber's lies between **42.0% and 62.0%** because Quartz–Amber is unobserved, so the gap is **+0.5 to +20.5 pp**. No admissible missing-cell rate reverses the sign.
- **Causally, no.** Route choice was not randomized and was made from current queue length (§A), so the contrast is confounded. Amber also has no Quartz observations, so the full-target causal effect fails positivity and is not identified.
- **Crude pooling misleads.** Slate 50.6% vs Amber 81.4% (−30.8 pp) is a site-mix artifact, not a target estimate.
- **The newsletter claim is unsupported.** It is unsigned recollection by a writer who did not inspect the register or protocol. Slate is observed at all three sites (K07/K08, K06, K09); no site is absent—only the Quartz–Amber cell is. Section C states that an absent cell means no observations, not failure.

## 1. Protocol rules and primary evidence

| R-17 element | Rule | Consequence here |
|---|---|---|
| §A outcome | Inspected tile delivered before its processing deadline; each tile inspected once; batch totals disjoint | Tile-level rates; do not weight batches |
| §A allocation | Dispatcher chose route using current queue length; **not randomized** | Observed contrast is associational |
| §B target | 50% Basalt, 30% Linden, 20% Quartz | Weights 0.5 / 0.3 / 0.2 |
| §B denominator | Inspected tiles, not batches | Sum tiles within site–route |
| §B covered sites | Retain only sites where both routes were used; renormalize target weights | Basalt + Linden, weights 0.625 / 0.375 |
| §C missing cell | Absent route–site = no observations, **not** all missed; no external rate | Quartz–Amber rate *p* can only be bounded in [0, 1] |

Registry rows used: K07 and K08 (Basalt–Slate); K01 and K05 (Basalt–Amber); K06 (Linden–Slate); K02 and K04 (Linden–Amber); K09 (Quartz–Slate). There is no Quartz–Amber row.

`briefing.txt` is secondary at best: unsigned, based on a dispatcher's recollection, and the writer did not inspect the register or protocol. It is treated only as the claim being tested, not as evidence. It also refers to “sites absent from the register,” but all three sites appear in the registry; the absence is one route–site cell.

## 2. Observed rates

**Table 1. Observed site–route rates (R-17 §B tile denominators).**

| Site | Route | Batches | On time / inspected | Rate |
|---|---|---:|---:|---:|
| Basalt | Slate | K07, K08 | 48 / 120 | 40.0% |
| Basalt | Amber | K01, K05 | 6 / 20 | 30.0% |
| Linden | Slate | K06 | 19 / 20 | 95.0% |
| Linden | Amber | K02, K04 | 108 / 120 | 90.0% |
| Quartz | Slate | K09 | 14 / 20 | 70.0% |
| Quartz | Amber | — | — | not observed |

Within-site Slate − Amber gaps are **+10.0 pp** at Basalt (40.0% vs 30.0%) and **+5.0 pp** at Linden (95.0% vs 90.0%). Quartz has Slate only, so no within-site Amber contrast exists there.

**Table 2. Pooled and target-weighted comparisons.**

| Scope | Slate | Amber | Slate − Amber |
|---|---:|---:|---:|
| Crude pooled (tile-pooled), all observed rows | 81/160 = 50.625% | 114/140 = 81.429% | −30.804 pp |
| Target-weighted **covered sites** (0.625 Basalt, 0.375 Linden) | 60.625% | 52.500% | **+8.125 pp** |
| Full target (50/30/20), **bounded** | 62.500% | 42.000–62.000% | **+0.5 to +20.5 pp** |

The crude reversal is composition: 120/140 (85.7%) of Amber tiles are at high-rate Linden, while 120/160 (75.0%) of Slate tiles are at low-rate Basalt. Both observable within-site contrasts favor Slate; the pooled contrast favors Amber. This is Simpson's reversal, so the crude pooled rate is not a usable target estimate.

## 3. Target-weighted comparison on covered sites

Protocol §B drops Quartz (Amber was not used there) and renormalizes: Basalt 0.5/0.8 = 0.625, Linden 0.3/0.8 = 0.375.

```text
Slate = 0.625(0.40) + 0.375(0.95) = 0.60625
Amber = 0.625(0.30) + 0.375(0.90) = 0.52500
gap   = 0.08125 = 13/160 = +8.125 pp
```

This is exact for the covered sites: all four site–route cells at Basalt and Linden are observed, so no extrapolation is needed. It remains a **descriptive standardized contrast**, not a causal effect.

## 4. Full-target contrast and the missing cell

Slate has all three target cells, so its full-target standardized rate is identified:

```text
Slate = 0.5(0.40) + 0.3(0.95) + 0.2(0.70) = 0.625 = 62.5%
```

Amber is missing Quartz, which carries weight 0.2. Writing the unobserved Quartz–Amber rate as *p*:

```text
Amber(p) = 0.5(0.30) + 0.3(0.90) + 0.2p = 0.42 + 0.2p
D(p)     = Slate - Amber(p)               = 0.205 - 0.2p
```

Because §C supplies no rate for the missing cell and *p* is a proportion, the **tightest protocol-allowed range is *p* ∈ [0, 1]**. Hence:

- Amber full-target standardized rate: **42.0% to 62.0%**.
- Gap D(*p*): **+0.5 pp to +20.5 pp** (exactly 1/200 to 41/200).
- Lower bound occurs at *p* = 1 (all Quartz–Amber tiles on time); upper bound at *p* = 0.
- Break-even is *p* = 1.025 = 41/40, outside [0, 1]. **The sign is therefore identified: Slate's standardized rate exceeds Amber's for every admissible value of the missing cell.**

**What the full-target contrast can be:** a sharp bound on the sign and magnitude, conditional on the R-17 weights; and an exact statement of Slate's full-target standardized rate (62.5%). **What it cannot be:** a point estimate of Amber's Quartz rate, Amber's full-target rate, or the full-target gap; a claim about the actual intended population's realized performance; or anything tighter than [0.5, 20.5] pp without an extra assumption. For example, borrowing Quartz–Slate's 70% for Quartz–Amber would give Amber 56.0% and a +6.5 pp gap, but that is an untested assumption that R-17 does not license.

These are **identification bounds for the weighted contrast, not confidence intervals**. R-17 specifies no sampling model, and the register is a finite set of inspected tiles. Reading the newsletter's assertion as a 0% rate for any unobserved cell would produce the *largest* gap (20.5 pp), but §C expressly forbids treating absence as failure; that reading is an extreme assumption, not evidence.

## 5. Descriptive versus causal conclusions

**Table 3. Claims and evidential support.**

| Proposition | Supported? | Basis |
|---|---|---|
| Observed on-time shares differ by site and route | Yes — descriptive | Table 1; registry rows K01–K02, K04–K09 |
| Under R-17 weights, Slate's standardized share is higher on covered sites | Yes — descriptive | §B; exact +8.125 pp |
| The full-target standardized gap is positive for every admissible missing rate | Yes — descriptive, bounded | §B/C; D(*p*) = 0.205 − 0.2*p* > 0 on [0, 1] |
| Slate **causes** better on-time processing | **No** | §A: non-random allocation by queue length; confounding; no design or adjustment |
| The full-target causal effect is identified | **No** | No Amber at Quartz (positivity failure); §C forbids an external rate |
| The newsletter's “missed every deadline on absent sites” claim | **No / unsupported** | §C: absence is no observations, not zero; no site is absent from the registry—only the Quartz–Amber cell |
| Crude pooled rates estimate target performance | **No** | Site-mix confounding; reversal shown above |

The causal barrier is stated in the primary record: dispatchers selected route using current queue length, and allocation was not randomized (§A). Queue length plausibly affects on-time delivery and is not recorded in the registry, so it cannot be adjusted for; batches also differ in ways the register does not describe. Even the within-site contrasts are observational. Additionally, the intended population includes Quartz (20%), where Amber has zero observations, so there is no overlap for a full-target causal contrast. “Better” can therefore describe realized on-time shares under the observed allocation, but it cannot be read as the effect of switching a site to Slate.

## 6. Verdict

**Descriptive conclusion (defensible):** under R-17's target weights, Slate's observed on-time share is higher than Amber's at both covered sites (+8.125 pp target-weighted) and the full-target standardized gap is positive for every admissible value of the missing Quartz–Amber cell (+0.5 to +20.5 pp), with Slate's full-target standardized rate at 62.5%.

**Causal conclusion (not defensible):** the registry cannot establish that Slate is better than Amber. Allocation was queue-driven and non-random, and the missing Quartz–Amber cell leaves the full-target magnitude unidentified.

A defensible summary for the cooperative: *“Among registered tiles, after standardizing to R-17's target site weights, Slate had a higher observed on-time share than Amber on the sites where both routes operated (+8.1 pp), and the full-target standardized gap is positive under any admissible value for the unobserved Quartz–Amber cell (+0.5 to +20.5 pp). This is a descriptive association, not evidence that Slate causally improves on-time processing; the full-target magnitude is unidentified.”*

A causal or full-population claim would require Quartz–Amber observations, or a randomized/queue-balanced allocation.

## 7. Reproduction

The computation is `analysis/analyze.py` (Python 3.13, standard library only; no network, no external data). Actual command:

```bash
cd /mnt && python3 analysis/analyze.py
```

It reads `registry.csv`, applies §§A–C, and writes `analysis/results.csv` (machine-readable table) and `analysis/results.json` (structured output with exact fractions). Reruns are byte-identical; the key quantities were independently recomputed through a separate code path.

## Appendix: machine-readable result table (`analysis/results.csv`)

```csv
metric,scope,site,route,numerator,denominator,value,unit,evidence,note
on_time_rate,site_route,Basalt,Slate,48,120,0.400000,proportion,registry K07+K08,inspected tiles denominator (R-17 B)
on_time_rate,site_route,Basalt,Amber,6,20,0.300000,proportion,registry K01+K05,inspected tiles denominator (R-17 B)
on_time_rate,site_route,Linden,Slate,19,20,0.950000,proportion,registry K06,inspected tiles denominator (R-17 B)
on_time_rate,site_route,Linden,Amber,108,120,0.900000,proportion,registry K02+K04,inspected tiles denominator (R-17 B)
on_time_rate,site_route,Quartz,Slate,14,20,0.700000,proportion,registry K09,inspected tiles denominator (R-17 B)
on_time_rate,site_route,Quartz,Amber,,,,proportion,R-17 C; no registry row,"absent route-site cell: no observations, not zero successes"
on_time_rate,crude_pooled_all_observed_sites,,Slate,81,160,0.506250,proportion,registry all rows,composition-confounded crude rate; not the target estimand
on_time_rate,crude_pooled_all_observed_sites,,Amber,114,140,0.814286,proportion,registry all rows,composition-confounded crude rate; not the target estimand
contrast,crude_pooled_all_observed_sites,,Slate_minus_Amber,,,-30.803571,percentage_points,registry all rows,negative: Amber higher in the crude pool
on_time_rate,target_weighted_covered_sites,,Slate,,,0.606250,proportion,"R-17 B; Basalt, Linden","weights renormalized over covered sites: Basalt=0.625000, Linden=0.375000"
on_time_rate,target_weighted_covered_sites,,Amber,,,0.525000,proportion,"R-17 B; Basalt, Linden","weights renormalized over covered sites: Basalt=0.625000, Linden=0.375000"
contrast,target_weighted_covered_sites,,Slate_minus_Amber,,,8.125000,percentage_points,"R-17 B; Basalt, Linden",exact over covered sites; no missing cells
on_time_rate,full_target,,Slate,,,0.625000,proportion,R-17 B; all Slate cells observed,identified exactly: all three Slate cells observed
on_time_rate,full_target,,Amber_lower,,,0.420000,proportion,R-17 B/C,"lower bound, missing Quartz-Amber rate p = 0"
on_time_rate,full_target,,Amber_upper,,,0.620000,proportion,R-17 B/C,"upper bound, missing Quartz-Amber rate p = 1"
contrast_bound,full_target,,Slate_minus_Amber_lower,,,0.500000,percentage_points,R-17 B/C,tightest protocol-allowed lower bound (p = 1)
contrast_bound,full_target,,Slate_minus_Amber_upper,,,20.500000,percentage_points,R-17 B/C,tightest protocol-allowed upper bound (p = 0)
break_even,full_target,,missing_Quartz_Amber_rate,,,1.025000,proportion,R-17 B/C,"rate at which Slate and Amber tie; outside [0,1] => sign identified"
```
