# Offline research audit

The audit checks a study's frozen plan, run record and marked manuscript statements against local evidence. From the workflow checkout, run `python3 ai4sci.py audit PROJECT` with Python 3.10 or later. `PROJECT` can be a study such as `studies/my-study` or an absolute path. From the study directory, use `python3 /path/to/ai4sci-workflow/ai4sci.py audit .` with your checkout's actual path. Paths in the manifests are relative to the study root.

## Minimal study

`research/plan.json`:

```json
{"question":"What is the estimate at the agreed sample size?","criteria":[{"id":"estimate","description":"Report the estimate and identify the method."}]}
```

Before the formal run, freeze the plan with `python3 ai4sci.py freeze PROJECT`. This writes `research/plan.sha256`.

`research/results.csv`:

```csv
n,estimate
8,0.12497
```

`research/source.md` contains the line `The estimate is the sample mean.` followed by a single LF.

`research/run.json` records the command that produced the CSV:

```json
{"status":"completed","command":"python3 measure.py","outputs":["research/results.csv"]}
```

`research/claims.json`:

```json
{"claims":[
  {"id":"C1","criterion":"estimate","statement":"At n=8 the estimate is 0.125.","status":"supported","evidence":[{"kind":"number","path":"research/results.csv","key":{"n":"8"},"column":"estimate","value":0.125,"display":"0.125","atol":0.00005}]},
  {"id":"C2","criterion":"estimate","statement":"The estimate is the sample mean.","status":"supported","evidence":[{"kind":"quote","path":"research/source.md","quote":"The estimate is the sample mean."}]}
]}
```

`research/paper.md`:

```markdown
# Estimate

At n=8 the estimate is 0.125. [C1]

The estimate is the sample mean. [C2]
```

## Plan and run record

`freeze` and `audit` use the same plan parser. The plan needs a nonblank `question` and a nonempty `criteria` array. Each criterion needs a unique nonblank string `id` and a nonblank `description`. JSON manifests must be UTF-8 objects with unique keys at every level and finite numbers. A malformed plan is rejected before `freeze` writes a digest.

`research/plan.sha256` contains the SHA-256 digest of the **raw plan bytes**, as 64 lowercase hexadecimal characters followed by a single LF. Freezing an unchanged plan again preserves the digest. `freeze` refuses to replace a different digest. The digest detects changes, including whitespace. To establish *when* the plan was frozen, keep a separately dated record.

| `research/run.json` status | What to record |
|---|---|
| `completed` | A nonblank `command` and a nonempty `outputs` array of distinct project files. List every CSV used for numeric evidence or required observations. A negative experimental result still belongs here. |
| `failed` or `blocked` | A nonblank `reason`. Record any conclusions that remain untested. A consistent record of either status yields `incomplete`. |
| `not-applicable` | A nonblank `reason`, for example a literature-only study. Cite source-reported numbers as quotations. This status cannot satisfy a plan with required observations or matched experimental conditions. |

Two optional fields bind the run to specific files. `plan_sha256` holds the frozen plan digest as a lowercase hexadecimal string **without** the LF. If supplied, it must match. `sha256` maps **every** listed output path, and no others, to its lowercase SHA-256 digest over raw bytes. Without the output map, the audit checks the declared files but does not verify their digests.

### Observations and matched conditions

To check that a measurement exists even when the paper does not print it, put `required_observations` on the relevant criterion **before freezing**. To test a numeric prediction as well, add `bounds` to that observation. For example, a new study could specify this interval for the estimate at `n=8`:

```json
{"id":"estimate","description":"Report the estimate, test the planned interval and identify the method.","required_observations":[{"path":"research/results.csv","key":{"n":"8"},"column":"estimate","bounds":{"min":0.125,"max":0.126}}]}
```

If present, `required_observations` must be a nonempty array. Each entry needs `path`, `key` and `column`. The key maps one or more nonblank column names to nonblank CSV strings. The result column must be distinct from the key columns. On a completed run, the path must be listed in `outputs`, the key must select exactly one row, and the result cell must contain a finite decimal. Two entries in the same criterion cannot select the same cell, even through different keys. Failed and blocked runs leave the observations unverified.

`bounds` uses finite JSON numbers for its limits. The comparison uses the **exact decimal value in the raw CSV cell**, with equality at either endpoint counted as `met`. In the example, a raw estimate of `0.12497` is below `0.125`, so the outcome is `missed` even though the manuscript correctly rounds the estimate to `0.125`. The miss is a valid negative result. A supported report of that result can be `ready`. A missing measurement in a run declared `completed` is an input error, not a negative result.

Without `bounds`, the cell check establishes only that the planned observation exists. Without `required_observations`, the audit checks that a claim references the criterion. The reviewer interprets the scientific implications. The audit does not infer thresholds from criterion descriptions or grade conclusions from prose. Document thresholds chosen after inspecting the data as exploratory, separately from the frozen prediction.

