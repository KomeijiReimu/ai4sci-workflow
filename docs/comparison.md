# Running and comparing studies

## Run the two-note study with your model

Create `studies/integration-review/` in the workflow checkout. Put the [two integration notes](../examples/opencode-study/inputs/) in that directory as your source materials. Start `opencode` from the checkout root and ask:

> Read `skills/ai4sci/SKILL.md` and the stage instructions it refers to. Use `studies/integration-review/` as the working directory. Using only the two notes as sources, choose an error prediction to test on uniform grids. Set the criteria before the run, use a CPU and the Python standard library, and write a short paper in Chinese. Have another reviewer recompute the main results. Save the experiment, data, figure, paper and review in the study directory.

The notes supply the mathematical derivations. The experiment should compute the estimates on each grid and compare them with the predictions. Read `studies/integration-review/research/paper.md` and use the checkout's verifier to check the registered claims:

```sh
python3 ai4sci.py audit studies/integration-review
```

The [archived study](../examples/opencode-study/REQUEST.md) includes a manuscript, raw data and an independent recalculation for comparison after the run.

## Compare two workflows

Choose a task with an answer you can check independently:

| Task | Materials for the agent | What to check |
|---|---|---|
| Numerical study | The two [integration notes](../examples/opencode-study/inputs/) and a question about error on uniform grids | Are the criteria set before the run? Recompute the estimates and convergence rates, compare the figure with the CSV, and check that the conclusions apply to the grids and function tested. |
| Source-based review | The [review question](../examples/source-audit/REQUEST.md) and its two source notes | Locate the reference integral and each cited passage. Check whether the draft distinguishes what the notes derive for one quadratic from what they establish about other functions. |

For a scored comparison, reserve fresh task variants. Keep reference manuscripts, answer keys and previous solutions out of the agents’ workspaces and session context. Give both workflows the same inputs, model, tools, compute budget, attempt limit and time or token allowance. Agree on outputs both can produce and use the same grading criteria.

For each task, report the two outcomes side by side: unsupported or incorrect claims, missing evidence, whether the results could be reproduced, human corrections, elapsed time and model usage. Include unsuccessful attempts in the comparison.
