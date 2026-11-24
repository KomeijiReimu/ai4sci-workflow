# Record a branch decision

Use `research/branches.json` when a result leaves two plausible explanations and the choice of follow-up matters. A simple comparison needs no tree. The audit reads a tree if present. To require it from the start, add `"required_checks":["branches"]` to the plan before freezing. The audit does not launch experiments or choose what to study. See the [two-round encoding study](../examples/branch-decision/) for a runnable example and its [complete ledger](../examples/branch-decision/research/branches.json).

## Before measuring the children

1. Start from an actual measurement. Give `root` a unique `id` and a `result` such as `{"path":"research/bytes.csv","key":{"node":"raw"},"column":"bytes"}`. Use the [study's numeric cell format](contract.md#observations-and-matched-conditions). Each result needs one distinct CSV row in a declared run output. Reference the parent's existing row across comparisons rather than copying its score.
2. Set `direction` to `min` or `max`. Bind the evaluated units using `"population":{"path":"trace_file","sha256":"trace_sha256"}`. These are **CSV column names**. Each measured row supplies a study-relative path to its actual input or exact inventory of evaluated unit IDs, and its SHA-256 digest over raw bytes. Use the evaluated subset, not the whole dataset from which it was sampled. In `matched`, name other fixed columns such as sample count, metric unit, split or execution allowance. In `settings`, name the effective method parameters that the next rounds might vary. Both lists are nonempty. Use distinct names for these columns and the two population columns. Record actual values in each measurement row, not just the requested configuration in a note.
3. Append a round under `rounds`. Name the `parent`, the `observation` motivating the follow-up, two distinct `predictions`, the single setting to `vary`, and a positive integer `budget` in child attempts. List the `children`, each with a new `id` and a distinct proposed `value` as a CSV string. Leave their `result` absent until measured. Set `decision` to `{"kind":"pending","reason":"…"}`. Write these notes **before** measuring the children. The ledger records that account. Its writable contents cannot establish when a choice was made. Keep a separately dated copy when priority matters.
4. Append each result to its child. Keep the raw rows, including measured misses. When a technical problem prevents measurement, append `{"command":"…","exit":1,"log":"logs/attempt.txt","reason":"…"}` to that child's `failures` array. Record the actual exit, including `0` if the process exited normally without producing the observation. Each failed attempt costs one unit, as does the final measurement. A repair keeps the same proposed change. A measured miss is not a technical failure. Leave alternatives without attempts visible as untried.

## Close the decision

Every `decision` has a `kind` and a nonblank `reason`. Only `best` and `follow` take a `selected` child ID.

| Kind | What the record says |
|---|---|
| `best` | The selected child strictly improves on the parent and every sibling in the stated direction. All children must have comparable measurements. |
| `none` | There is no unique improving child. This covers a tie for best or no improvement on the parent. All children must have comparable measurements. |
| `follow` | Continue from a measured child for the stated scientific reason, such as investigating an adverse result. No scalar ranking is asserted. |
| `stop` | Close the round without selecting a child. Use this for an exhausted budget, an uninformative contrast or a deliberate stop with unmatched observations. |
| `pending` | A requested decision is still open. Name the evidence or action it needs. |

The scalar check reads the raw decimal cells, including the parent, before rounding. It verifies each population file's digest. Two copies of the same bytes match. Two different inventories called “development” do not. For an unordered set, write the IDs in a canonical order. The metric column and fixed condition values must also match, with exactly the requested single setting changed. Missing fields, wrong digests and ambiguous cell locators are invalid. A real measurement with different effective settings or observations stays in the tree as `incomparable`. `best` and `none` cannot rank it. A later round inherits the **selected child's** actual row, not the first round's baseline. Each parent opens at most one round. Siblings represent coequal alternatives, not successive improvements.

The report includes every recorded node and its parent. Measured children show `better`, `tie`, `adverse` or `incomparable` relative to that parent. A consistent closed tree returns `0`, an open decision returns `1`, and an invalid ledger or promotion returns `2`. The main audit also checks the rest of the study. Follow-ups on the same observations are exploratory. To claim confirmation, lock the choice and evaluate it separately on previously untouched independent units. A different seed or a renamed split does not make reused units independent.

For aggregate scores, the checker establishes which inventory each row cites. It does not trace which units contributed to an aggregate inside the experiment code. Review the inputs and commands for incorrect attribution, omitted conditions and scientific meaning. A best score only orders the declared measurements. It does not establish an explanation, independent confirmation or novelty.
