---
name: ai4sci-paper
description: Write a complete computational research manuscript from a study's actual results and literature; use for 论文初稿、摘要、方法、结果、讨论 or converting existing experiments into a paper.
---

# Draft from the evidence

Inventory each primary result, its raw output, figure/table and what it actually establishes. If the request starts with a results folder, reconstruct the study design from contemporaneous records; label retrospective criteria as retrospective. Do not call a reconstructed plan preregistered.

Outline the argument first: question and closest work → test that can answer it → finding → scope. Write a title, abstract, introduction/related work, methods (enough to rerun), results, discussion, limitations, and verified references. Include failed comparisons relevant to the main question. For a short study these may be compact sections. Draft the abstract last from verified results; do not broaden claims there. Use the requested language, notation and citation format.

For each conclusion-bearing empirical or literature claim, attach a stable `[C…]` marker and add the exact sentence to `research/claims.json` using the checkout's `checks/contract.md`. Identify the actual CSV key/column or source passage. State measured values, not heuristic confidence. Note uncertainty, units and scope where warranted. Link figures from the report, keep code that regenerates quantitative figures, and distinguish illustrations. Hand off the paper, claims and raw outputs to `ai4sci-review`.
