# AI4Sci Workflow

[中文](README.md) · English · [Read the studies](#completed-studies)

AI4Sci Workflow is a research workflow for [OpenCode](https://opencode.ai/). Use it to explore the literature, choose a question and design an experiment, analyze observations you have already collected, or write up existing results. For computational experiments and reproductions, the protocol, code, commands and raw results stay in your study directory so you can resume the work and others can repeat the analysis.

## How the workflow helps

- **Define the question and the comparison up front**. The workflow weighs prior work and available data to identify what a new experiment could answer. You can stop with a reading list or a shortlist of ideas. If you go on to an experiment, the workflow records the dataset, baseline and evaluation criteria before the run. The report distinguishes a result that failed to reproduce from one that could not be tested because data were missing.
- **Trace claims to their sources**. Before delivery, the checker compares measurements marked in the draft with the result tables and checks cited numbers against saved source excerpts. A reviewer considers the population and conditions studied to judge whether the conclusions go beyond the evidence.
- **Share the work across agents**. With [omo-slim](https://github.com/alvinunreal/oh-my-opencode-slim), a multi-agent plugin for OpenCode, one agent can look for prior work and counterevidence while another inspects the available data. The lead agent coordinates their work, so you don't have to brief each agent or relay the findings. An agent who did not run the experiment or write the draft can use the protocol and original materials to recompute key metrics, then compare those values with the manuscript.

---
## Get started

Configure a model in OpenCode and clone this repository. You can use the same checkout for multiple studies:
```sh
git clone https://github.com/KomeijiReimu/ai4sci-workflow.git
cd ai4sci-workflow
pwd
```

To work in the workflow checkout, run `opencode` from the repository root and describe what you want to study:

> Use ai4sci to find papers on handling missing values in time series and suggest a few questions worth testing.

When a new study needs files, OpenCode creates a directory under `studies/`. To resume an existing study, give its directory (for example, `studies/my-study/`) and say what you want to do next. Git ignores your study files by default.

To work in your own study directory, run `opencode` there. Replace the path in this prompt with the checkout path printed by `pwd`:

> Read `/path/to/ai4sci-workflow` and use its workflow to write a short paper from the experimental results in this directory.

The manuscript is saved at `<study-directory>/research/paper.md`. The evidence check that OpenCode runs before delivery requires Python 3.10 or later.

---
## Completed studies

- [Predicting penguin body mass from flipper length](examples/penguins/research/paper.md). Both models were fitted on two years of observations and tested on the same 119 complete observations from 2009. Predicting the training mean gave a mean absolute error of about 710 g, compared with 326 g for a linear prediction from flipper length. See the [row-level predictions](examples/penguins/research/predictions.csv) and [independent review](examples/penguins/research/review.md).
- [Why two assessments of global warming in 2024 give different estimates](examples/climate-sources/research/paper.md) (in Chinese). The World Meteorological Organization combined several datasets, while the Copernicus Climate Change Service reported an estimate from the ERA5 reanalysis. The review traces both estimates to the bulletins and explains why a single year does not establish whether a long-term temperature goal has been exceeded. See the [source records](examples/climate-sources/research/sources.json).

[Choosing a research workflow](docs/comparison.md) · [Evidence checks](checks/contract.md) · [From two notes to a short paper](examples/opencode-study/REQUEST.md) · [Drawing a methods illustration (Chinese)](integrations/codex-image/guide.md) · [Sources and licenses](SOURCES.md)
