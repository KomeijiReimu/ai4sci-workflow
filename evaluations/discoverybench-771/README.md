# DiscoveryBench: one held-out synthetic astronomy query

**The submission missed the published hypothesis, but an independent analysis confirmed its numerical findings.** DiscoveryBench query `771` asks how galaxy density increase relates to thirteen characteristics. The answer key says the increase depends on those characteristics in galaxies classified as having high dark-matter density. The [submitted answer](submission/paper.md) reports that every recorded increase was `1.0` and draws no such inference. The verdict is a local assessment, not an official DiscoveryBench score.

## Task and protocol

| Item | Record |
|---|---|
| Organizer and version | Allen Institute for AI, [DiscoveryBench commit `c31fcf0`](https://github.com/allenai/discoverybench/commit/c31fcf011e070f021a5f5b906896d0821f6880e8) |
| Exact task | `discoverybench/synth/test/astronomy_0_0`, metadata ID `0`, query ID `771` · [question and dictionary](https://github.com/allenai/discoverybench/blob/c31fcf011e070f021a5f5b906896d0821f6880e8/discoverybench/synth/test/astronomy_0_0/metadata_0.json) · [organizer's data](https://raw.githubusercontent.com/allenai/discoverybench/c31fcf011e070f021a5f5b906896d0821f6880e8/discoverybench/synth/test/astronomy_0_0/data.csv) |
| Selection | To select a simulated physical-science task, the coordinator sorted the six `astronomy_<integer>_<integer>` directories in the synthetic `test` split lexicographically and took the first. Within it, the lowest numeric metadata suffix and then the lowest query ID determined the task. The protocol required a data file under 1 MiB and a published key, with no substitution based on the result. |
| Solver interface | A fresh agent session used the original CSV, question and column descriptions with the local ai4sci workflow. Its instructions excluded external lookup, other studies, prior sessions, keys and graders. The session shared a host with the evaluator and had no separate OS sandbox. The check did not use the official DiscoveryBench agent or test whether the task appeared in training data. |
| Timing | The coordinator froze the [assessment rules](assessment-plan.json) before viewing measurements or answer text. The solver noticed the constant outcome in its initial data check and recorded it in its [analysis plan](submission/analysis-plan.json) before freezing the plan and running the thirteen comparisons. The evaluator hashed the sole submission and its results before opening the [matching answer-key row](https://github.com/allenai/discoverybench/blob/c31fcf011e070f021a5f5b906896d0821f6880e8/eval/answer_key_synth.csv?plain=1#L43). The submission was not revised. |

## Key alignment: miss

Under the frozen rubric, **full** agreement required the conditional relationship specified in the key. **Partial** agreement required at least one substantive link. Repeating predictor names from the question did not count. An answer that recovered no substantive link was a **miss**. The key specifies no sign, coefficient, functional form or effect size.

| Gold element | What the submission says | Local decision |
|---|---|---|
| Galaxies classified as having higher dark-matter density | Used all rows with an observed predictor and outcome for each comparison, without identifying the high-density class. | Condition missing |
| In that class, the increase depends on distance to the nearest star-forming region, star formation rate, magnetic field presence, galaxy age, dominant stellar age, luminosity variability, binary star system presence, stellar velocity dispersion, stellar surface temperature, UV emission, cosmic radiation, red-star proportion and blue signature intensity. | Compared groups for each predictor and found identical means and undefined correlations. It did not assert dependence on any predictor in the high-density class. | No substantive link recovered for any of the thirteen predictors |

## Independent numerical check

The reviewer used SQLite to analyze the same upstream CSV independently. Of the **500** rows, **494** recorded an outcome. Every recorded value was **1.0**, giving a sample standard deviation of **0.0**. The other six rows had blank outcomes. Grouping the rows by the dark-matter classification named in the key gives:

| Dark-matter classification | Rows | Recorded | Blank | Range of recorded outcomes |
|---|---:|---:|---:|---|
| High | 252 | 250 | 2 | 1.0–1.0 |
| Low | 248 | 244 | 4 | 1.0–1.0 |

For all **13** comparisons, the reviewer reproduced the submitted pair counts, group sizes, means and mean differences. For example, the mean was **1.0** both for the **219** rows with a recorded outcome and no magnetic field and for the **230** with a recorded outcome and a magnetic field. All **13** Pearson correlations were undefined because the outcome's standard deviation was zero. The [submitted contrasts](submission/contrasts.csv) and [summary](submission/summary.csv) give the original results.

A separate rerun of the workflow's structural audit verified the evidence for three claims and thirteen required comparisons, with zero errors. That audit checks the submission against its evidence. Agreement with the benchmark key was assessed separately.

All 250 recorded responses in the **high-density class** were 1.0. Even in the class named by the key, the table therefore supplies no outcome variation from which to infer the stated dependence. This finding concerns the recorded values, not the six missing outcomes or the underlying generating mechanism. The local verdict remains a miss on this one task.

## Reproduce

From this directory, run `python3 verify.py` with Python 3.10 or later and internet access to the pinned organizer files. The [checker](verify.py) uses only the standard library. It verifies the hashes of the CSV, metadata, key, paper and contrasts, then retrieves the unique matching key record. It independently rebuilds all thirteen comparisons and prints the outcome counts for both dark-matter classes. This reproduces the numerical check without running the solver or calling a model. The comparison with the published hypothesis is the manual assessment above.

| Artifact | SHA-256 |
|---|---|
| Frozen assessment rules | `ec4bb86a4c4859491bd442a2c7459f24e2e968f5af65a79828ebeb8841d16ce0` |
| Upstream CSV | `8e9f72b6820e7f4f234576112ffc53c956794abb6b5fef4aaedd79062ffabd9b` |
| Submitted paper | `b9bf936f0b35acc8084c7bf53560b1a3e792b933c9c98520fe3602f9e290ccdf` |

Contains information from [DiscoveryBench](https://github.com/allenai/discoverybench), by Majumder et al., available under the [Open Data Commons Attribution License](https://github.com/allenai/discoverybench/blob/c31fcf011e070f021a5f5b906896d0821f6880e8/discoverybench/license.md). The upstream table and answer key are linked rather than redistributed here.
