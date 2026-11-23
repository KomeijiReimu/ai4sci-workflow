---
name: ai4sci
description: Route a computational research project from a question or idea through a reproducible experiment to an evidence-checked manuscript. Use for 选题、计算实验、复现论文、查证据、写研究报告 or resuming an existing study. Enter or stop at the requested stage.
---

# Run a study

Identify two paths. `KIT` is the workflow checkout containing this file at `skills/ai4sci/SKILL.md`. `STUDY` is the named `studies/<topic>/` in that checkout, or the user's current external project. When an external session receives a path to this file, read any needed stage instructions directly from `$KIT/skills/<name>/SKILL.md`. Do not install the kit, copy skills or alter project configuration. Give both resolved paths to collaborators, run experiments from `STUDY`, and keep all research outputs there.

Determine the requested deliverable, existing inputs and compute budget. Reply and write in the requested language. For a literature-only task stop at a sourced synthesis; for an idea screen stop after the cheapest decisive test. For a full study deliver the manuscript, raw outputs, commands and evidence review. When resuming, read the study's `research/` files first; do not rerun completed jobs on the strength of a chat summary.

1. Use `ai4sci-idea` for a broad direction or a novelty check. Bring the chosen question and the closest existing result to the design stage.
2. Use `ai4sci-experiment` to agree on what would answer the question, freeze the plan, run a pilot, then run the declared comparison. In a reproduction, match the source's conditions and disclose substitutions. Keep valid negative results.
3. Use `ai4sci-paper` for drafting and `ai4sci-figures` for figures. Do not fill result placeholders with predictions. Build `research/claims.json` while drafting, not after losing the source locations.
4. Use `ai4sci-review` on a settled draft. Return the report path, run status, supported and unresolved claims and the exact command to check the deliverable. Incomplete or blocked work is a handoff, not a finished experiment.

## Delegate by responsibility (omo-slim)

- Check the current session's actual roles and permissions. For substantive work, send one read-only task to locate the closest studies and counterevidence, another to inspect the available data, evaluation and resources. Each brief names inputs, scope, output, budget and validation owner. Do not assign fixed agent names.
- The coordinator reconciles these findings, freezes the question and gives a single owner each writable area. Independent experiments may run in separate directories from a shared baseline. The analyst returns code, exit status and raw result paths. The writer cites them; a separate reviewer receives the frozen design, draft, references and run outputs, not the analyst's self-rating. With only one worker, label the result self-checked. Shared project memory is not a blinded review.
- Investigate missing evidence once; return a precisely identified gap to the same owner. After a bounded repair, recheck the affected claims. Stop when the answer is supported, the declared budget is exhausted, or the remaining dependency is unavailable. Do not keep running to turn a negative result positive.

## Files and commands

Read `$KIT/checks/contract.md` and consult `$KIT/templates/plan.json` when preparing a formal study. Write the study's own `research/plan.json`, `run.json`, raw files, `claims.json` and `paper.md` under `STUDY`. With `KIT` and `STUDY` set to their actual paths, run `python3 "$KIT/ai4sci.py" freeze "$STUDY"` before the formal experiment and `python3 "$KIT/ai4sci.py" audit "$STUDY"` after drafting. Report the result of the check that actually ran.
