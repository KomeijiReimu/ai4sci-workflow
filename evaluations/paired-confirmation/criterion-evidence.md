# Confirmation scores against the unchanged key

`R1`–`R8` and `C1`–`C10` use the item order in `frozen-rubric.md` (not manuscript claim IDs). One point per item, no half credit. All line locators refer to the unedited generated outputs under `outcomes/`. No score is awarded for workflow-specific scaffolding or audit status.

## Reading lists

| Item | Plain | Workflow | `reading-list.md` evidence: plain; workflow |
|---|---:|---:|---|
| R1 CPython default | 1 | 1 | 30–44; 9–23 |
| R2 interpolation and rank/endpoint convention | 1 | 1 | 37–51; 19–23, 55–60 |
| R3 NumPy default and type 7 | 1 | 1 | 11–28; 3–5, 25–35 |
| R4 no universal equivalence from “linear” | 1 | 1 | 78–96; 55–62 |
| R5 concrete method-aligned pair | 1 | 1 | 98–110; 3–5, 57–68. Both pair CPython `inclusive` with NumPy `linear` and identify that the packet does not prove the mapping. |
| R6 unread article treated as bibliographic metadata | 1 | 1 | 53–66; 37–43 |
| R7 traceable primary versions, methods and locators | 1 | 1 | 11–31, 53–66; 9–43 |
| R8 stop at requested reading list | 1 | 1 | Only new file in each finished workspace was `reading-list.md`. |
| **Total** | **8/8** | **8/8** | Both retain the evidence limitation. Exact formulas are absent from the packet, although some CPython branch arithmetic is visible. |

## Registry reports

| Item | Plain | Workflow | `research/paper.md` evidence: plain; workflow |
|---|---:|---:|---|
| C1 crude pooled rates and direction | 1 | 1 | 41–51; 23–32 |
| C2 common sites' four rates and direction | 1 | 1 | 28–43; 23–38 |
| C3 explanation by differences in composition | 1 | 1 | 47–51; 23–38 |
| C4 Amber–Quartz absent, Slate–Quartz observed | 1 | 1 | 19–26, 28–43; 17–34, 65–69 |
| C5 normalized weights, both weighted rates and contrast | 1 | 1 | 44–63; 13–15, 40–51 (50/80 and 30/80 are the correct weights) |
| C6 full-target rates, both endpoints and derivation | 1 | 1 | 65–89; 42–57 |
| C7 sharp contrast bounds, positive sign, unknown point value | 1 | 1 | 79–89; 53–65 |
| C8 descriptive interpretation and primary allocation evidence | 1 | 1 | 13–26, 91–105; 7–11, 59–73 |
| C9 runnable computation from data, **not hardcoded answers** | 0 | 1 | Plain 117–125 advertises both result files, including exact fractions; `analysis/analyze.py`'s `exact_fractions` object encodes ten literal answers. The primary CSV and most of the JSON are genuinely computed. Workflow 83–91 and `research/analyze.py` compute all reported table values. Both programs reran with exit 0 and byte-identical outputs on the original data. |
| C10 machine-readable pooled, weighted and bounded comparisons | 1 | 1 | Plain `analysis/results.csv` has `scope`, `route`, `value`, `unit`; workflow `research/results.csv`, rows 2–17, rates/proportions in `value/lower/upper`. |
| **Total** | **9/10** | **10/10** | All requested scientific numerical answers and conclusions are correct in both reports. The sole deduction is for **part of the additional JSON output**, not the CSV or the frozen-data arithmetic. |

**Hardcoding check.** Plain's auxiliary `exact_fractions.full_diff_lower` is the literal `1/200` in the script. To verify the practical consequence, the evaluator moved one on-time tile from batch K07 to K09 on disposable copies of **both** studies, preserving total counts. Both programs exited 0 and both CSVs correctly changed the lower bound to 13/1200 (about +1.08333 percentage points). Plain's computed JSON likewise changed, but its advertised exact-fraction field still said `1/200`. This is an explicitly post-hoc diagnostic of the pre-existing C9 restriction, not a model run, new scoring item, or replacement input for the official rerun. A CSV-only reading would find both core computations correct. See `execution.json` for the rerun hashes and diagnostic values.
