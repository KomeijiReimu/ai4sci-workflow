# Offline research audit

The audit checks a frozen plan, a run record and the evidence for marked statements in a manuscript. With Python 3.10 or later, run `python3 ai4sci.py audit PROJECT` from the workflow checkout. `PROJECT` is the study directory, for example `studies/my-study` or an absolute path to an external study. From the study itself, run `python3 /path/to/ai4sci-workflow/ai4sci.py audit .` using the actual checkout path. Paths inside the manifests are always relative to the study root.

## Minimal study

`research/plan.json`:

```json
{"question":"What is the estimate at the agreed sample size?","criteria":[{"id":"estimate","description":"Report the estimate and identify the method."}]}
```

Before running the experiment, record the plan digest with `python3 ai4sci.py freeze PROJECT` from the checkout. This creates `research/plan.sha256` in the study directory.

`research/results.csv`:

```csv
n,estimate
8,0.12497
```

`research/source.md` contains the exact text `The estimate is the sample mean.`

`research/run.json` records the command that produced the CSV:

```json
{"status":"completed","command":"python3 measure.py","outputs":["research/results.csv"]}
```

`research/claims.json`:

```json
{"claims":[{"id":"C1","criterion":"estimate","statement":"At n=8 the estimate is 0.125.","status":"supported","evidence":[{"kind":"number","path":"research/results.csv","key":{"n":"8"},"column":"estimate","value":0.125,"display":"0.125","atol":0.00005}]},{"id":"C2","criterion":"estimate","statement":"The estimate is the sample mean.","status":"supported","evidence":[{"kind":"quote","path":"research/source.md","quote":"The estimate is the sample mean."}]}]}
```

`research/paper.md`:

```markdown
# Estimate

At n=8 the estimate is 0.125. [C1]

The estimate is the sample mean. [C2]
```

## Plan and run record

- `research/plan.sha256` must contain the 64-character lowercase hexadecimal SHA-256 digest of the raw `research/plan.json` bytes followed by a single LF. Changing even whitespace in the plan changes its digest. Comparing the two local files checks for drift; independently attesting when the plan was frozen requires a separate record.
- `research/run.json` is required. A `completed` experiment needs a nonblank `command` and a nonempty `outputs` array of distinct project-relative regular file paths. Include every CSV cited as numeric evidence in `outputs`. A measured negative result belongs in a completed run; record the observation and cite its data.
- For `failed` or `blocked`, give a nonblank `reason` and record which claims remain untested. A consistent record of either outcome is `incomplete`. For a literature-only study, use `not-applicable` with a nonblank reason and cite quotations, including for numbers reported by a source.
- Use UTF-8 for manifests, the manuscript, CSVs and quoted sources. Each JSON manifest has an object at its root. Keys within each object must be unique; numeric values must be finite. Additional metadata fields are ignored. The plan needs a nonblank `question` and a nonempty `criteria` array. Each criterion has a unique nonblank string `id` and nonblank `description`.
- Optional output integrity: `sha256` in `research/run.json` maps **every** listed `outputs` path (and no others) to its lowercase 64-character SHA-256 over raw file bytes. Without this map the audit does not verify output digests.
- Optional controlled comparison: freeze `"matched_conditions":["threads","dataset"]` in the plan (distinct nonblank names, for experiments only). A completed run must then record at least two arms with distinct IDs, e.g. `"arms":[{"id":"old","conditions":{"threads":1,"dataset":"A"}},{"id":"new","conditions":{"threads":1,"dataset":"A"}}]`. For each named condition, every arm must declare the same scalar value (nonblank string, number or Boolean, without coercion between these types). The audit compares the declared settings; the reviewer can use the execution logs to check the settings actually used. Extra conditions are ignored.

## Claim ledger and manuscript

