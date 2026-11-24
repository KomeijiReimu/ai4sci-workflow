# Choosing and comparing research workflows

Choose by what the next researcher needs to do: find the passage behind an answer, explore many possible experiments, resume a workspace, or recompute a result in a manuscript.

Use AI4Sci Workflow when a collaborator needs to check a manuscript from files in your own project directory. A formal computational study keeps its agreed criteria, run command, raw outputs and manuscript together. The [offline audit](../checks/contract.md) checks marked statements against specific CSV rows or quoted passages without executing the experiment.

The [reviewer](../skills/ai4sci-review/SKILL.md) looks for important unmarked claims, recalculates the decisive result from its inputs where possible, and judges whether the text goes beyond the evidence. The [workflow](../skills/ai4sci/SKILL.md) separates this responsibility from analysis and writing. With only one worker, the result is labeled self-checked.

## Which tool fits the task?

| Primary source | Useful when | What to check before adopting it |
|---|---|---|
| PaperQA2 ([2026-08-12 release](https://github.com/Future-House/paper-qa/releases/tag/v2026.08.12), [versioned guide](https://github.com/Future-House/paper-qa/blob/v2026.08.12/README.md)) | You have a collection of papers and want an answer with in-text citations. PaperQA2 retrieves, reranks and summarizes passages. | Inspect the cited passages for support. A cited value tells you what the paper reports. Reproducing it takes the underlying data and method. |
| [Kosmos](https://arxiv.org/abs/2511.02824) (Nov 2025) | You have a dataset and an open-ended objective. Parallel literature and analysis agents share findings through a structured world model. Reports cite code or papers. | The authors describe exploratory runs lasting up to 12 hours. Budget for discovery, then decide which findings warrant a separate confirmatory test. |
| [The AI Scientist-v2](https://arxiv.org/abs/2504.08066) (Apr 2025) | You want an agent to propose ML hypotheses, branch across experiments using tree search, and write a manuscript. | The [released implementation](https://github.com/SakanaAI/AI-Scientist-v2#readme) targets Linux with NVIDIA GPUs. Compare it on an ML task with an explicit compute budget. |
| [AutoSciRub](https://github.com/zjunlp/AutoSciRub/tree/2c6c58392ee6399e08f2526e35176f0e2c716e16/plugins/autoscirub/skills) (Oct 2026 revision) | A broad request needs concrete evaluation criteria. Its skills build a rubric, check artifacts against each criterion and direct repairs to missing evidence. | Read the rubric before execution: an omitted control can escape criterion-level review. AI4Sci reuses the verification and targeted-revision instructions. |
| [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/tree/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd) (Nov 2026 revision) | You want research skills that pair an executor with a reviewer using a different model. | Cross-model review needs a configured reviewer backend. AI4Sci separates reviewer and analyst responsibilities without prescribing a model pair. |

For work that spans sessions, compare the records each workbench keeps:

| Workbench (Nov 2026 revisions) | What a collaborator can use | Adoption consideration |
|---|---|---|
| [Open Science Desktop, AI4S Research](https://github.com/ai4s-research/open-science/tree/1dc2cbd8eb6b58887a1e6c41f80c797051f07700) | Named projects with persistent memory, searchable session history, notebooks and runs. | Useful when the next researcher needs to resume the investigation. Give an independent reviewer the design and outputs separately from the analyst's conversation. |
| [OpenScience, Synthetic Sciences](https://github.com/synthetic-sciences/openscience/tree/dbb60cba76afa518941a70ec4c25febba3114f4b) | A desktop, browser or terminal workspace that records searches, code and outputs and provides Python and R kernels. | Choose it when collaborators need an execution environment as well as files. For a manuscript handoff, identify which recorded run produced each reported result. |
| [OpenResearch, alphaXiv](https://github.com/alphaXiv/OpenResearch/tree/b74275826e1a5e2fb2c65cc6497d5683a1f07818/agent-skills/orx-experiment-tree) | An experiment tree whose child runs inherit the parent's code and run command. Completed nodes preserve good and bad outcomes. | Use the tree to compare variants. Check which conditions changed between the baseline and the branch cited in the paper. |
| [AIPOCH Open-Science](https://github.com/aipoch/open-science/tree/9d42705b02783d4ac96a55f183d3c99998e1ee13) | A portable `.science` package containing selected conversation branches, file versions, notebook records and verification evidence. | A recipient can inspect the sender's checks. For an independent reproduction, rerun the calculation and compare the outputs. |

The [peer comparison](../evaluations/maturity/peers.md) follows research decisions through versioned code, reports and output tables. It includes a recalculation of a bundled forecast and a test of what happens when a replay and its reference both omit the same observation. [Sources and reuse](../SOURCES.md) identifies which protocols and tools AI4Sci incorporates or adapts.

## Evaluation records (November 2026)

The [24 November maturity assessment](../evaluations/maturity/assessment.md) compares three workbenches by researcher task. Its reviewers accepted the implementation they examined but withheld the comparative claim: none of the five named leaderboard configurations had a complete comparison across all six research dimensions, against a requirement of at least three. [Checks of the selected peer archives](../evaluations/maturity/product-studies/archive-checks.md) identify which measurements could actually be recomputed. Publishing the workflow and its working examples is separate from a verdict about its overall standing.

- **Follow a result into a second comparison.** In the [German demand forecast study](../examples/power-forecast/), the archived day-ahead forecast beat the weekly baseline over the full year but lost on average during the busiest hours. The [follow-up](../examples/power-forecast/research/followup-decision.md) tested whether that reversal depended on using realized demand to select the hours. It reused the same year.
- **Follow a reviewer objection into the final document.** The [baseline amendment](../examples/penguins-revision/research/response.md) explains why a reviewer questioned the original constant predictor. The [rendered-file review](../examples/penguins-revision/research/independent-review.md) checks that the revised comparison and its limits appear in the delivered Word file. This was a development case using a known holdout.
- **Choose a question before doing the experiment.** Two researchers started from broad briefs on [urban cycling](../evaluations/research-decisions/cycling/amendment.md) and [stellar variability](../evaluations/research-decisions/stars/amendment.md). A [separate reader](../evaluations/research-decisions/amendment-review.md) found that the cycling test could lose a necessary comparison if even one date in its smallest group failed the weather or data checks. The stellar proposal narrowed its question to a difference in eclipse timing that the available observations can test. Neither experiment was run.
- **Check what the 19-byte result measures.** The [interleaved-counter example](../examples/branch-decision/) reports both the predictor that increased the payload size and the one that reduced it. A collaborator counted UTF-8 widths directly from the input without running the original encoder. The [returned manuscript](../evaluations/research-decisions/handoff/manuscript.md) and [reply](../evaluations/research-decisions/handoff/reply.md) explain that 19 bytes was the smallest payload on the one trace tested. That count excludes headers and assumes the recipient knows how to decode the payload.
- **Reopen a reviewer's concern.** The [two-round climate demonstrator](../examples/review-rounds/) uses real bulletin excerpts and illustrative correspondence. The archive preserves which reviewer objected to which passage, how the replies changed, and why the authors retained two estimates rather than replacing one with the other. It illustrates a revision process, not an external editorial decision.
- **Paired comparison.** The [pilot grades](../evaluations/paired-pilot/grades.md) compare plain OpenCode with AI4Sci on a registry analysis and a source-reading task. The [pilot method](../evaluations/paired-pilot/method.md) documents an omitted module that prevented the workflow from running its own audit. The [full-runtime comparison](../evaluations/paired-confirmation/results.md) uses fresh paired sessions on the same tasks and budget.
- **Complete-kit integration.** On a separate question, the [integration study](../evaluations/paired-pilot/integration/result.md) ran the computation, corrected a manuscript mismatch flagged by the audit, and passed the recheck. This run does not replace either pilot score.
- **DiscoveryBench.** On [public astronomy query 771](../evaluations/discoverybench-771/README.md), the submission missed the published hypothesis about galaxies with high dark-matter density. All 494 observed outcomes had the same value. An independent reviewer reproduced all 13 reported group contrasts.

## Run the two-note study with your model

Create `studies/integration-review/` in the workflow checkout. Put the [two integration notes](../examples/opencode-study/inputs/) in that directory as your source materials. Start `opencode` from the checkout root and ask:

> Read `skills/ai4sci/SKILL.md` and the stage instructions it refers to. Use `studies/integration-review/` as the working directory. Using only the two notes as sources, choose an error prediction to test on uniform grids. Set the criteria before the run, use a CPU and the Python standard library, and write a short paper in Chinese. Have another reviewer recompute the main results. Save the experiment, data, figure, paper and review in the study directory.

The notes supply the mathematical derivations. The experiment should compute the estimates on each grid and compare them with the predictions. Read `studies/integration-review/research/paper.md` and use the checkout's verifier to check the registered claims:

```sh
python3 ai4sci.py audit studies/integration-review
```

After the run, compare it with the [archived study](../examples/opencode-study/REQUEST.md). Its experiment summed the function values on each grid. The [independent reviewer](../examples/opencode-study/research/review.md) used the integer sum-of-squares formula to recompute all twelve estimates without calling the experiment code.

## Compare two workflows

Choose a task with an answer you can check independently:

| Task | Materials for the agent | What to check |
|---|---|---|
| Numerical study | The two [integration notes](../examples/opencode-study/inputs/) and a question about error on uniform grids | Are the criteria set before the run? Recompute the estimates and convergence rates, compare the figure with the CSV, and check that the conclusions apply to the grids and function tested. |
| Source-based review | The [review question](../examples/source-audit/REQUEST.md) and its two source notes | Locate the reference integral and each cited passage. Check whether the draft distinguishes what the notes derive for one quadratic from what they establish about other functions. |

For a scored comparison, reserve fresh task variants. Keep reference manuscripts, answer keys and previous solutions out of the agents’ workspaces and session context. Give both workflows the same inputs, model, tools, compute budget, attempt limit and time or token allowance. Agree on outputs both can produce and use the same grading criteria. Grade the substance of each claim even when the two workflows record it in different formats.

For each task, report the two outcomes side by side: unsupported or incorrect claims, missing evidence, whether the results could be reproduced, human corrections, elapsed time and model usage. Include unsuccessful attempts in the comparison.

For open-ended ML tasks, [MLR-Bench (NeurIPS 2025)](https://proceedings.neurips.cc/paper_files/paper/2025/hash/ab8dd000d6f87f40061a73f8bca7fae4-Abstract-Datasets_and_Benchmarks_Track.html) provides [tasks and review rubrics](https://github.com/chchenhui/mlrbench) for individual stages and for a finished paper. Report a rubric judgment separately from whether a reviewer could reproduce the reported result.
