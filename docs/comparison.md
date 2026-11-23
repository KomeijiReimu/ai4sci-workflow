# Running and comparing studies

## Run the two-note study with your model

From the workflow checkout, run:

```sh
python3 scripts/live_study.py .local/study-01
```

Use a directory that does not already exist. The script needs Git and OpenCode on `PATH` and uses your configured model account. It installs the kit in a new study, copies the two numerical integration notes and gives OpenCode the [original task](../examples/opencode-study/REQUEST.md). The notes contain the mathematical derivations; the model supplies the experiment, results and manuscript.

On success, read `.local/study-01/study/research/paper.md` and `.local/study-01/audit.json`. The latter comes from the checker in the workflow checkout. To select a model, pass `--model provider/model`; `--timeout SECONDS` limits how long the script waits for OpenCode. If the run stops, its files and logs remain in `.local/study-01/`. Check them before starting another run. Keep the session logs private.

## Compare two workflows

Choose a task with an answer you can check independently:

| Task | Materials for the agent | What to check |
|---|---|---|
| Numerical study | The two [integration notes](../examples/opencode-study/inputs/) and a question about error on uniform grids | Are the criteria set before the run? Recompute the estimates and convergence rates, compare the figure with the CSV, and check that the conclusions apply to the grids and function tested. |
| Source-based review | The [review question](../examples/source-audit/REQUEST.md) and its two source notes | Locate the reference integral and each cited passage. Check whether the draft distinguishes what the notes derive for one quadratic from what they establish about other functions. |

For a scored comparison, reserve fresh task variants. Keep reference manuscripts, answer keys and previous solutions out of the agents’ workspaces and session context. Give both workflows the same inputs, model, tools, compute budget, attempt limit and time or token allowance. Agree on outputs both can produce and use the same grading criteria.

For each task, report the two outcomes side by side: unsupported or incorrect claims, missing evidence, whether the results could be reproduced, human corrections, elapsed time and model usage. Include unsuccessful attempts in the comparison.
