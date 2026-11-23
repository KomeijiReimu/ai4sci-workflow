# Artifact grades (one point per numbered item of `frozen-rubric.md`)

The evaluator wrote the key before the sessions and scored it afterward with arm labels visible. Scientific content and reproducibility were graded separately from the workflow's own evidence checker. `C1`–`C10` and `R1`–`R8` below denote the rubric items, not the manuscript's claim IDs. Line references refer to the original, unedited outputs under `outcomes/`.

| Counts criterion | Plain | Workflow | Where to verify (plain paper; workflow paper) |
|---|---:|---:|---|
| C1 pooled | 1 | 1 | lines 51–56; 39–58 |
| C2 covered cells | 1 | 1 | 36–49; 35–50 |
| C3 site mix | 1 | 1 | 51–57; 54–58 |
| C4 missing Amber–Quartz and observed Slate–Quartz | 1 | 1 | 28–34, 40–49; 37–50, 98–104 |
| C5 weighted covered sites | 1 | 1 | 59–70; 60–80 (rounded within tolerance; exact table supplied) |
| C6 full rates and bounds | 1 | 1 | 72–90; 66–90 |
| C7 tight nonzero lower bound; descriptive sign, unknown magnitude | 1 | 1 | 84–113; 84–96 |
| C8 nonrandom dispatch; primary locator | 1 | 1 | 21–29, 103–120; 15–23, 92–104 |
| C9 runnable computation | 1 | 1 | 122–143 and `compute.py`; 114–122 and `analyze.py`. Both independent reruns (with old outputs removed) exited 0 and reproduced all corresponding result-file bytes. See `execution.json`. |
| C10 machine-readable | 1 | 1 | plain `results.csv` rows 8–17; workflow `results.csv` rows 8–9 and 15–22. These CSVs use rates/proportions. |
| **Total / 10** | **10** | **10** | Same scientific grade despite different process artifacts. |

| Reading criterion | Plain | Workflow | Where to verify (plain reading list; workflow reading list) |
|---|---:|---:|---|
| R1 CPython default | 1 | 1 | lines 7–12; 9–14 |
| R2 interpolation vs rank convention | 1 | 1 | 10–12, 33; 12–14, 42 |
| R3 NumPy default and type | 1 | 1 | 14–19; 16–21 |
| R4 no universal identity from word “linear” | 1 | 1 | 3, 31–35; 5, 39–44 |
| R5 concrete method-aligned comparison | 1 | 0 | Plain 35 pairs CPython `inclusive` with NumPy `linear`, flagging the unavailable formula table. Workflow 46–54 lists required settings and the need to verify a crosswalk, but does not choose an aligned pair. |
| R6 bibliographic record only | 1 | 1 | 21–29; 23–37 |
| R7 traceable primary sources | 1 | 1 | 7–26; 9–26. Source versions, locators and article identity are present. |
| R8 reading-list-only delivery | 1 | 1 | Only `reading-list.md` was created by either arm. |
| **Total / 8** | **8** | **7** | Both rejected the unsupported endorsement in the digest. |

**Interpretation of R5.** The packet names NumPy's type 7 method but does not give its index formula. The plain arm's technically correct crosswalk is labelled interpretation and is not proved by the supplied material; the workflow arm explicitly declines to infer it. The fixed key requires the crosswalk, so the raw point stands. It does not establish that the plain reading list was better grounded. If the goal is strictly source-supported information, both earned all seven other items. The workflow reading list says “four supplied texts” although there were three files; it treats the missing article as a separate bibliographic entry. Neither list claimed to have read the article.
