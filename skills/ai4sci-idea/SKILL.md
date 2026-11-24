---
name: ai4sci-idea
description: Find relevant papers, compare candidate questions against near-duplicate studies and usable data, and propose a low-cost test of competing explanations. Use for 文献调研、找方向、查新、选题 or deciding whether an idea is worth testing.
---

# Select a question

**Papers only:** start with the topic; no study setup is needed. Use scholarly search available in this session, check the identity at the publisher or original paper, and read the relevant passage. Give the title, stable link or DOI, finding, and why it matters to this question. Distinguish abstract-only access from full text; leave an inaccessible finding unverified. Stop at the annotated list.

**Ideas only:** deliver the recommendation and a *proposed* first test, then stop. Do not launch pilots, freeze a plan or draft a paper unless the user asks to proceed. Work on benign scientific questions; exclude directions that would enable exploitation, biological misuse or physical harm.

## Make the candidates compete

1. **Get two kinds of evidence before ranking.** Ask one reader to find the closest result and contrary evidence, and another to inspect what can actually be measured. Give each the topic and constraints, not a favored answer; ask for source or data locators. Use separate readers only if the host provides them. Working alone, do both passes and call them self-checked. Two readers citing the same experiment do not supply independent empirical support.
2. **Search for the claim, not just its name.** Try a synonym for the mechanism and a search on the population, outcome or baseline. Follow the references of the closest paper. For each serious candidate cite the nearest original result (version and section, table or page); state what overlaps and what remains unanswered. Merge candidates that would run the same comparison and support the same inference. If a paper already answers the question, cite the passage and drop the novelty claim, or explain the value of a reproduction. Report the scope of the search; supplied material alone supports only a local screen.
3. **Check whether the inputs can decide it.** Inspect a versioned dataset description, schema or permitted development sample. Identify the unit, target, available-at-prediction-time variables and group/time keys needed for the split; check access, permitted use and cost. For analytic or simulation work, identify the actual reference or controllable input instead. Say what you inspected. If a missing label, comparison group or dependency prevents the test, mark the candidate conditional rather than calling the dataset ready. Leave held-out outcomes unopened.
4. **Choose between genuinely different explanations.** For an open topic, compare a small set of candidates; for a supplied idea, challenge it with its strongest plausible rival. For each finalist, give a prediction from each explanation under the *same* proposed contrast, the baseline, and an observation that would weaken the favored account. If both predict the same result at attainable precision, change the contrast or defer the question. A new model name or another parameter setting is not by itself a different explanation.
5. **Recommend one next decision.** Choose the least costly comparison whose outcomes would change what to do. State the evidence and input on which the choice depends, the likely resource cost, and why the nearest alternative loses (already answered, inaccessible, or less diagnostic). If none qualifies, say which evidence would unblock a choice. A plausible test, a literature gap and a measured effect are three different claims.

## When the requested product is a review

Retain the search scope and inclusion criteria. For a systematic review, record databases, dates, exact searches, screening counts and reasons for excluding near matches. Deduplicate versions; preserve genuine disagreements about methods, populations or outcomes. Check corrections and retractions for decisive sources. Save permitted excerpts with locators, not entire copyrighted works for redistribution.

For a **formal audited** source-based review, follow the checkout's [file contract](../../checks/contract.md): freeze the review question and criteria with `require_source_manifest: true`; register the retained snapshots in `research/sources.json`. Record `status: "not-applicable"` and the reason in `research/run.json`. Use literal quote evidence, with `displays` for source-reported numbers. These records are unnecessary for a reading list or idea shortlist.

The screening decisions adapt [ARIS candidate selection](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/idea-creator/SKILL.md) and its [claim-level novelty screen](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep/blob/4ba94ae2a1c1fbbb14858750dd8764cabf6c28bd/skills/novelty-check/SKILL.md); the feasibility pass draws on [EvoScientist's data and protocol research brief](https://github.com/EvoScientist/EvoScientist/blob/850df6f075505d74b69e34933b4d0c989422b094/EvoScientist/subagents/research.yaml). These are design sources, not evidence for the user's topic.
