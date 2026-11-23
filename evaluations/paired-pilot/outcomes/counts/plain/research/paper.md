# Slate vs Amber on-time processing — R-17 registry review

**Question.** Using the tile registry, can the cooperative conclude that Slate is
better than Amber for on-time processing in its intended service population
(50% Basalt, 30% Linden, 20% Quartz)?

**Bottom line.** A *descriptive, target-weighted* statement is supported: on the
two sites where both routes were used, Slate's weighted on-time rate is 60.63%
vs Amber's 52.50% (+8.13 pp), and under full target weights Slate's advantage is
positive for **every** value the missing Quartz–Amber cell could take
(+0.50 to +20.50 pp). But the *magnitude* is not identified, the naive all-site
pooled rate points the opposite way because route is confounded with site, and
nothing here supports a *causal* claim that Slate causes better on-time
processing.

## Evidence and method

Only three local files were used: `registry.csv`, `registry-protocol.md`
(R-17, paragraphs A–C), and `briefing.txt`.

- Protocol A: the outcome is delivery before the processing deadline; each tile
  was inspected once and batch totals are disjoint, so tile counts may be summed
  across batches. Route was chosen by dispatchers using current queue length and
  **allocation was not randomized**.
- Protocol B: target weights are Basalt 50%, Linden 30%, Quartz 20%; the
  denominator is **inspected tiles, not batches**; for covered sites retain only
  sites where both routes were used and renormalize the target weights.
- Protocol C: an absent route–site combination means **no observations**, not
  that every tile missed its deadline; no external performance rate is available
  for an unobserved combination.

Registry rows (all eight batches): K07 and K08 (Basalt/Slate), K01 and K05
(Basalt/Amber), K06 (Linden/Slate), K02 and K04 (Linden/Amber), K09
(Quartz/Slate). There is **no Quartz/Amber row**.

## Observed site–route rates

| Site | Route | Inspected | On time | Rate |
|---|---|---|---:|---:|---|
| Basalt | Slate | 120 | 48 | 40.00% |
| Basalt | Amber | 20 | 6 | 30.00% |
| Linden | Slate | 20 | 19 | 95.00% |
| Linden | Amber | 120 | 108 | 90.00% |
| Quartz | Slate | 20 | 14 | 70.00% |
| Quartz | Amber | 0 | 0 | unobserved |

**Within-site:** Slate exceeds Amber by +10.00 pp at Basalt and +5.00 pp at
Linden. Quartz has only Slate (70.00%), so it contributes no within-site
contrast.

**Observed all-site pooled (tiles pooled, ignoring site and target weights):**
Slate 81/160 = **50.63%**; Amber 114/140 = **81.43%**; difference **−30.80 pp**.
This pooled figure reverses the sign of every within-site comparison. The reason
is compositional: 120 of 140 Amber tiles (86%) are at Linden (a high-baseline
site), while 120 of 160 Slate tiles (75%) are at Basalt (a low-baseline site).
Pooling tiles therefore compares sites, not routes — a textbook confounding
(Simpson-type) artifact, not a population comparison.

## Target-weighted comparison on covered sites (protocol B)

Covered sites (both routes used): Basalt and Linden. Renormalized weights:
Basalt 0.50/0.80 = 0.625; Linden 0.30/0.80 = 0.375.

| Route | Basalt (0.625) | Linden (0.375) | Weighted rate |
|---|---:|---:|---:|
| Slate | 40.00% | 95.00% | **60.63%** |
| Amber | 30.00% | 90.00% | **52.50%** |

Covered-site contrast: **+8.13 pp** in favour of Slate. Quartz is correctly
excluded here because Amber was not used there.

## Full-target contrast and the missing cell

The full-target Slate rate is fully observed:
0.50(0.40) + 0.30(0.95) + 0.20(0.70) = **62.50%**.

The full-target Amber rate is not identified. Let *x* be the unobserved
Quartz/Amber on-time rate. Then

Amber = 0.50(0.30) + 0.30(0.90) + 0.20·*x* = 0.42 + 0.20·*x*,

and Slate − Amber = 0.625 − (0.42 + 0.20·*x*) = 0.205 − 0.20·*x*.

**Tightest bounds allowed by the protocol.** R-17 supplies no external rate and
no route-mix constraint for the unobserved combination (C), so the only
admissible statement is that *x* is a proportion, *x* ∈ [0, 1]. No tighter bound
follows from the registry. Hence:

- Amber full-target rate ∈ **[42.00%, 62.00%]**
- Contrast Slate − Amber ∈ **[+0.50, +20.50] pp**

