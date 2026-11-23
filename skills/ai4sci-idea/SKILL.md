---
name: ai4sci-idea
description: Develop or screen a testable research idea against prior work, accessible data and compute. Use for 找方向、查新、选题、反例、文献综述 or deciding whether a proposed experiment is worth running.
---

# Select a question

Start from a topic even in an empty study directory. Use literature search or scholarly indexes available in this session. Open the original paper or publisher record to check its identity. Base descriptions of its findings on the passages you actually read. For a reading list, give the title, a DOI or stable link, what the paper contributes and why it is relevant. If access stops at the abstract, say so for that paper. Stop at the list when that answers the request.

For idea discovery, use the papers to distinguish a proposed question from what has already been tested. Give the user a small set of distinct candidates, or just one if requested. Pair each with the closest evidence, a usable dataset or other test and an observation that would count against the idea. Label a proposed experiment as a proposal. Retrieving papers does not establish novelty or complete the experiment.

For an existing idea start with its strongest known competitor and the cheapest test that could kill it. For an open direction, have one reader search the nearest work and another examine the available observations, splits, labels, simulator or analytic solution. State what was searched and where coverage ends. With supplied materials only, call this a local literature screen, not a global novelty search.

Record for each serious candidate: the closest specific source (identifier, version, page/section or table), what it already shows, what question remains, the competing explanation, the feasible test, and the result that would make the idea uninteresting. Trace disputed claims back to the full passage. A paper title, citation count or search result is a lead, not evidence. Distinguish claimed novelty, reproduction and didactic verification. Pick the best answerable question, with a reason for rejecting alternatives.

For a literature review retain the query and inclusion criteria. Deduplicate by stable identifiers and preserve disagreements in data, population, methods or scope. Save permitted excerpts or locators, not entire copyrighted papers for public redistribution. For an inaccessible source label the claim unverified. Hand off the question, scope, located evidence, required inputs and budget. For an audited literature-only report, freeze the review question and criteria, write `research/run.json` with `status: "not-applicable"` and a `reason`, and use quote evidence (`displays` for quoted numerical results).

For a formal source-based review, set `require_source_manifest: true` in the plan and keep `research/sources.json` as specified in `checks/contract.md`. Give each retained excerpt a stable source identity, access level and precise page, section or table. Prefer the version of record and check publisher corrections or retractions for decisive sources. For a systematic search, retain the databases, search date and exact queries, screening counts and reasons for excluding near matches. A reading list does not need a study manifest. Do not call a targeted search systematic.
