---
name: ai4sci-experiment
description: Design, freeze, execute and compare computational experiments or paper reproductions, including controls, negative results and numerical tolerances. Use for 对照实验、复现、消融 or fair benchmarking.
---

# From hypothesis to results

Write `research/plan.json` before formal evaluation. Use the kit's `templates/plan.json` and `checks/contract.md`. Give criteria stable IDs. Specify the question, nearest comparison, unit of analysis, available-at-prediction-time inputs, primary metric/units/direction, tolerances, split or analytic reference, conditions held equal, uncertainty or deterministic rationale, compute cap and stopping rule. Distinguish exploration from confirmation; disclose data already inspected. Freeze the file with the kit's `freeze` command. A digest detects changes relative to this file; it is not an external timestamp. Store amendments separately rather than silently loosening a threshold.

Run a small pilot to check inputs and units. Execute the declared baseline and test under comparable conditions. Write `research/run.json` using the checkout's `checks/contract.md`: `status: "completed"`, `command` as the actual command string, and `outputs` as a list of project-relative result files including the CSVs you cite. Preserve execution settings and any remote job reference. For a fair comparison declare `matched_conditions` in the plan and record the observed values for each run arm. Compare siblings from a common baseline. Repair an environment failure on its existing run; do not repair a valid negative finding. Keep the independent test set out of the search loop. When budget runs out, stop and document untested criteria.

Select the comparison that answers the question: align tables by unique sample ID, check the entire ID set, and use prespecified tolerances rather than rounding until a comparison passes. `checks/compare.py --help` documents the offline comparison command. Treat changed grouping separately from merely renamed labels. Support conclusions with actual outputs rather than notebook prose.

For more involved rubrics, consult the vendored [criterion verification](references/autoscirub/criterion-level-verification.md) and [targeted revision](references/autoscirub/targeted-revision.md) protocols. Use this project's file contract and available roles; their upstream file/tool names are not requirements here.
