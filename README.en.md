# AI4Sci Workflow

[中文](README.md) · English · [Read the studies](#completed-studies)

AI4Sci Workflow is a research workflow for [OpenCode](https://opencode.ai/). Start with a broad topic, a dataset, a draft or a reviewer's objection. For computational work, the protocol, code, commands and raw results stay in your study directory so a collaborator can repeat an analysis or revisit a conclusion during revision.

## Where to start

- **Find papers or choose a question**. Ask for an annotated reading list or start with a disagreement between papers, an unexpected observation or a decision you need to make. The workflow checks what the closest original studies already answered and whether the available data can distinguish the remaining explanations. You can stop with a recommended question and a low-cost test.
- **Run an experiment or reproduce a finding**. Agree on the baseline, comparison conditions, metric and budget first. Test competing changes separately against the same baseline and keep each result, including negative findings. If a result fits two explanations, choose a follow-up on which their predictions differ. A previously examined test set can show how sensitive an estimate is to an analysis choice. Independent confirmation requires data that did not guide selection or tuning.
- **Write, prepare a submission or respond to reviewers**. Start from existing results or supply the venue's requirements and template for a Word manuscript or LaTeX source with a compiled PDF. To revise a paper written elsewhere, bring the submitted version, the reviewer comments and whatever study records you have. Cite existing results where they answer a comment. If a new comparison is needed, record its plan separately before running it and save the results. Update the affected passages and figures and explain the changes in the response letter.

With [omo-slim](https://github.com/alvinunreal/oh-my-opencode-slim), a multi-agent plugin for OpenCode, one agent can look for the closest papers and counterevidence while another checks the data and compute requirements. The lead agent coordinates them. An agent who did not run the experiment or write the draft can recompute the decisive result from the inputs and check whether the claim holds for the population and conditions studied.

---
## Get started

The repository includes the six research skills. All your studies can use the same checkout without an initialization step or a local copy of the skills. Configure a model in OpenCode, then clone the repository:
```sh
git clone https://github.com/KomeijiReimu/ai4sci-workflow.git
cd ai4sci-workflow
pwd
```

To work in the workflow checkout, run `opencode` from the repository root and describe what you want to study:

> Use ai4sci to look for studies of short-term electricity demand forecasts with gaps in the input series. Find the closest comparison and a usable dataset. Recommend a small first experiment, but don't run it yet.

When a new study needs files, OpenCode creates a directory under `studies/`. To resume an existing study, give its directory (for example, `studies/my-study/`) and say what you want to do next. Git ignores your study files by default.

To work in your own study directory, run `opencode` there. Replace the path in this prompt with the checkout path printed by `pwd`:

> Read `/path/to/ai4sci-workflow` and use it with the reviewer comments and the submitted Word manuscript in this directory. Check whether our existing results answer the requested comparison, then prepare the revised manuscript and a point-by-point response.

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
