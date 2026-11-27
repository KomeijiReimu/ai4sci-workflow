---
name: ai4sci
description: Help with a research question, literature search, study design, analysis, reproduction or evidence-checked manuscript. Use for 文献调研、选题、研究设计、计算实验、复现、查证据、写研究报告 or resuming an existing study. Enter or stop at the requested stage.
---

# Run a study

The user's request can be just a checkout path and a research goal. Resolve `KIT` from this file's location and read the relevant `$KIT/skills/<name>/SKILL.md`. Do not install tools, copy skills or edit project configuration to start a study.

## Choose the study directory

- **New study:** From the checkout, create an unused `studies/<topic>/` only when the task needs files. If the natural name is taken, choose a more specific name rather than reusing the occupied folder. A reading list returned in chat needs no directory. From an external project, use the user's current study directory as `STUDY`.
- **Continuing a study:** Use the directory the user names, or reuse the one clearly identified by the conversation and its local records. Switching from reading to analysis, figures or writing does not start a new study. If the intended directory is unclear, inspect the names and handoffs read-only. If several fit, show those paths and ask which one; if none fit, ask for the location. Do not create files, dispatch writers or run experiments until the study is identified.
- **Working in the selected study:** Give collaborators the resolved `KIT` and `STUDY` paths. Run experiments from `STUDY` and keep task outputs there. Use project memory to find leads; verify study-specific decisions and results against this study's records. When reusing material from a different study, cite its source and version, leave the original untouched and write any derived files in the receiving study.

## Choose the work

Start at the stage the goal needs. A request to find papers can end with an annotated reading list. A request for ideas can end with candidate questions, their closest prior work and a feasible first test. Use the available search tools when the user has supplied only a topic. Neither quick request needs a manuscript, experiment run record or handoff. For field, laboratory or observational work, help design the protocol and analyze supplied measurements. Identify who must collect missing observations; do not report a proposed physical procedure or a simulation as a performed experiment.

For a full or multi-session study, maintain one short `$STUDY/research/handoff.md` using `$KIT/templates/handoff.md`. Update it at pauses and delivery; link to evidence rather than duplicating it. On resume, read the existing handoff, frozen plan, run record, outputs, draft and review (where present) before deciding whether anything needs to run again. For a full study deliver the manuscript, raw outputs, commands and evidence review.

1. Use `ai4sci-idea` for a broad direction or a novelty check. Identify why the question matters, test it against the closest existing result and an objection, and bring the surviving question and its strongest rival to the design stage. A reading-list request stops before this comparison.
2. Use `ai4sci-experiment` to agree on what would answer the question, freeze the plan, run a pilot, then run the declared comparison. In a reproduction, match the source's conditions and disclose substitutions. Keep valid negative results.
3. Use `ai4sci-paper` for drafting and `ai4sci-figures` for figures. Do not fill result placeholders with predictions. Build `research/claims.json` while drafting, not after losing the source locations.
4. Use `ai4sci-review` before delivering a formal draft. Run the evidence check yourself. Report any disagreement between text and source to the author for correction, then recheck the affected claims. Tell the user where the manuscript is and which findings hold or remain unresolved. Give the rerun command on request or in the handoff, not as an outstanding task for the user.

For more than one experimental route, preserve the parent, alternatives and the observed reason to continue or stop. The [branch decision check](../../checks/branches.md) can compare recorded measurements. For a submission, a resubmission or reviewer comments on an existing manuscript, start from the actual author files and read [the submission and revision route](../ai4sci-paper/references/submission.md). For several review rounds, follow each concern into the actual version returned and re-open it when new evidence changes the answer. The [review-round check](../../checks/rounds.md) can follow the issue across versions. A single draft does not require these optional records. Neither a book list nor a request for editorial advice starts an experiment or a rewrite.

Choose tools from the current session. A scholarly search connector such as `paper-search` can search multiple indexes, follow references and resolve identifiers. Use a paper-reading tool for long original articles when available. For a supplied Word template or tracked edits, use an available DOCX skill. Use a spreadsheet skill for an actual Excel supplement and a PDF tool to inspect the final pagination, captions and figures. Keep the author's existing library, bibliography and experiment environment. Missing optional tools block only the task that needs them. Never call a Markdown preview a reviewed Word or PDF file.

## Delegate by responsibility (omo-slim)

- Check the current session's actual roles and permissions. For substantive work, send one read-only task to locate the closest studies and counterevidence, another to inspect the available data, evaluation and resources. Each brief names inputs, scope, output, budget and validation owner. Do not assign fixed agent names.
- Before parallel work in the same study, including work in separate sessions, agree on one owner for each output. Share baseline inputs read-only. Give each task distinct writable paths; use separate working directories for runs that generate the same filenames. Record active writers and their paths in the study handoff when work spans sessions. If another session owns the draft or its ownership is unclear, return edits in a separate file. One designated editor merges changes into the canonical manuscript and handoff.
- The coordinator reconciles findings and freezes the question. The analyst returns code, exit status and raw result paths. The writer cites them. A separate reviewer receives the frozen design, draft, references and run outputs, not the analyst's self-rating. With only one worker, label the result self-checked. Shared project memory is not a blinded review.
- Investigate missing evidence once and return a precisely identified gap to the same owner. After a bounded repair, recheck the affected claims. Stop when the answer is supported, the declared budget is exhausted, or the remaining dependency is unavailable. Do not keep running to turn a negative result positive.

## Files and commands

For a new formal study conducted with this workflow, read `$KIT/checks/contract.md` and `$KIT/templates/plan.json`. Keep the manuscript, plan, run record and claim ledger in `$STUDY/research/`. Run `python3 "$KIT/ai4sci.py" freeze "$STUDY"` before the formal experiment and `python3 "$KIT/ai4sci.py" audit "$STUDY"` after drafting. If an author brings a manuscript from elsewhere, start with the [revision route](../ai4sci-paper/references/submission.md). Review the actual returned file against the evidence available. Audit a new formal supplement in its own directory, not the original study. Report the checks performed and their scope.
