---
name: ai4sci-idea
description: Develop or screen a testable research idea against prior work, accessible data and compute. Use for 找方向、查新、选题、反例、文献综述 or deciding whether a proposed experiment is worth running.
---

# Select a question

For an existing idea start with its strongest known competitor and the cheapest test that could kill it. For an open direction, have one reader search the nearest work and another examine the available observations, splits, labels, simulator or analytic solution. State what was searched and where coverage ends. With supplied materials only, call this a local literature screen, not a global novelty search.

Record for each serious candidate: the closest specific source (identifier, version, page/section or table), what it already shows, what question remains, the competing explanation, the feasible test, and the result that would make the idea uninteresting. Trace disputed claims back to the full passage. A paper title, citation count or search result is a lead, not evidence. Distinguish claimed novelty, reproduction and didactic verification. Pick the best answerable question, with a reason for rejecting alternatives.

For a literature review retain the query and inclusion criteria; deduplicate by stable identifiers and preserve disagreements in data, population, methods or scope. Save permitted excerpts or locators, not entire copyrighted papers for public redistribution. For an inaccessible source label the claim unverified. Hand off the question, scope, located evidence, required inputs and budget. For an audited literature-only report, freeze the review question and criteria; write `research/run.json` with `status: "not-applicable"` and a `reason`, and use quote evidence (`displays` for quoted numerical results). There is no numerical experiment to invent.
