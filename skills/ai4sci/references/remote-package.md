# Hand over an experiment before the remote run

Use this route when the requested deliverable is the runnable experiment itself: a training or analysis pipeline, its inputs or acquisition instructions, and the command for another machine. It applies with or without a named venue. A request for ideas or a design alone does not require a package. If the user asks for preparation only, do not launch a pilot, a toy study or the actual job on either machine. Static reading, digest checks and inspection of archive members do not require a run.

## Involve reviewers before decisions are made

1. **Choose the reviewers at the start.** Inspect the host's available agents, permissions and configured model profiles. Select Oracle or specialists with strong reasoning appropriate to the method and remote execution; reserve three independent sessions across the study. Record the qualified `provider/model#variant` profiles before dispatch (omit `#variant` if unset). A role alias, call count or several cheap model calls is not evidence of a strong reviewer. The same qualified model may run in separate fresh sessions. The lead dispatches these assignments without waiting for the author to name the agents.
2. **Methods reviewer — question through implementation.** Bring the strongest prior and alternative to the reviewer at question selection. Before freezing the plan, have it challenge the baseline, split, estimand, decision rule and compute budget. Give the reviewer the actual proposed plan bytes and ask for the decisive objection, its disposition and any blocker. Return to that same session when a change to data access, evaluation, baseline or implementation changes the scientific comparison. Preserve frozen history; review an amended design before building against it. Continuing this session provides continuity, not another independent opinion. For a supplied frozen design, assess it as received and date the review accordingly; never backdate a design approval.
3. **Build and identify the exact delivery.** Package the instructions, entry point, frozen plan and its digest, environment and input versions or acquisition steps, outputs and failure/resume behavior. Record the command a receiver will run. Compute SHA-256 of the plan and of the final distributable file. For a directory delivery, seal one archive from the intended file set and deliver those reviewed bytes. Keep host review records **outside** the archive. Source-tree approval does not cover omissions during packaging.
4. **Two fresh final reviewers, in parallel.** Start two new qualified child sessions. Neither may have proposed the design, implemented the pipeline, built the package or worked on the other's review. Give both the original brief, the same archive and the declared design; do not send a preferred verdict. Both must open the archive, verify its plan and archive digests, cite concrete member paths and state findings and blockers.
   - **Science:** trace the packaged claim through selected inputs, split, actual baseline and budget, evaluation code, metric and decision rule. Check whether an implementation that runs could still answer the wrong question. Identify the observations that require execution.
   - **Launch:** trace the documented invocation from clean extraction through its working directory, prerequisites, resource limits, output paths and failure or resume behavior. Distinguish a missing bundled file from a receiver prerequisite. Static inspection is not a connectivity, GPU or training test.
5. **Settle both judgments before handoff.** Return defects to the builder. If a repair changes the method, involve the methods reviewer again. When any archive byte changes, send the replacement to **both** final reviewers; they may limit their reread to the change and its impact, but both must acknowledge the replacement digest. Both final judgments must also cover the latest methods decision, even when no files changed. If someone is unavailable, dispatch a qualified independent substitute with the actual package. If review is missing or unverifiable, hand off only as **review pending**; if a material blocker remains, **blocked**. Do not downgrade to a weaker model to mark the package reviewed. A cleared handoff states **statically reviewed; experiment not run** when preparation was the requested limit. This is a separate decision from review of a future results manuscript.

## Verify the three returns on the issuing OpenCode host

Ask each reviewer to end a substantive, blocker-free response with the applicable standalone line below, substituting the actual lowercase SHA-256 values. A reviewer who finds an unresolved blocker reports it without the line. On a later methods recheck, reaffirm the current plan in the latest return. Record the real child references and findings in the existing handoff; do not copy a marker into a chat on a reviewer's behalf.

```text
AI4SCI-REMOTE design PLAN_SHA256
AI4SCI-REMOTE science PLAN_SHA256 PACKAGE_SHA256
AI4SCI-REMOTE launch PLAN_SHA256 PACKAGE_SHA256
```

Run the [return check](../../../checks/remote_review.py) on the issuing host, using the actual plan and file to be transferred. `QUALIFIED_PROFILE` is a preselected model profile, not a role name. Repeat `--qualified` for each eligible profile. Pass `--contributor CHILD_ID` for **each** other session that helped design or implement the package. The lead and methods reviewer are already excluded. For a resumed study whose methods review belonged to an earlier lead, also pass `--design-parent ORIGINAL_LEAD`.

```sh
python3 "$KIT/checks/remote_review.py" "$PLAN" "$PACKAGE" \
  --parent "$LEAD" --design "$METHODS_CHILD" --science "$SCIENCE_CHILD" \
  --launch "$LAUNCH_CHILD" --qualified "$QUALIFIED_PROFILE"
```

The check reads OpenCode's actual session records and compares the returned decisions with the current files. Use it **and** read the reviews: a matching return does not establish model competence, independence from undeclared contributors or scientific validity. The lead checks these from the original assignments, evidence and dispositions. A missing host record or unsuccessful check leaves verification pending. The receiver can compare the delivered file's digest without installing OpenCode.