The **sign is identified**: the contrast is positive across the entire admissible
range. Flipping it would require *x* ≥ 1.025, which is impossible for a
proportion. So the missing cell cannot *qualitatively* overturn "Slate higher,"
but it *quantitatively* leaves a 20-point-wide interval; the data cannot say
whether the true advantage is a fraction of a point or about 20 points.

What the full-target contrast **can** claim: Slate's target-weighted on-time rate
(62.50%) exceeds Amber's for every possible Quartz/Amber rate, by 0.50–20.50 pp.
What it **cannot** claim: a point estimate or a narrow interval for that gap, and
therefore any claim about its practical size.

## Descriptive vs causal

Everything above is **descriptive**. Protocol A states route assignment used
current queue length and was not randomized. Queue length plausibly affects both
route choice and on-time delivery, so the within-site differences mix any route
effect with dispatcher selection. With no randomization and no queue-length
adjustment, the cooperative may report that Slate *was associated with* higher
on-time rates under target weighting; it may **not** conclude that switching
tiles to Slate would *cause* the improvement, nor that Slate is intrinsically
faster. The missing Quartz/Amber cell and the small within-site counts (e.g.
Linden/Slate, n = 20) further limit inference.

The unsigned newsletter (`briefing.txt`) asserts Slate "almost certainly missed
every deadline on the sites absent from the register." That is unsupported on two
counts: all three target sites appear in the register (the gap is a route within
Quartz, not an absent site), and protocol C explicitly says absence means no
observations, not universal failure. The claim is also immaterial to the sign:
even if Quartz/Amber were 100% on time, Slate remains ahead by 0.50 pp.

## Reproducibility

Runnable, stdlib-only computation (no installs, no network): `compute.py` reads
`../registry.csv` and writes `results.csv` and `results.json`.

Actual command and output:

```
$ cd /mnt/research && python3 compute.py
R-17 registry analysis (denominator: inspected tiles)
site     route    insp  on_time     rate
Basalt   Slate     120       48   40.00%
Basalt   Amber      20        6   30.00%
Linden   Slate      20       19   95.00%
Linden   Amber     120      108   90.00%
Quartz   Slate      20       14   70.00%
Quartz   Amber       0        0      n/a

all-site pooled  Slate  50.62%  Amber  81.43%  diff -30.80 pp
covered weighted Slate  60.62%  Amber  52.50%  diff  +8.13 pp  (weights Basalt=0.625, Linden=0.375)
full target      Slate  62.50%  Amber [42.00%, 62.00%]  diff [+0.50, +20.50] pp  sign stable positive: True
wrote results.csv, results.json
```

Machine-readable result table (`results.csv`):

```
metric,site,route,inspected,on_time,rate,weight,notes
site_route,Basalt,Slate,120,48,0.400000,,
site_route,Basalt,Amber,20,6,0.300000,,
site_route,Linden,Slate,20,19,0.950000,,
site_route,Linden,Amber,120,108,0.900000,,
site_route,Quartz,Slate,20,14,0.700000,,
site_route,Quartz,Amber,0,0,,,unobserved
pooled_all_sites,all,Slate,160,81,0.506250,,tile-pooled; confounded by site mix
pooled_all_sites,all,Amber,140,114,0.814286,,tile-pooled; confounded by site mix
covered_weighted,covered,Slate,,,0.606250,Basalt=0.6250;Linden=0.3750,Basalt+Linden only
covered_weighted,covered,Amber,,,0.525000,Basalt=0.6250;Linden=0.3750,Basalt+Linden only
covered_diff,covered,Slate-Amber,,,0.081250,,positive => Slate higher
full_target,all,Slate,,,0.625000,1.0000,fully observed
full_target_bound,all,Amber,,,0.420000,,Quartz-Amber=0 lower bound
full_target_bound,all,Amber,,,0.620000,,Quartz-Amber=1 upper bound
full_target_diff_bound,all,Slate-Amber,,,0.005000,,at Quartz-Amber=1 (tightest low end)
full_target_diff_bound,all,Slate-Amber,,,0.205000,,at Quartz-Amber=0 (tightest high end)
```

### Verdict

- **Descriptive, covered sites (target-weighted):** Slate 60.63% vs Amber 52.50%,
  +8.13 pp — Slate higher.
- **Descriptive, full target:** Slate 62.50%; Amber 42.00–62.00%; Slate higher by
  0.50–20.50 pp for every admissible missing value — sign identified, magnitude
  not.
- **Pooled all sites:** Amber 81.43% vs Slate 50.63% — a site-confounded artifact,
  not usable for the population question.
- **Causal:** not established (non-random queue-based allocation, no adjustment,
  missing cell).
