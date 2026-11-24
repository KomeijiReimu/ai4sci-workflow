# Research workflow maturity evaluation

This protocol was fixed before opening held-out tasks or grading the new workflow. The comparison baseline is `1c5d24060e1a1a67b551b1724427db3f77fefcb8`. The object of comparison is a researcher's ability to select, test, challenge, revise and hand off a scientific conclusion. Both systems may use their normal host tools. Desktop features, file counts, popularity and passing our own checker are not measures of scientific quality.

## Comparison groups

| Group | Systems | Role |
|---|---|---|
| A | Qiushi Engine, InnoClaw 2.0, Ligase, AutoSciRub, EvoLab | The five leading configurations with 40/40 scores in the [frozen official Pass@1 snapshot](https://github.com/InternScience/ResearchClawBench-Home/tree/6be2ab8ca379bd3ad0c1e83d86c985e11af972af/data). These five form the majority denominator. Retain model and version identities. EvoLab is not EvoScientist. |
| B | Synthetic Sciences OpenScience, AIPOCH Open-Science, AI4S Research Open Science Desktop | Mandatory comparisons on the research investigation, transferred reproducibility package, persistent study, and review. Match actual repository and system versions. |
| C | ARIS, alphaXiv OpenResearch, EvoScientist, Sakana AI Scientist-v2, Kosmos, Denario, Agent Laboratory, PaperQA2, OpenScholar, AIDE, autoresearch, Heuresis and relevant domain specialists | Compare what is distinctive for the stage they support, including capabilities we lack. Neither B nor C supplies a missing A vote. |

For each B/C entry record a task applicable to both tools, evidence on both sides, inspection performed, finding and limitation. Distinguish documented behavior from actual study outputs. An unavailable artifact is unknown, not a loss for its author.

## Decision rule

Assess six dimensions using scientific work rather than software feature counts:

1. **Question selection.** Is the question distinct from its closest verified precedent, consequential and falsifiable?
2. **Grounded reading.** Do the decisive passages support the interpretation, accounting for access limits and counterevidence?
3. **Design and adaptation.** Do the controls distinguish credible explanations? Did actual evidence motivate a branch, a stop or a revision without rewriting the original test?
4. **Execution and replication.** Can another investigator recover the decisive comparison from inputs, rather than reading off the same summary?
5. **Manuscript and revision.** Does the delivered file present the supported result, including material corrections or an informative negative result?
6. **Handoff.** Can a fresh investigator locate, reproduce and continue the correct study state without oral help from its author?

Record the evidence level (unknown, documented mechanism, observed research product or independently checked outcome) separately from the comparative judgment (below, comparable on observed work, stronger on observed work or unknown). A provider-published artifact can qualify if a non-author actually inspects or recomputes the relevant work. One artifact can cover several dimensions. Give the version, locator, demanding task, comparison rationale and checks actually run. Comparable is a bounded judgment of the observed work, not statistical equivalence.

Overall success requires comparable or stronger work on **all six dimensions for the same at least three of the five A systems**, with no material scientific deficit. Publish the full matrix including adverse and unknown cells. All 200 Group A entries have `details_exported: false` in this snapshot. Their scores alone do not demonstrate workflow mechanisms. Seek version-linked external archives. A public benchmark slice is a separate milestone with a separately frozen protocol, never a substitute selected after seeing an adverse result.

## Trials and resources

Use two sealed, independent benign computational studies in different domains: one starts with a research direction and real literature, the other with existing data or results and a material revision. An independent custodian selects tasks, permitted inputs, references and grading criteria. Before launch record opaque identifiers, dated commitments, release/kit digests, allowed literature access and the resource class. Keep cases and answers out of project memory, implementation workspaces and the operator's history. Without an isolated custodian, call the runs developmental. A public task may have been seen during model training.

Run in fresh sessions and study directories with only the frozen product and allowed inputs. Hide previous solutions, evaluation archives, repository history and other attempts. Keep a receipt for compromised or failed runs. CPU only, zero additional model spend, maximum two hours per research run and two hours of review in aggregate. One primary attempt per task, no best-of selection. Record model, compute, elapsed time, interventions and usage. Any expansion requires advance authorization. Do not run unsafe cases or silently change judges. Archive local scientific studies even when external comparative evidence is insufficient.

## Release gates

**Prospective public-transfer amendment (before case selection).** An externally authored, versioned pool can supply two post-freeze transfer cases even when private local custody cannot be established. This is evidence about public tasks with a withheld reference, not a secret evaluation or a guarantee of no training exposure. Freeze the release, stratum eligibility, known exposures, input allowlist, adjudication, budget, future public randomness round or deterministic timing rule, and reserve order before drawing IDs. Verify denied access to an excluded marker, host checkout, previous work, shared memory and the general web in a fresh operator namespace. Give the operator only lawfully obtained prompt and task inputs. Lock a dated manifest of the whole submitted study before obtaining the external answer for grading. A reserve may replace a predeclared eligibility or custody failure, never an unfavorable scientific result. If separation cannot be verified label the trial developmental. No assertion that merely using an unbilled endpoint provides privacy or authorisation.

Grade a dimension only when the case offered an opportunity. A prescribed question is not evidence of originating it. A well-supported decision to retain a finding after criticism can show review handling, not actual document correction. Additional attributable cases at the same configuration may fill opportunity gaps. Every peer counted needs at least one connected investigation from question or design through execution to a research report. No opportunity in all inspected cases remains unknown.

- The public penguin reviewer amendment is a development check. Preserve the original and identify its plan, run, evidence and review by digest. Work on its previously inspected holdout is sensitivity analysis, not fresh confirmation. Other public showcases do not count as sealed validation.
- Check the actual submitted DOCX/PDF and any supplied LaTeX source and build. Inspect decisive text, figures and revision propagation. Bind a dated review to the exact final bytes and audited ledger outside the delivered document. A hash establishes identity, not approval. Report whether the reviewer was a person, a separate agent or the author.
- Orchestrator and oracle independently record verdicts, counted peers, evidence and blockers before exchanging their reasoning. Leakage, invented evidence, failure to reproduce a decisive conclusion, undeclared reuse of confirmation data, or a final document retaining a withdrawn conclusion veto completion. A factual disagreement gets one independent recheck. A bounded product repair does not erase a failed trial. Re-evaluation of a changed release uses an unused sealed case only within authorized resources.
- Overall release requires matching verdicts on the same majority claim and settled validation. Refresh the Chinese and English homepages locally. Check the entire outgoing commit range excludes both README changes before pushing other accepted changes to `master`.
