# AI4Sci Workflow

[中文](README.md) · English · [Get started](#get-started) · [Read the studies](#completed-studies)

AI4Sci Workflow is a research workflow for [OpenCode](https://opencode.ai/). Start with a broad topic, a dataset, a draft or a reviewer's objection. For computational work, the protocol, code, commands and raw results stay in your study directory so a collaborator can repeat an analysis or revisit a conclusion during revision.

## Built-in research skills

| Task | Skill | What you get |
| --- | --- | --- |
| Start or resume a study | [`ai4sci`](skills/ai4sci/SKILL.md) | Selects the skills your question calls for. A reading-list request ends with the list. When you resume a study, it reads the design and results before choosing the next step. |
| Find papers or choose a question | [`ai4sci-idea`](skills/ai4sci-idea/SKILL.md) | An annotated reading list with sources. For a new study, it starts from a disagreement in the literature or an unexpected observation and proposes a small test that can distinguish competing explanations with the data available. |
| Run or reproduce an experiment | [`ai4sci-experiment`](skills/ai4sci-experiment/SKILL.md) | Sets the metric, conditions and budget up front, compares alternatives against the same baseline and keeps commands and raw results even for changes that did not help. It distinguishes sensitivity checks on a reused test set from independent confirmation. |
| Plot results | [`ai4sci-figures`](skills/ai4sci-figures/SKILL.md) | Plots drawn from result files, with units, a definition of any error bars and a command to regenerate the figure. You can also request a separate illustration of the method. |
| Write or revise a manuscript | [`ai4sci-paper`](skills/ai4sci-paper/SKILL.md) | A draft from existing results or a submission in the venue's format (Word, or LaTeX source and compiled PDF). For a paper written elsewhere, start with the submitted version, reviewer comments and available records. Plan any new comparison before running it, then cite the results in the revision and point-by-point response. |
| Check the findings | [`ai4sci-review`](skills/ai4sci-review/SKILL.md) | Checks citations against the original passages and recalculates key metrics from the data. The review identifies the passage and evidence behind each concern and which claims need narrower wording or another test. |

---
## Collaboration and continuity

For a [study aimed at publication](skills/ai4sci/references/publication.md), the lead agent in [omo-slim](https://github.com/alvinunreal/oh-my-opencode-slim) assigns work to the roles available in your configuration:

- **Choosing a question.** Two Explorer agents or their equivalents work in parallel. One checks what the target venue has published recently and looks for prior answers elsewhere. The other checks the data, controls and compute costs. The lead asks Oracle or another configured scientific reviewer to challenge the leading idea with the strongest counterevidence. If you asked only for an idea, you get the recommendation and the reasoning here.
- **Running the study.** The methods reviewer checks the baseline, data split and metrics before the investigator runs and analyzes the comparison. Before drafting, the same reviewer interprets the first decisive result and weighs competing explanations. The lead brings that reviewer back if the comparison or the main conclusion changes materially.
- **Delivering the manuscript.** The writer drafts from the measured results. The lead opens a fresh session with a strong scientific reviewer who took no part in methods review, analysis or writing. That reviewer recalculates key results from the original materials, checks the exact manuscript to be delivered and reviews any corrections to the issues they raised. Work done by a single agent is labeled self-checked.

**If you ask only for a [remote experiment package](skills/ai4sci/references/remote-package.md)**, the workflow prepares code and launch instructions without running the experiment locally or remotely. Before coding starts, the lead asks a methods specialist to look for flaws that could invalidate the comparison. The same reviewer returns if the implementation materially departs from the design.

Before handoff, the lead selects two reviewers whose configured models suit their specialties and opens a fresh session for each. Neither helped design the study or write the package. They inspect the same final package: one checks that the code implements the agreed controls and metrics, and the other checks dependencies, data paths and remote launch instructions. An author's check is labeled a self-check. Any independent review that has not returned stays pending.

With [Magic Context](https://docs.cortexkit.io/magic-context/getting-started/introduction/) enabled, you can return to a long session days later and find the discussion behind a baseline choice. A new session in the same OpenCode project can recall the decisions and reasons saved in project memory.

To hand a multi-session study to a colleague, share the study directory. Its `research/handoff.md` records progress, evidence locations and the next step, as in the [electricity forecast handoff](examples/power-forecast/research/handoff.md).

---
## Get started

The repository includes the six research skills. All your studies can use the same checkout without an initialization step or a local copy of the skills. Configure a model in OpenCode, then clone the repository:
```sh
git clone https://github.com/KomeijiReimu/ai4sci-workflow.git
cd ai4sci-workflow
pwd
```

Run `opencode` from the repository root and say what you want to study and how far you want to take it. For papers only, try “Use ai4sci to give me a reading list on day-ahead load forecasting.” If you're aiming for publication, you can name a venue or give a target category such as CCF B:

> Use ai4sci to suggest a day-ahead load forecasting question for ACM e-Energy.

> Use ai4sci to design and run a day-ahead load forecasting study and write it up for ACM e-Energy.

> Use ai4sci to prepare a day-ahead load forecasting experiment package for my cluster without running it.

When a new study needs files, OpenCode gives it its own directory under `studies/`. Literature, experiments and manuscripts for the same study stay in that directory. If it's clear which study you mean, just say what you want to do next. Otherwise, OpenCode asks which study to resume before writing any files. This repository ignores study files under `studies/` by default.

To work in your own study directory, run `opencode` there. Replace the path in this prompt with the checkout path printed by `pwd`:

> Read `/path/to/ai4sci-workflow` and use it to revise the submitted Word manuscript in this directory. Address the reviewer comments and give me the revision and a point-by-point response.

---
## Literature search and document tools

For literature searches and citation trails, we recommend paper-search MCP. Check your existing connections with `opencode mcp list`. If the server is not configured, use [uv](https://docs.astral.sh/uv/) to install the [upstream revision used here](https://github.com/openags/paper-search-mcp/tree/cab1b5cc276a0cd004a0044003926a6440088049), then register it globally in OpenCode 2:
```sh
uv tool install git+https://github.com/openags/paper-search-mcp.git@cab1b5cc276a0cd004a0044003926a6440088049
opencode mcp add paper-search --global -- "$(uv tool dir --bin)/paper-search-mcp"
opencode mcp list
```

Look for `paper-search connected`, and if the list is empty on startup, wait a few seconds and run `opencode mcp list` again in the same project directory.

To look up a citation in OpenCode, ask:

> Use paper-search to look up DOI `10.3390/math12010019` in Crossref. Check the title, authors and journal of this paper on day-ahead load forecasting in Europe.

We recommend [`paper-reader`](https://github.com/KomeijiReimu/my-skills) for close reading. Choose [document skills](https://github.com/anthropics/skills) to suit the files you work with: `docx` for Word templates, `xlsx` for Excel supplements, `pdf` for checking page layouts and `pptx` for presentation slides. Use [Bun](https://bun.sh) to install them for OpenCode at user scope. Include only the skill names you need and don't already have:
```sh
bun x skills add KomeijiReimu/my-skills -g -a opencode --skill paper-reader
bun x skills add anthropics/skills -g -a opencode --skill docx xlsx pdf pptx
```

---
## Completed studies

- [When did last week's load beat Germany's day-ahead forecast?](examples/power-forecast/) Across 8,756 paired hours in 2019, the day-ahead forecast had 540 MW lower mean absolute error. In the 876 hours of highest realized demand, its error was 159 MW higher. When the midpoint of the two forecasts defined the high-demand group instead, the day-ahead forecast still had 161 MW higher error in that group.
- [Why two assessments of global warming in 2024 give different estimates](examples/climate-sources/research/paper.md) (in Chinese). The World Meteorological Organization combined several datasets, while the Copernicus Climate Change Service reported an estimate from the ERA5 reanalysis. The review traces both estimates to the bulletins and explains why a single year does not establish whether a long-term temperature goal has been exceeded. See the [source records](examples/climate-sources/research/sources.json).
- [Responding to a baseline objection](examples/penguins-revision/research/response.md). The [original penguin study](examples/penguins/research/paper.md) used mean training mass as the constant predictor. A reviewer pointed out that the median minimizes absolute error on the training data. Against that baseline, the flipper-length model's advantage in mean absolute error narrowed from about 385 g to 372 g on the same observations. The [revised Word manuscript](examples/penguins-revision/paper/final.docx) identifies this as a sensitivity analysis on the previously examined 2009 records.

[Choosing a research workflow](docs/comparison.md) · [Evidence checks](checks/contract.md) · [Checking a submission](checks/submission.md) · [Drawing a methods illustration (Chinese)](integrations/codex-image/guide.md) · [Sources and licenses](SOURCES.md)
