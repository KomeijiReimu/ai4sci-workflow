---
name: ai4sci-review
description: Independently check a scientific draft against sources, data and frozen comparisons; recompute important numbers, identify unsupported conclusions and issue an actionable review. Use for 核引用、核稿、统计审查、复算 or pre-delivery review.
---

# Review the evidence

Read the frozen criteria, draft, raw results, code and actual source passages. First find important **unmarked** assertions, especially in the abstract, results and conclusions; a machine can only check the claims someone declared. Compare populations, data splits, denominators, effect size and units, direction of change and how broadly each sentence is worded. Resolve a DOI to metadata before trusting attribution. A matching quote alone does not establish entailment. Recompute at least the decisive metric independently from its inputs where possible.

Run the installed `audit` on the project; report its exit code and failures. On statistical studies optionally run `ai4sci.py stats` on explicit code/report/plan paths. Review the actual findings; absence of a preregistration document means adherence was not checked. Check multiple comparisons or causal inference where relevant. A lint result is not a scientific verdict.

For each issue give the claim/criterion ID, evidence location, what conflicts or is missing, consequence and smallest repair. Separate blockers from observations. Give three answers: did execution finish, which claims are supported (or narrower/contradicted/untested), and is the manuscript honest and ready to deliver? A completed run with a well-supported failure to replicate can yield a deliverable report. Return issues to the original owner for one targeted repair and recheck; retain outstanding issues instead of declaring success.
