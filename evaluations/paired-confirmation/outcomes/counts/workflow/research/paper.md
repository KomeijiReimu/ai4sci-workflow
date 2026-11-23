# Slate versus Amber on-time processing under registry protocol R-17

## Summary

The registry does not support the newsletter's all-missed story, and it does not support a causal claim that Slate is better. It does support a descriptive one: pooled over all inspected tiles, Amber looks better, but that marginal reverses within every site where both routes were observed because route is confounded with site. Standardized to the protocol's intended site mix, Slate's on-time rate is higher on the covered sites and remains higher across the entire protocol-admissible range of the missing Quartz Amber cell. The result is an association among inspected tiles, not an identified route effect.

## Question and evidence base

The question is whether the cooperative can conclude that Slate is better than Amber for on-time processing in its intended service population, defined by protocol R-17 as 50 percent Basalt, 30 percent Linden and 20 percent Quartz. The only evidence is the supplied extract `registry.csv` (eight disjoint batches, 300 inspected tiles, 195 on time) and the signed protocol extract `registry-protocol.md`. The unsigned `briefing.txt` is treated as an assertion to check, not as evidence.

Protocol paragraph A fixes the outcome as delivery of an inspected tile before its processing deadline and states that allocation was not randomized. Paragraph B fixes inspected tiles, not batches, as the denominator and defines the covered-site calculation. Paragraph C states that an absent route-site combination means no observations were collected; it does not license a zero rate.

## Method

Batch rows were summed within each site-route cell. Each cell rate is on-time tiles divided by inspected tiles. The all-site pooled rate sums every inspected tile regardless of site. The covered-site comparison keeps Basalt and Linden, the two sites where both routes appear, and renormalizes the target weights from 50:30 to 50/80 and 30/80. The full-target comparison keeps 50/30/20 but leaves the Quartz Amber cell missing. Because the only protocol-admissible range for an unobserved proportion is the closed unit interval, that cell is bounded at zero and one, never imputed from an external rate. All arithmetic is exact rational arithmetic with six-decimal reporting.

## Results

The cells behind Table 1 come directly from the registry rows: Basalt Slate from K07 and K08, Basalt Amber from K01 and K05, Linden Slate from K06, Linden Amber from K02 and K04, and Quartz Slate from K09. Quartz Amber has no batch row at all. Overall, 195 of the 300 inspected tiles were on time (0.650000).

Every observed site-route rate, and the all-site pooled marginals, are in Table 1.

| Site | Slate inspected | Slate on time | Slate rate | Amber inspected | Amber on time | Amber rate |
|---|---:|---:|---:|---:|---:|---:|
| Basalt | 120 | 48 | 0.400000 | 20 | 6 | 0.300000 |
| Linden | 20 | 19 | 0.950000 | 120 | 108 | 0.900000 |
| Quartz | 20 | 14 | 0.700000 | — | — | unobserved |
| All-site pooled | 160 | 81 | 0.506250 | 140 | 114 | 0.814286 |

Across all inspected tiles pooled over sites, the Slate on-time rate was 0.506250 and the Amber rate was 0.814286. [C1]

The all-site pooled Slate-minus-Amber difference was -0.308036, so the marginal pooled comparison favors Amber. [C2]

Within Basalt, Slate's on-time rate was 0.400000 and Amber's was 0.300000; within Linden, Slate's was 0.950000 and Amber's was 0.900000; within Quartz, Slate's was 0.700000. [C3]

The protocol requires inspected tiles, not batches, as the within-site denominator, so each site-route rate uses its inspected-tile count. [C4]

The pooled reversal is Simpson's paradox: Slate tiles are concentrated in Basalt and Quartz, while Amber tiles are concentrated in Linden, where both routes do well. Pooling therefore compares different site mixes rather than the routes. Within both sites where the routes compete, Slate is higher by 0.100000 at Basalt and 0.050000 at Linden.

Table 2 gives the protocol comparisons.

| Comparison | Slate | Amber | Slate-minus-Amber |
|---|---:|---:|---:|
| Covered sites, target weights renormalized | 0.606250 | 0.525000 | 0.081250 |
| Full target, missing cell at zero | 0.625000 | 0.420000 | 0.205000 |
| Full target, missing cell at one | 0.625000 | 0.620000 | 0.005000 |
| Full target, admissible bounds | 0.625000 | [0.420000, 0.620000] | [0.005000, 0.205000] |

