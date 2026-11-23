# Slate versus Amber for on-time tile processing: a bounded reanalysis of registry R-17

## Summary

The signed registry supports a **descriptive** conclusion that Slate is better than Amber for on-time tile processing in the cooperative's intended service population, but not a causal one. The naive all-site pooled comparison points the other way because the two routes served very different site mixes. On the two sites where both routes were used, protocol-weighted rates favour Slate, and the missing 20 percent Quartz-Amber cell cannot reverse the sign for any rate the protocol allows. Route assignment was by queue length, not randomization, so the contrast is an association among recorded tiles.

## Question and primary evidence

The question is whether the cooperative can conclude that Slate is better than Amber for on-time processing in its intended service population. The only evidence used is the supplied study set.

- `registry.csv` — eight batch records covering 300 inspected tiles, with counts by site and route.
- `registry-protocol.md` — signed protocol R-17, paragraphs A–C (the primary methods record).
- `briefing.txt` — an unsigned newsletter written from a dispatcher's recollection; it is a claim to be assessed, not data.

Protocol A fixes the outcome as delivery of an inspected tile before its processing deadline, states that each tile was inspected once and that batch totals are disjoint, and records that dispatchers chose the route using current queue length with no randomization. Protocol B sets the intended service population to 50 percent Basalt, 30 percent Linden and 20 percent Quartz, requires inspected tiles rather than batches as the denominator, and requires covered-site weights to be renormalized over sites where both routes were used. Protocol C states that an absent route–site combination means no observations were collected, not that every tile missed its deadline, and that no external performance rate exists for an unobserved combination.

Key protocol text:

> A. "Each tile was inspected once. Batch totals are disjoint. Dispatchers chose the route using current queue length; allocation was not randomized."
>
> B. "The intended service population is 50 percent Basalt, 30 percent Linden and 20 percent Quartz. Within each site, use inspected tiles, not batches, as the denominator. For the covered-site calculation retain only sites where both routes were used and renormalize target weights."
>
> C. "An absent route–site combination means no observations were collected, not that every tile missed its deadline. No external performance rate is available for an unobserved combination."

## Method

