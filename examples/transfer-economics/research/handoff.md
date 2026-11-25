# Study handoff

**Question.** Does faster GDP per capita growth mark larger life-expectancy gains among economies with similar initial longevity and income in the same region? A GDP–HDI comparison alone cannot separate health from the income component of the index. A mortality-inequality measure such as HLI would require life tables absent from this panel.

**Design.** The [plan](plan.json) was frozen locally on 2026-11-25 at 02:47:24.788407 UTC, before inspection of the outcome rows for this analysis ([SHA-256](plan.sha256)). A 95% interval wholly above six months would support a material gradient; one wholly below it would rule out a gradient that large. An interval crossing the threshold leaves its materiality unresolved.

**Finding.** For 192 economies, the adjusted gradient was +1.37 years of life expectancy gained per 1.5-fold difference in GDP growth factors (95% interval 0.45–2.29). The direction is positive; the six-month threshold remains unresolved. The nonlinear specification clears the threshold; omitting East Asia and Pacific makes the interval include zero. This is an observational result, not a causal estimate.

**Use.** [Manuscript](paper.md) · [estimates](estimates.csv) · [sample coverage](coverage.csv) · [evidence ledger](claims.json) · [data and rights](../provenance/README.md) · [replay script](../replay.sh) and [instructions](../README.md) · [independent scientific review](independent-review.md).