To compare experiments under declared common settings, add `"matched_conditions":["threads","dataset"]` to the plan. The array must contain distinct, nonblank names and cannot be empty. A completed run must then record at least two `arms` with distinct IDs, for example:

```json
{"arms":[{"id":"old","conditions":{"threads":1,"dataset":"A"}},{"id":"new","conditions":{"threads":1,"dataset":"A"}}]}
```

For each named condition, every arm must declare the same nonblank string, number or Boolean, without coercion between types. Extra conditions are ignored. Check the execution logs to confirm that the experiment actually used the declared settings.

## Claim ledger and manuscript

Every criterion needs at least one claim, even if it is untested. Each claim has a unique `id` matching `C[1-9][0-9]*`, a `criterion` referencing a plan ID, a unique nonblank single-line `statement`, a `status` and an `evidence` array. Put the exact statement, one space and `[ID]` alone on a manuscript line. Outer line whitespace is ignored. Bracketed markers such as `[C1]` are reserved for registered claims. Each must occur exactly once and cannot be embedded in a statement. Unmarked prose needs separate review.

`supported`, `partial` and `contradicted` require at least one verified `number` or `quote`. The reviewer judges whether the cited evidence supports or contradicts the wording. `unsupported` and `untested` may have empty evidence arrays. To record a gap, use `{"kind":"incomplete","reason":"Replicate pending"}` or `{"kind":"blocked","reason":"Source unavailable"}`. A gap is not supporting evidence and cannot appear in a `supported` claim. Citing a missing file instead of declaring the gap is an input error.

### Numbers from an experiment

For each `number`, specify the CSV `path`, `key` and `column` as for a required observation. Key values are compared to CSV fields as literal strings. `value` and `atol` are mandatory JSON numbers. `display` is the exact numeric spelling used in the manuscript and must denote `value`. If omitted, the audit uses the string form of the parsed JSON number. Set `display` explicitly for trailing zeros, scientific notation or a leading plus sign.

The allowed transcription difference is **the smaller of `atol` and half a unit in the last displayed decimal place**, including any exponent. Both limits are inclusive. For `display: "0.250"` and `atol: 1`, a CSV value of `0.2505` passes but `0.25051` fails. With `atol: 0`, only exact agreement passes. For `+2.50e-3`, half a unit is `0.000005`. Use a nonnegative `atol` and the same units as the CSV. There is no implicit percentage conversion. Neither the display precision nor `atol` widens a frozen observation's `bounds`.

A `number` evidence record may explicitly declare `numeric_outcome` as `met` or `missed`. It must refer to a bounded cell under **that claim's criterion**, and the declared outcome must match the raw-cell comparison. For the interval and estimate above, a claim reporting the missed prediction could use:

```json
{"kind":"number","path":"research/results.csv","key":{"n":"8"},"column":"estimate","value":0.125,"display":"0.125","atol":0.00005,"numeric_outcome":"missed"}
```

The checker uses exact rational arithmetic. Numeric CSV values use ASCII signed decimals with an optional base-10 exponent. Whitespace, digit grouping, NaN and infinity are invalid. The compared spellings are limited to 100 characters and to an absolute decimal exponent of 1000 after accounting for fractional digits.

### Numbers and quotations in the text

- In `supported` and `partial` claims, **each occurrence** of a reported number needs evidence, even when two measurements have the same value. Two separate results printed as `8` need two distinct CSV cells or quoted number occurrences. Naming the same cell through a different key does not provide another measurement.
- An explicit key context such as `n=8` is exempt when it matches a verified number record's key in that claim. The `8` in `n=8` cannot also serve as the reported estimate. Write numbers as separate tokens, with a space before ASCII units. A number may adjoin Chinese prose, as in `误差为0.74。`.
- For numeric binding, the audit treats ASCII `-` and mathematical `−` as the same sign, including in an exponent. The exact manuscript line and the literal source quotation must still match their respective files.
- A `quote` needs a `path` and a nonblank, case-sensitive literal `quote` from the UTF-8 text file, with universal-newline translation. For a source-reported number, add `"displays":["85.2"]`. Each listed spelling must be distinct after minus-sign normalization and occur as a complete numeric token in both the claim and the quoted part of the original file. One quotation containing the same number twice can support two occurrences. Overlapping quotations of the same source token count only once per claim.

Evidence locators must be unique within a claim. Different claims may cite the same evidence. The reviewer checks the statistic, units, population and meaning of each passage, including whether it warrants the manuscript's conclusion.

## Source registry

To require a formal source registry, put `"require_source_manifest":true` in the plan before freezing. The flag must be Boolean. If `research/sources.json` exists, the audit checks it whether or not the plan requires it. If the file is optional and absent, literal quote and numeric display checks still apply.