For site *s* and route *r*, let *k* be on-time inspected tiles and *n* inspected tiles, so the site-route rate is *k*/*n*. Batch rows are summed within a site-route cell because batch totals are disjoint (protocol A). The all-site pooled rate sums *k* and *n* across observed cells; it is not target-weighted. The covered-site target-weighted rate is

  *R*<sub>*r*</sub> = Σ<sub>*s*∈covered</sub> [ *w*<sub>*s*</sub> / Σ<sub>*c*∈covered</sub> *w*<sub>*c*</sub> ] · (*k*<sub>*sr*</sub>/*n*<sub>*sr*</sub>),

with target weights *w* from protocol B. The full-target rate uses all three sites and the original weights. Because the Quartz-Amber cell is unobserved, its rate *p* is not estimated; it is varied over the complete protocol-permitted set [0, 1]. The reported full-target contrast is Slate minus Amber. Arithmetic is exact rational arithmetic; `research/results.csv` is the machine-readable table of every quantity below. The registry is a signed census of recorded batches, so the intervals reported here are missing-cell bounds, not sampling confidence intervals.

## Results

### Observed site rates

**Table 1.** On-time inspected tiles / inspected tiles (rate), by site and route.

| Site | Slate | Amber |
|---|---|---|
| Basalt | 48/120 (0.400) | 6/20 (0.300) |
| Linden | 19/20 (0.950) | 108/120 (0.900) |
| Quartz | 14/20 (0.700) | not observed |
| Pooled (each route's observed cells) | 81/160 (0.506) | 114/140 (0.814) |

Within Basalt, the Slate on-time rate is 0.4 and the Amber rate is 0.3. [C1]

Within Linden, the Slate on-time rate is 0.95 and the Amber rate is 0.9. [C2]

The only Quartz cell with observations is Slate, at an on-time rate of 0.7. [C3]

### The pooled comparison reverses the within-site ordering

Pooled across observed sites, Slate is 81 of 160 on time for a rate of 0.506, while Amber is 114 of 140 for a rate of 0.814. [C4]

The pooled reversal reflects site mix: 0.75 of Slate tiles are from Basalt, whereas 0.857 of Amber tiles are from Linden. [C5]

This is Simpson's paradox in the registry. Basalt is the low-performing site and Linden the high-performing one. Slate's pooled total is dominated by Basalt, where its own rate is only 0.400; Amber's pooled total is dominated by Linden, where its rate is 0.900. The pooled difference therefore describes two differently composed groups, not the intended service population, and it does not answer the cooperative's question.

### Target-weighted comparison on covered sites

Both routes were used at Basalt and Linden, so protocol B requires renormalizing their 50 and 30 percent target weights over the 80 percent covered by both routes.

**Table 2.** Protocol-weighted rates and the full-target bounds.

| Quantity | Value |
|---|---|
| Covered-site weight, Basalt | 0.625 |
| Covered-site weight, Linden | 0.375 |
| Covered target-weighted Slate rate | 0.606 |
| Covered target-weighted Amber rate | 0.525 |
| Covered Slate-minus-Amber contrast | +0.081 |
| Full-target Slate rate | 0.625 |
| Full-target Amber rate | [0.420, 0.620] |
| Full-target Slate-minus-Amber contrast | [+0.005, +0.205] |
| Quartz-Amber rate needed for parity | 1.025 |

On covered sites the renormalized weights are 0.625 for Basalt and 0.375 for Linden, and the target-weighted rates are 0.606 for Slate and 0.525 for Amber, a difference of 0.081. [C6]

The covered-site comparison is the cleanest descriptive contrast available: it holds the site fixed, uses the protocol's population weights, and includes every site where the routes can be compared. It still covers only 80 percent of the target population.

### The full-target contrast with the missing cell

Slate is observed at all three target sites: 0.5(0.400) + 0.3(0.950) + 0.2(0.700) = 0.625. Amber is observed at Basalt and Linden: 0.5(0.300) + 0.3(0.900) = 0.420, plus 0.2*p for Quartz Amber. Protocol C forbids substituting an external rate, so the only admissible values are *p* ∈ [0, 1]. Hence the full-target Amber rate lies in [0.420, 0.620] and the contrast lies in [0.005, 0.205].

Over the protocol-permitted interval, the full-target Amber rate is bounded between 0.42 and 0.62, so the Slate-minus-Amber contrast lies between 0.005 and 0.205. [C7]

Parity would require a Quartz Amber on-time rate of 1.025, above the permitted maximum of 1. [C8]

Both endpoints are attainable, at *p* = 1 and *p* = 0, so no narrower interval follows from the protocol. The full-target contrast **can** establish the direction of the difference for the intended population and a range for its size: Slate is ahead at every admissible value of the missing cell, by at least 0.005 and at most 0.205. It **cannot** produce a point estimate of the full-target Amber rate or of the contrast; it cannot say how well Amber would have performed at Quartz; and it cannot establish equality or Amber superiority without a Quartz-Amber rate above 1, which is impossible. The 0.005 lower bound is the least favourable admissible case, so the direction is robust but the minimum margin is small. If the absent Amber cell were instead set to zero on-time work, the contrast would sit at its upper bound, widening Slate's advantage.

## Interpretation: descriptive, not causal

Because dispatchers chose the route using current queue length and allocation was not randomized, the contrast is descriptive rather than causal. [C9]

The protocol supplies no randomization, no queue measurements and no tile-difficulty covariates. Slate may have been dispatched when queues were shorter or tiles were easier, so the within-site gaps cannot be attributed to the route itself. The covered-site and full-target calculations therefore estimate how the recorded tiles performed under the observed dispatch practice; they do not estimate what would happen if the cooperative assigned Slate to tiles now handled by Amber. The defensible descriptive claim is that, among recorded tiles and under the protocol's target weights, Slate's on-time rate exceeds Amber's and the sign survives the missing cell. A causal claim about switching routes is not supported.

## The unsigned newsletter

The target population named in protocol B is Basalt, Linden and Quartz, and the register contains records for all three sites. [C10]

The newsletter's claim that Slate missed every deadline on sites absent from the register conflicts with protocol C, which says an absent route–site combination means no observations, not that every tile missed its deadline. [C11]

The register has no absent site: Basalt, Linden and Quartz all appear (Table 1). The only unobserved cell is the Quartz-Amber route–site combination — and it belongs to Amber, not Slate; Slate's Quartz cell is observed at 0.7. Protocol C explicitly rules out reading that absence as zero on-time work. The newsletter's premise therefore has no referent in the register, and its implied conclusion is not evidence about Slate. If the absent Amber cell were set to zero on-time work, the full-target contrast would move to its upper bound, widening Slate's advantage; the missing cell cannot be converted into evidence against Slate. The newsletter was written from recollection without inspecting the register or protocol, so it should not be used as primary evidence.

## Limitations

- **No causal identification.** Route assignment followed queue length; site, time and tile difficulty may confound the contrast.
- **Census, not sample.** The registry records the cooperative's batches; no sampling model or confidence interval is claimed. The reported intervals concern the missing cell only.
- **One missing cell.** The bounds use only *p* ∈ [0, 1] because protocol C forbids an external rate. A defensible external Quartz-Amber rate would tighten them but is unavailable.
- **Sparse cells.** The Linden-Slate and Quartz-Slate cells each contain 20 inspected tiles, so their site rates are imprecise even as descriptive summaries.
- **Pooled rates are not population rates.** The all-site pooled figures reflect the routes' different site mixes and should not be read as target-population performance.

## Reproduction

From `/mnt`, the computation was run as:

```sh
python3 research/analyze.py
```

It reads `registry.csv` and the target weights in `registry-protocol.md` and writes `research/results.csv` (23 rows, one per reported quantity). Input and output SHA-256 digests, the plan digest and the Python version are recorded in `research/run.json`; the plan is in `research/plan.json`. No network, installs or external data were used.

The workflow's `audit` command was attempted but could not execute: the local checkout at `/media` lacks `checks/sources.py`, so `ai4sci.py` fails at import with `ModuleNotFoundError: No module named 'checks.sources'`. The same missing module prevented `ai4sci.py freeze`; `research/plan.sha256` was therefore written as the SHA-256 of the raw plan bytes plus a single LF, which is the digest that command defines. The claim ledger was checked locally against the manuscript and result table by exact string and numeric comparison.

## Primary sources

1. Lattice Imaging Cooperative. *Registry protocol R-17*, paragraphs A–C (`registry-protocol.md`).
2. Lattice Imaging Cooperative. *Tile registry extract* (`registry.csv`), eight batch records.
3. Unsigned logistics newsletter (`briefing.txt`), dispatcher recollection; assessed, not used as data.
