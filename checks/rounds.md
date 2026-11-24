# Check a revision across review rounds

Use this optional check when several reviewers or follow-up rounds make it hard to tell which version answered a concern. A first draft, advice about an editorial decision, and a straightforward single reply do not need a trail. For a working example with two disagreeing reviewers, see the [climate note demonstrator](../examples/review-rounds/).

From the checkout, run `python3 checks/rounds.py STUDY`. This read-only command needs no experiment plan or run record. For a study conducted with this kit, also run its [evidence audit](contract.md). Do not recreate a historical plan for a supplied manuscript.

## Keep the versions

Save the original manuscript, then a separately named manuscript and reply for each round. Keep the exact incoming comments and their sources. For example, `versions/note-v1.md` should remain available after you write `versions/note-v2.md`. In each reply include one line naming its manuscript, such as:

```text
Manuscript version: `versions/note-v2.md`
```

Put the Markdown and reply being handed over in `research/paper.md` and `research/reply.md`. These must be byte-for-byte copies of the last archived pair, not links to the archive. If a venue requests Word or PDF, also preserve the actual rendered manuscript as described below.

## Record the issues

The [example `research/rounds.json`](../examples/review-rounds/research/rounds.json) is a complete input. At the top level, `original` binds the starting `.md` and `rounds` is a nonempty list in chronological order. Each round declares `manuscript`, `reply`, `comments` and `decisions`. A file reference has a study-relative `path` and `sha256` over the raw bytes. Use `sha256sum` on the actual files. Different versions and roles need distinct files. Evidence can be cited more than once.

**Comments refer to the preceding manuscript.** Give each atomic concern a unique comment `id` (such as `B2`), a `reviewer`, the verbatim `comment`, and a `location` that is an exact line in the manuscript reviewed, such as its section heading. Assign an `issue` (`I1`, `I2`, …). A genuinely new scientific question gets a new issue ID. A follow-up, duplicate or conflicting request about the same point gets a new comment ID on the existing issue. That automatically reopens a closed issue. Never reuse an old comment ID for new words. If a single editorial comment contains two questions, retain the original and use related references like `B2a` and `B2b`.

**Decisions refer to this round's actual files.** Each decision has an `issue`, a `status` and a `response`. Copy one complete line from the actual reply as the response. Include `[I1]` and each of that issue's comment references to date, such as `[A1] [B2]`. Use the reply to explain what changed, or why it should not change. When reviewers disagree, answer both requests and explain why the evidence favors the chosen wording. Record a remaining disagreement as open when it still affects the scientific conclusion.

| Status | What the checker looks for |
|---|---|
| `revised` | The complete `passage` occurs on exactly one line of the revised manuscript and was absent as a line from the preceding version. |
| `no-change` | The same `passage` was already present and remains in the current version. Justify keeping it in the actual reply and cite the evidence. |
| `open` | The reply can report the outstanding question, a missing datum or a deferred action. Neither a promise nor a new reply closes it. |

A new comment with no decision stays open. A follow-up on a previously closed issue with no decision stays reopened. Unchanged decisions carry forward, so a later reply can address only the new comments. Each closed issue's passage must still be in every later version unless the issue reopens. If a coauthor changes a previously closed passage, log what changed and recheck the issue.

**Closing an issue needs evidence outside the paper and reply.** Supply a nonempty `evidence` list. Each entry binds a UTF-8 file by `path` and `sha256` and gives an exact `quote` to locate in that file. For example, use a complete CSV row and state the columns and calculation in the reply. The `passage` independently locates the corresponding result in the manuscript. It can be a translation, a paraphrase or a computed quantity. Set `verbatim` to `true` only for text or a reported value that should appear literally in both places. That option checks token boundaries too, so `1.6` cannot stand in for `11.6` or `1.60`. If only a gap can be documented, leave the issue open.

## Formal Word or PDF delivery

In each round that produces a formal package add `package: {"path":"versions/note-v2.pdf","sha256":"…"}` with the actual DOCX or PDF snapshot. Keep earlier packages. The latest package must match the primary DOCX or PDF bytes declared in [`research/submission.json`](submission.md). The rounds check runs the existing submission check. Each closed issue's passage in the current canonical `research/paper.md` must be a complete marked ledger line whose statement the submission checker found in the delivered document. For LaTeX delivery, bind the PDF here. The submission manifest also binds the editable TeX source. Review layout, figures, and any edits outside the registered claim text on the rendered pages.

## Interpret the result

| Exit | Meaning |
|---|---|
| `0` | The declared trail is consistent and all recorded issues are closed in the files checked. |
| `1` | A recorded issue remains open or reopened, or the formal package check reports an unresolved revision. |
| `2` | A file, digest, locator, version or transition is missing, stale or inconsistent. A blocked package check also gives `2`. |

`history` shows the issues opened or reopened in each round and their states at the end of that round. `issues` shows the latest states reached. Read `errors` first if the check stopped early. The output does not certify reviewer identity, establish the date of a file, or count a reasoned disagreement as reviewer assent. Hashes kept with editable files are not authentication. Retain original correspondence and externally dated copies where provenance matters.

An independent reader should open the exact files returned, compare each response with its passage in context and read the cited source or recompute the result. The check uses Markdown source lines, not rendered visibility or scientific meaning. It cannot detect an omitted comment, a contradictory caption elsewhere, or a true number applied to the wrong population. Name the person or separate AI that actually read the manuscript and list any outstanding judgments. Identify an author's own inspection as a self-check.