The registry contains a nonempty `sources` array. Each record needs seven nonblank string fields:

| Field | Value |
|---|---|
| `id`, `title` | A unique source ID and the source title. |
| `origin`, `locator` | The source's HTTP(S) URL for published material, or a description of the origin for supplied material. The locator identifies the passage, such as a section, table or paragraph. |
| `access` | `full-text`, `abstract` or `provided`. Both `full-text` and `abstract` require an HTTP(S) origin with a hostname. |
| `path`, `sha256` | A distinct local snapshot and its lowercase SHA-256 digest over raw bytes. |

For the one-line source in the minimal study, the optional `research/sources.json` is:

```json
{"sources":[{"id":"method-note","title":"Estimator definition","origin":"Supplied study note","locator":"Only paragraph","access":"provided","path":"research/source.md","sha256":"85067ddd976471a2b783a44466e71ddd8fb5f497a505d5f02017d3777d499b0a"}]}
```

With a registry, every quote's `path` must resolve to a registered snapshot. The audit verifies every registered digest, even when the quoted sentence itself has not changed. It does not fetch the URL, resolve a DOI, verify the stated access level or decide whether the passage entails the claim. For a published-source example, see the [climate study](../examples/climate-sources/) and its [source registry](../examples/climate-sources/research/sources.json).

## File formats and paths

Use UTF-8 for manifests, manuscript, CSVs and source text. CSVs need nonblank unique headers, at least one data row and consistent field counts. Paths use `/`-separated components relative to the study, without a drive, backslash, empty component, `.` or `..`. All files read by the audit must resolve to regular files inside the study directory. Evidence and run outputs must be distinct from `research/plan.json`, `research/plan.sha256`, `research/run.json`, `research/claims.json`, `research/paper.md` and, when present, `research/sources.json`. The check compares file identities, including symbolic and hard links.

## Output and exit status

The audit prints one JSON object. It reads the artifacts without executing the experiment. `run` describes the **audit**, while `scientific_run` gives the status read from the run record, or `null` if unavailable. `claims` maps claim IDs to their recorded status after local checks, or `invalid` for a failed claim.

`criterion_coverage` reports `required_observations` and `verified_observations` counts by criterion ID. A legacy criterion without cell requirements reports `0` and `0`, not a scientific pass.

`observation_outcomes` maps each criterion ID to an array with one `{path,key,column,outcome}` record per bounded observation. A criterion with no bounded observations has an empty array. The outcome is `met`, `missed` or `not_evaluated`. The last value means no comparison result was available. For the interval example, this field reads:

```json
{"estimate":[{"path":"research/results.csv","key":{"n":"8"},"column":"estimate","outcome":"missed"}]}
```

`source_records` counts the validated source entries, or is `null` when no registry was loaded. The `errors` and `incomplete` lists show up to 20 messages of up to 300 characters each. `error_count` and `incomplete_count` give the full counts.

| Exit | `run` | `deliverability` | Meaning |
|---|---|---|---|
| 0 | `complete` | `ready` | Every criterion has a claim, all registered claims are marked supported and the applicable file, evidence and observation checks pass. |
| 1 | `complete` | `incomplete` | The records are consistent, but a claim is not supported, an evidence gap remains or the scientific run failed or was blocked. |
| 2 | `invalid` | `blocked` | A required input is missing, a record is malformed or the manuscript, evidence or observations fail a check. |

## Compare two CSV outputs

From the workflow checkout, pass two distinct files to `checks/compare.py`, even when their contents are identical.

```sh
python3 checks/compare.py expected.csv actual.csv --id sample --column estimate --atol 0.001 --rtol 0.01
python3 checks/compare.py expected.csv actual.csv --id sample --labels cluster --min-ari 0.95
```

Select numeric columns with `--column NAME` (repeat for more columns), a cluster-label column with `--labels NAME`, or both. The selected columns and the ID column must have distinct names present in both files. Each ID must be nonblank, unique in its file and present on both sides. The comparator aligns rows by ID and ignores unselected columns.

Here the allowed absolute difference is $a + r\lvert x\rvert$, where $x$ is the expected value, $a$ is `--atol` and $r$ is `--rtol`. Equality at the threshold passes. Both tolerances default to zero. For cluster labels, the comparator uses the adjusted Rand index (ARI), so renaming clusters preserves the score. Labels must be nonblank. `--min-ari` defaults to 1 and accepts values from −1 to 1. Identical degenerate partitions, including a one-sample partition, score 1.

The JSON report gives `result`, `aligned_ids` (`null` if alignment did not complete), `ari` (`null` unless computed), `diagnostic_count` and a bounded `diagnostics` list. Exit `0` means match, `1` means different ID sets or results outside the requested thresholds, and `2` means invalid input or usage. CLI usage errors go to stderr.
