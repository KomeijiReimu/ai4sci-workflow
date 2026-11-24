# Check the requested final manuscript package

For final delivery, require both the [evidence audit](contract.md) and the package check in one run:

```sh
python3 ai4sci.py audit --submission studies/my-study
```

The ordinary `python3 ai4sci.py audit studies/my-study` command also checks the package when it finds `research/submission.json`. Without the manifest, it checks only the evidence. Add `--submission` to require the manifest. For isolated **package diagnostics**, use `python3 checks/submission.py studies/my-study`. That command does not rerun the evidence audit and cannot clear a study for delivery by itself.

The package check is read-only. It does not edit, render or compile files, install anything, fetch sources or run the experiment. It compares current package bytes with a dated review record and looks for **each audited claim statement in the final document text**. Passing both checks does not establish scientific validity.

## Declare the files

`research/submission.json` has one requested `format`, an `artifacts` object, and a reference to a separate review record. Example shape (replace angle-bracket placeholders with actual SHA-256 values):

```json
{
  "format": "docx",
  "artifacts": {
    "docx": {"path": "paper/final.docx", "sha256": "<docx digest>"}
  },
  "review": {"path": "research/delivery-review.json", "sha256": "<review digest>"}
}
```

| Requested format | Exact artifact keys | What is compared with the ledger |
|---|---|---|
| `docx` | `docx` | Paragraphs from the Word main document body |
| `pdf` | `pdf` | Page text emitted by `pdftotext` |
| `latex+pdf` | `tex`, `pdf` | The **PDF page text**, not the TeX source |

For instance, a `latex+pdf` package uses `"artifacts":{"tex":{"path":"paper/main.tex","sha256":"<tex digest>"},"pdf":{"path":"paper/final.pdf","sha256":"<pdf digest>"}}`. Supply nonempty files with matching extensions. The `.tex` entry must contain UTF-8 source with content other than comments. Separately check that the source compiles, that the resulting PDF matches the one delivered and that any supplementary build files have been reviewed.

If the recipient explicitly requests a **marked-up redline**, supply it as a separately named companion (for example, `paper/changes.docx`) alongside the clean primary. Do not substitute the redline for `final.docx`/`final.pdf` or list it as another primary artifact. The package report covers only the declared clean manuscript, so confirm the redline's contents and delivery separately. An open issue in the clean manuscript is still an open revision.

Paths use `/`-separated components relative to the study. No absolute names, `.`/`..`, backslashes, drive prefixes or outside symlinks. Files with different package roles must be distinct regular files (including hard-link identity). Do not use the deliverables, package manifest or review as evidence for themselves. The canonical files are always `research/paper.md` and `research/claims.json`. JSON must be UTF-8 with no duplicate keys. A digest is 64 lowercase hexadecimal characters over **raw file bytes**. For example, from the study directory run `sha256sum research/paper.md research/claims.json paper/final.docx`.

## Obtain the external review record

Review the rendered pages of the actual final DOCX/PDF. The reviewer can be a human, a separate AI with access to those pages, or the author performing a self-check. Identify who reviewed the pages. Do not describe a self-check as independent or programmatic extraction as visual inspection. Compare the conclusions, key numbers, units and qualifications with the canonical claims and evidence. On the rendered pages, inspect the tables, equations, captions, references and pagination. Record what was actually inspected, limitations and remaining issues. If rendered inspection is still pending, say so and use `needs-revision`. Example `research/delivery-review.json` (illustrative, not a completed review):

```json
{
  "reviewer": "Reviewer name or accountable role",
  "date": "2025-03-12",
  "status": "approved",
  "visual_inspection": "Opened the final DOCX in Word. On p. 2, compared the estimate and its units to C1 and Table 1; Table 1 fits on the page. Read the remaining pages for contradictory or unmarked conclusions.",
  "open_revisions": [],
  "sha256": {
    "research/paper.md": "<canonical paper digest>",
    "research/claims.json": "<ledger digest>",
    "paper/final.docx": "<docx digest>"
  }
}
```

