---
name: ai4sci
description: Route a computational research project from a question or idea through a reproducible experiment to an evidence-checked manuscript. Use for 选题、计算实验、复现论文、查证据、写研究报告 or resuming an existing study. Enter or stop at the requested stage.
---

# Run a study

The user's request can be just a checkout path and a research goal. Resolve `KIT` from this file's location in the checkout. Read the relevant `$KIT/skills/<name>/SKILL.md` yourself. From an external project, use the user's current directory as `STUDY`. From the checkout, use the named `studies/<topic>/` if supplied. For a new topic that needs files, choose a fresh, descriptive folder there. Give both paths to collaborators. Run experiments from `STUDY` and keep research outputs there. Do not install tools, copy skills or edit project configuration to start a study.

Start at the stage the goal needs. A request to find papers can end with an annotated reading list. A request for ideas can end with candidate questions, their closest prior work and a feasible first test. Use the available search tools when the user has supplied only a topic. Neither of these requests needs a manuscript or an experiment run record. For a full study deliver the manuscript, raw outputs, commands and evidence review. When resuming, read the study's existing files before deciding whether to rerun anything.

1. Use `ai4sci-idea` for a broad direction or a novelty check. Bring the chosen question and the closest existing result to the design stage.
2. Use `ai4sci-experiment` to agree on what would answer the question, freeze the plan, run a pilot, then run the declared comparison. In a reproduction, match the source's conditions and disclose substitutions. Keep valid negative results.
3. Use `ai4sci-paper` for drafting and `ai4sci-figures` for figures. Do not fill result placeholders with predictions. Build `research/claims.json` while drafting, not after losing the source locations.
4. Use `ai4sci-review` before delivering a formal draft. Run the evidence check yourself. Report any disagreement between text and source to the author for correction, then recheck the affected claims. Tell the user where the manuscript is and which findings hold or remain unresolved. Give the rerun command on request or in the handoff, not as an outstanding task for the user.

## Delegate by responsibility (omo-slim)

- Check the current session's actual roles and permissions. For substantive work, send one read-only task to locate the closest studies and counterevidence, another to inspect the available data, evaluation and resources. Each brief names inputs, scope, output, budget and validation owner. Do not assign fixed agent names.
- The coordinator reconciles these findings, freezes the question and gives a single owner each writable area. Independent experiments may run in separate directories from a shared baseline. The analyst returns code, exit status and raw result paths. The writer cites them. A separate reviewer receives the frozen design, draft, references and run outputs, not the analyst's self-rating. With only one worker, label the result self-checked. Shared project memory is not a blinded review.
- Investigate missing evidence once and return a precisely identified gap to the same owner. After a bounded repair, recheck the affected claims. Stop when the answer is supported, the declared budget is exhausted, or the remaining dependency is unavailable. Do not keep running to turn a negative result positive.

## Files and commands

Read `$KIT/checks/contract.md` and consult `$KIT/templates/plan.json` for a formal study. The manuscript path is `$STUDY/research/paper.md`. Its plan, run record and claim ledger belong in that same `research` subdirectory. Create it when needed. With `KIT` and `STUDY` set to their actual paths, run `python3 "$KIT/ai4sci.py" freeze "$STUDY"` before the formal experiment and `python3 "$KIT/ai4sci.py" audit "$STUDY"` after drafting. Report the result of the check that actually ran.
