---
name: ai4sci
description: Help with a research question, literature search, study design, analysis, reproduction or evidence-checked manuscript. Use for 文献调研、选题、研究设计、计算实验、复现、查证据、写研究报告 or resuming an existing study. Enter or stop at the requested stage.
---

# Run a study

The user's request can be just a checkout path and a research goal. Resolve `KIT` from this file's location in the checkout. Read the relevant `$KIT/skills/<name>/SKILL.md` yourself. From an external project, use the user's current directory as `STUDY`. From the checkout, use the named `studies/<topic>/` if supplied. For a new topic that needs files, choose a fresh, descriptive folder there. Give both paths to collaborators. Run experiments from `STUDY` and keep research outputs there. Do not install tools, copy skills or edit project configuration to start a study.

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
- The coordinator reconciles these findings, freezes the question and gives a single owner each writable area. Independent experiments may run in separate directories from a shared baseline. The analyst returns code, exit status and raw result paths. The writer cites them. A separate reviewer receives the frozen design, draft, references and run outputs, not the analyst's self-rating. With only one worker, label the result self-checked. Shared project memory is not a blinded review.
- Investigate missing evidence once and return a precisely identified gap to the same owner. After a bounded repair, recheck the affected claims. Stop when the answer is supported, the declared budget is exhausted, or the remaining dependency is unavailable. Do not keep running to turn a negative result positive.

## Files and commands

Read `$KIT/checks/contract.md` and consult `$KIT/templates/plan.json` for a formal study. The manuscript path is `$STUDY/research/paper.md`. Its plan, run record and claim ledger belong in that same `research` subdirectory. Create it when needed. With `KIT` and `STUDY` set to their actual paths, run `python3 "$KIT/ai4sci.py" freeze "$STUDY"` before the formal experiment and `python3 "$KIT/ai4sci.py" audit "$STUDY"` after drafting. Report the result of the check that actually ran.