The review digest map must name exactly the canonical paper, ledger and all requested artifacts by their declared paths. Date is a real, nonfuture `YYYY-MM-DD`. `needs-revision` or any item in `open_revisions` prevents `ready`, even if the reviewer wrote `approved`. If the paper, ledger or any final file changes, save a new dated review. **Updating the hashes alone does not renew the review.** Finally hash the separate review file and put that digest in the submission manifest. The review cannot be the submission manifest itself. The note records the inspection. The program cannot authenticate the reviewer, the date, the note or the reviewer's independence. Preserve an externally dated/signed copy if those properties matter. Do not invent an inspection just to complete a manifest.

## What counts as final claim text?

Keep each ledger `statement` intact in the final manuscript. **It need not be a separate paragraph.** For a canonical line `At n=8 the estimate is 0.125. [C1]`, this final paragraph matches: `We repeated the run. At n=8 the estimate is 0.125. Precision remains limited.` The claim ID is optional in the final. `It is not true that At n=8 the estimate is 0.125.` does not match. A bare ID, digest, metadata field or paraphrase is not a substitute. The canonical Markdown still requires each exact marked line as in the evidence audit.

Inside a paragraph, the statement must start and end at sentence boundaries. The checker recognizes `.`, `!`, `?` followed by a space or paragraph end, and `。`, `！`, `？` even without spaces. It folds whitespace but not case, signs, digits, punctuation, units or words. A ledger fragment without a sentence stop matches only an entire extracted paragraph (optionally followed by its marker). These are punctuation rules, not a language model: abbreviations and unusual typography can make boundaries ambiguous.

- **DOCX:** The checker reads the package relationship and content type for `word/document.xml` in a transitional OOXML package. It reads ordinary body and table-cell paragraphs, joining text across runs, including hyperlinks. It does not search ZIP bytes, comments, document properties, deleted text, field instructions or text inside drawings. Directly hidden runs are not used. Common tracked changes in the main body require resolution. Complex paragraphs (fields, equations, content controls, etc.) may not be extractable. Provide a separate ordinary conclusion-bearing paragraph rather than weakening the match.
- **PDF:** Install nothing during the check. `pdftotext` (Poppler) must already be on `PATH`. Blank lines separate text blocks. Within a block on the same page, the checker folds line wraps when matching sentences. A physical line break alone does not turn a qualification on the preceding line into a separate sentence. Blank/image-only pages do not supply claim text. No OCR is performed, including in the LaTeX case. Split-page wrapping, multicolumn reading order, ligatures, equations and discretionary hyphenation can block an otherwise legible manuscript. Inspect the final file rather than treating a failure as scientific refutation.

Extraction is **not** rendered or semantic verification. Styles, colors, overlays, clipping and a PDF's hidden/OCR text layer can make extracted text differ from what the reader sees. A matching passage cannot rule out a contradictory result elsewhere, wrong table labels, unsupported unmarked prose, or an inappropriate citation. The reviewer must check those. Byte hashes detect changes, not truth, provenance, aesthetics or approval.

## Result

The isolated package checker prints one JSON object. `content_check` identifies the extractor and lists the matched and missing claim IDs. If the checker could read and validate the bound review, `review` describes it. `errors` and `incomplete` give reasons. Processing may stop at the first invalid input, so a claim's absence from `missing_claims` does not mean it passed a blocked check.

| Exit | `deliverability` | Meaning for this package check only |
|---|---|---|
| 0 | `ready` | Bound review records approval, no open revisions, all canonical supported claim text found. |
| 1 | `incomplete` | Inputs checked but a ledger claim is not supported, revisions are open, or the review requests changes. |
| 2 | `blocked` | Invalid/missing files, stale digest/review, extractor unavailable, malformed document, or missing required text. |
