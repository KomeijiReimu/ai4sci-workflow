# Separate external integration check — not a comparison arm

A new standalone OpenCode process received `prompt.txt`, `study/scans.csv` and `study/field-note.md`. Its working directory and `PWD` were both `/mnt`, outside the read-only complete kit at `/media`. No prior model output or evaluator key was supplied. All 22 shared kit files were byte-identical to the paired trial; the complete snapshot added only `checks/sources.py`. The process ended with exit 0 in 228.089 seconds. It reported equally frequent logged warnings (Iris 4/80, Juniper 6/120, both 5%), not established equivalence or a causal device effect.

| Event | Actual command from the model session | Exit |
|---|---|---:|
| Freeze (the four data rows had already been read; the plan disclosed this) | `python3 /media/ai4sci.py freeze /mnt` | 0 |
| Formal computation | `python3 /mnt/analysis.py` | 0 |
| First evidence audit | `python3 /media/ai4sci.py audit /mnt` | 2 |
| Recheck after aligning manuscript C3 with its ledger statement | `python3 /media/ai4sci.py audit /mnt` | 0 |
| Optional statistical lint including the JSON plan | `python3 /media/ai4sci.py stats /mnt/research/paper.md /mnt/analysis.py /mnt/research/plan.json` | 1 |
| Optional lint of report and code only (no plan-adherence check) | `python3 /media/ai4sci.py stats /mnt/research/paper.md /mnt/analysis.py` | 0 |
| Computation rerun | `python3 /mnt/analysis.py` | 0 |
| Four later audit calls, including after source inventory and final edits | `python3 /media/ai4sci.py audit /mnt` | 0 each |

The first evidence audit rejected an exact-line mismatch for C3. The optional lint did not recognize `plan.json` as a statistical-lint input; the later successful lint checked only the files it recognized. The evaluator's final fresh offline audit on an unchanged copy exited 0 (`ready`, four marked claims, one source record). This establishes that the audited pipeline ran on this case, not that the checker independently established the model’s statistical interpretation. `../execution.json` gives command order, results and per-snapshot identity. The replay subset in `study/` has the original inputs and all files needed to rerun the logged computation and the structural audit.