On the covered sites with target weights renormalized, Slate's weighted rate was 0.606250, Amber's was 0.525000, and the Slate-minus-Amber contrast was 0.081250. [C5]

The protocol sets the intended population at 50 percent Basalt, 30 percent Linden and 20 percent Quartz and renormalizes over sites where both routes were used, making the covered-site contrast a renormalized subset rather than the full-target contrast. [C6]

With fixed target weights the full-target Slate rate is 0.625000, while Amber's full-target rate lies between 0.420000 and 0.620000 because the Quartz Amber cell is unobserved. [C7]

The full-target Slate-minus-Amber contrast therefore lies between 0.005000 and 0.205000, so its sign is positive throughout the protocol-admissible range. [C8]

The bound is the tightest the protocol allows. Writing the missing Quartz Amber rate as p, Amber's full-target rate is 0.420000 + 0.200000 p, so the contrast is 0.205000 - 0.200000 p. With p confined to the unit interval, the endpoints are 0.005000 at p equal to one and 0.205000 at p equal to zero; both endpoints are attainable, so no narrower interval follows from the protocol.

## What can and cannot be concluded

**Descriptively**, the registry supports saying that Slate's on-time rate among inspected tiles is higher than Amber's when standardized to the protocol's target site mix: +0.081250 on covered sites, and at least +0.005000 on the full target even under the most Amber-favorable admissible value of the missing cell. That is a statement about the supplied inspected tiles and the stated weights, not a population estimate with sampling error. The registry is a supplied extract with no documented sampling frame, and no confidence interval or hypothesis test is computed.

**Causally**, the registry does not identify a route effect. The protocol says dispatchers chose the route from current queue length and allocation was not randomized, so queue conditions and batch selection can differ between routes. The within-site ordering is consistent with a Slate advantage, but it is equally consistent with Slate being assigned easier queues or different tile mixes. No causal conclusion follows.

**For the missing cell**, the registry can bound the full-target contrast but cannot identify its point value, estimate the Quartz Amber rate, or import an external rate. The full-target point estimate is unidentified, and the covered-site +0.081250 is a different estimand from the full-target contrast. The bounds are deterministic arithmetic, not uncertainty intervals.

The registry comparison is descriptive, not causal, because dispatchers chose the route from current queue length and allocation was not randomized. [C9]

Protocol paragraph C rules out reading the missing Quartz Amber cell as a zero rate: an absent route–site combination means no observations were collected, not that every tile missed its deadline. [C10]

The newsletter's all-missed assertion is unsupported because its writer did not inspect the register or the protocol. [C11]

The newsletter goes further than the registry can support: it asserts that "The Slate roll-out almost certainly missed every deadline on the sites absent from the register." No observations exist for absent sites, and for the one absent route-site cell the protocol explicitly forbids treating absence as universal failure. The newsletter therefore cannot be used as evidence either for or against Slate.

## Limitations

- The eight batches are a supplied extract with no documented sampling frame, not a probability sample; the target-weighted values are standardized summaries, not population estimates.
- Route assignment was not randomized and depended on queue length, so confounding remains at both site and batch level.
- The Quartz Amber cell has no observations. The full-target point estimate and the Quartz Amber rate are unidentified; only the stated bounds follow from the protocol.
- The bounds assume the protocol's target weights are fixed and that the missing site-route rate is a proportion in the unit interval. They do not cover sampling variability, batch-to-batch variation or measurement error in the registry.
- No uncertainty model, confidence interval or significance test was specified or computed; the analysis is deterministic arithmetic on the supplied counts.

## Reproducibility

The runnable computation is `research/analyze.py`. It was run from the study root `/mnt` with:

```sh
python3 research/analyze.py
```

Exit status was 0. It reads `registry.csv` and writes the machine-readable table `research/results.csv`, whose SHA-256 digest is recorded in `research/run.json`. The frozen plan digest is in `research/plan.sha256`; claim-to-cell bindings are in `research/claims.json`. Primary-source quotations come from `registry-protocol.md` and `briefing.txt`, registered with digests in `research/sources.json`.
