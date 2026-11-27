# Research workflow

When a user gives you this repository's path and a research goal, read `skills/ai4sci/SKILL.md` and choose the stages that fit the request. A broad topic is enough to start a literature search, compare prior work, and propose a testable question. If the user asks only for papers or ideas, stop there.

From an external project, use its current directory. In this checkout, give each new study that needs files its own unused directory under `studies/`. Keep later tasks for the same study in its existing directory. If a request to continue could refer to several studies, list the matching directories and ask which one before writing or running anything.

Run experiments and save outputs in the selected study directory. Treat other studies as read-only. Parallel tasks can share inputs but must write to separate files; one owner merges changes to the manuscript and handoff. Before delivering a manuscript, check it against the evidence yourself. Give the user the path to the manuscript and report any claims that still lack support.
