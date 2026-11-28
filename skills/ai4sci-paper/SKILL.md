---
name: ai4sci-paper
description: Draft a research manuscript from results and literature, produce a venue-specific Word or LaTeX submission, or turn a reviewer concern into a scoped supplement, revised paper and response. Use for 论文初稿、投稿、返修、改投 or editing a paper from existing experiments.
---

# Draft from the evidence

For a manuscript intended for submission, arrange the [independent final review](../ai4sci/references/publication.md) of the requested deliverable as part of the writing assignment.

For a manuscript from outside this workflow, start with [submission and revision](references/submission.md). Preserve the supplied files and revise a new copy in the requested format. Hand the exact revised manuscript, reply and cited material to `ai4sci-review`. A supplied Word or PDF does not need a reconstructed plan or run record. If the revision calls for a new comparison, keep its plan, results and audit in a separate supplement.

Inventory each primary result, its raw output, figure/table and what it actually establishes. If the request starts with a results folder, reconstruct the study design from contemporaneous records. Label retrospective criteria as retrospective. Do not call a reconstructed plan preregistered.

Outline the argument first: question and closest work → test that can answer it → finding → scope. Write a title, abstract, introduction/related work, methods (enough to rerun), results, discussion, limitations, and verified references. Include failed comparisons relevant to the main question. For a short study these may be compact sections. Draft the abstract last and keep its claims within the scope of the verified results. Use the requested language, notation and citation format.

For a formal study conducted with this kit, attach a stable `[C…]` marker to each conclusion-bearing empirical or literature claim and add the exact sentence to `research/claims.json` using the checkout's `checks/contract.md`. Identify the actual CSV key/column or source passage. State measured values, not heuristic confidence. Note uncertainty, units and scope where warranted. Link figures from the report, keep code that regenerates quantitative figures, and distinguish illustrations. Hand off the paper, claims and raw outputs to `ai4sci-review`.

If the request names a final file, venue, reviewer comments, or a previous submission, follow [submission and revision](references/submission.md). For follow-up reviews, keep each previous manuscript and reply and link the new comments to the issues they reopen. Review the exact version handed over. For a question about a passage or an initial draft, stop at that deliverable.