- Every criterion needs at least one claim (even if untested). Each claim has a unique `id` matching `C[1-9][0-9]*`, one `criterion` referencing a plan ID, a unique nonblank single-line `statement`, `status`, and an `evidence` array. Put the exact statement, one space, and `[ID]` alone on a manuscript line (outer line whitespace ignored). No embedded claim markers. `[C` followed by digits and `]` is reserved everywhere in the manuscript: exactly one per claim, no unknown markers. Ordinary prose without these markers is **not** audited.
- A `number` record must select **one** data row using a nonempty `key` object. All key values are nonblank strings, compared as literal CSV fields. `column` names a non-key result field. `value` and `atol` are mandatory JSON numbers. Set `atol` to a nonnegative absolute tolerance appropriate to the reported precision. The CSV value must lie within that tolerance of `value`. `display` is a string representing exactly `value`; if omitted, the check uses Python's string form of the parsed JSON number. Set it explicitly for scientific notation or any formatting that matters.
- `display` must occur as a standalone signed decimal token in the statement, not inside an ASCII identifier or another number. Numbers may adjoin Chinese prose, e.g. `误差为0.74。`. For supported and partial claims **every numeric token** requires a display binding, except explicit `column=value` key contexts from that claim's verified numeric records (e.g. `n=8`). Use spaces between numbers and ASCII units, a decimal point, no digit grouping, and separate key contexts from results. Values refer to the same units as the CSV, with no implied percentage conversion.
- For a number reported by a source, use a `quote` record with `"displays":["85.2"]`. Each listed spelling must be distinct and occur as a numeric token in both the quotation and the claim. The checker verifies transcription; the reviewer checks which statistic, unit and population the passage describes and whether it supports the interpretation.
- A `quote` needs `path` and a nonblank `quote` that is a case-sensitive literal substring of the UTF-8 text file (universal-newline translation). CSVs require nonblank unique headers, at least one row and consistent field counts. Evidence file paths must use relative `/`-separated components, no drive, backslash, empty, `.` or `..` components. All inputs including manifests must resolve to regular files within PROJECT, including through symlinks. Reusing evidence across claims is allowed; duplicate locators within one claim are not.
- Evidence files and declared outputs must be distinct from the five control files: `research/plan.json`, `research/plan.sha256`, `research/paper.md`, `research/claims.json` and `research/run.json`. The audit compares file identities, including for symbolic and hard links.
- `supported`, `partial` and `contradicted` require at least one verified number or quote. `unsupported` and `untested` may have an empty evidence array. Declare known gaps with `{"kind":"incomplete","reason":"Replicate pending"}` or `{"kind":"blocked","reason":"Source unavailable"}`. A gap cannot serve as the required evidence or appear in a `supported` claim. For `contradicted`, a reviewer assesses whether the source conflicts with the statement. Citing a missing file produces an input error.
- Decimal parsing for comparisons uses exact rational arithmetic: ordinary signed decimals, optionally with a base-10 exponent; no whitespace, NaN, infinity or thousands separators. Compared numeric spellings are limited to 100 characters, with absolute decimal exponent (after accounting for fractional digits) at most 1000.

## Output and exit status

Stdout is a JSON object. `run` describes the **audit**. `scientific_run` reports the status declared in the run record, or `null` if that status could not be read and validated. The checker reads the artifacts without executing the experiment. `claims` maps claim IDs to their recorded status after local checks (`invalid` for a claim that failed). `deliverability` summarizes the study. Errors and pending reasons have separate counts; each list shows up to 20 messages of up to 300 characters each.

| Exit | run | deliverability | Meaning |
|---|---|---|---|
| 0 | complete | ready | Every agreed criterion covered and all recorded claims supported by structurally verified evidence. |
| 1 | complete | incomplete | Consistent record, but a claim is not supported or scientific run failed/blocked. Reasons include declared blocked/incomplete evidence. |
| 2 | invalid | blocked | Missing required input, invalid schema, unaligned manuscript, uncovered criterion, or inconsistent evidence. |

## Compare two CSV outputs

From the workflow checkout, pass the paths of the two study outputs to `checks/compare.py`. The reference and actual outputs must be distinct files, even when their contents are identical.

```sh
python3 checks/compare.py expected.csv actual.csv --id sample --column estimate --atol 0.001 --rtol 0.01
python3 checks/compare.py expected.csv actual.csv --id sample --labels cluster --min-ari 0.95
```

Select numeric columns with `--column NAME` (repeat for more columns), a cluster-label column with `--labels NAME`, or both. The selected columns and the ID column must have distinct names, present in both files. Each ID must be nonblank, unique in its file and present on both sides. The comparator aligns rows by ID and ignores unselected columns.

For numbers, the allowed absolute difference is $a + r\lvert x\rvert$, where $x$ is the expected value, $a$ is `--atol` and $r$ is `--rtol`. Equality at the threshold passes. Both tolerances default to zero. For cluster labels, the comparator measures agreement of the partitions using the adjusted Rand index (ARI), so renaming clusters preserves the score. Labels must be nonblank. `--min-ari` defaults to 1 and accepts values from −1 to 1. Identical degenerate partitions, including a one-sample partition, score 1.

Stdout JSON reports `result`, the number of aligned IDs (`null` if alignment did not complete), `ari` (`null` unless computed), the number of diagnostics and a bounded preview. Exit `0` means match, `1` means different ID sets or results outside the requested thresholds, and `2` means invalid input or usage. CLI usage errors go to stderr.
