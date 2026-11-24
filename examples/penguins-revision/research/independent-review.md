# Independent delivery review: the training-median comparison

**Reviewer:** Ninja, independent AI reviewer (nonblind), 2026-11-24 UTC. I did not author the study. I read the concern, paired tables and manuscripts before the recalculation.

**Decision: approved for delivery as a retrospective sensitivity analysis.** The run finished. All eight marked claims and the direction and scope of the unmarked conclusions are supported. In 119 scored records, switching from the training mean to the training median reduced the pooled line's MAE advantage from **384.707 g to 372.361 g**. It did not change a single original prediction. No revision remains open.

## What the added control tests

The [original manuscript](../original/research/paper.md) used the arithmetic mean, an intercept-only least-squares fit. The [original review, “Interpretation and verification”](../original/research/review.md#interpretation-and-verification) pointed out that a median, not necessarily the mean, minimizes training absolute error among constants. This is a question about the fairness of the comparison under MAE, not an error in the two original estimates. The [reply](response.md) quotes the concern accurately, locates the amended methods and results, distinguishes training optimality from test performance, and gives the direction and magnitude of the change. The [revised manuscript](paper.md) itself now identifies the concern, both controls and the consequence for the conclusion. I checked the earlier paper, the issue paragraph and reply in their own reading proofs and compared those passages directly with the rendered Word manuscript.

The [supplement](plan.json) specified one additional constant on the earlier split. Its frozen raw bytes match `4a76f82e2c0401ef446a5e92303a854e6e472a0d89cea60138134fde273c8391`. The local freeze receipt (07:52:33 UTC) precedes the recorded start (07:53:49 UTC) by 76 s on 2026-11-24. These are local records, not an external timestamp. The previous scores, concern and 2009 outcomes were already available. Independent calculation checks arithmetic; it does not turn these birds into a fresh confirmation sample. The manuscript appropriately restricts the result to complete records from the observed year/site and the pooled-species model; neither a within-species nor a causal or future-year effect is established.

## Cohorts, errors and byte checks

From the archived CSV, there were 110, 114 and 120 records in 2007, 2008 and 2009. Rows 4 and 272 lacked the required measurements: 223/224 training and 119/120 holdout records remained (C1–C2). Seven training and two test records without sex remained eligible. The recovered training mean was 4197.197309417 g; the median was 4050 g (C3). The intercept was −5477.164604778 g and slope 48.394596264 g/mm. Neither year nor species was a fitted covariate.

| Quantity on the same 119 test records | Independent estimate (g) | Manuscript (g) |
|---|---:|---:|
| Training-mean MAE (C4) | 710.455213476 | 710.455 |
| Training-median MAE (C5) | 698.109243697 | 698.109 |
| Pooled-line MAE (C6) | 325.748479323 | 325.748 |
| Mean-minus-line paired absolute error, averaged (C7) | 384.706734152 | 384.707 |
| Median-minus-line paired absolute error, averaged (C8) | 372.360764374 | 372.361 |

After fitting, alignment by original one-based row ID found no missing or extra IDs. Both measured fields agreed for each row in both versions. All 238 original predictions, all 357 revision predictions and all summary fields (13 original, 9 revision) matched exactly at stored precision. All five recorded arms matched the independently computed ordered train/test ID hashes and input hash. The median's lower test MAE is an observation, not a property guaranteed by the training criterion.

From the repository root:

| Check | Exit | Result |
|---|---:|---|
| `(cd examples/penguins-revision && sha256sum --check original.sha256 && sha256sum --check artifacts.sha256)` | 0 | 13 archive entries and 21 author-stage entries match. |
| `python3 -B ai4sci.py audit examples/penguins` | 0 | Six original claims supported; no required observation cells in the original plan. |
| `python3 -B ai4sci.py audit examples/penguins-revision` | 0 | `ready`, C1–C8, 8/8 planned observations, 2 source records, zero errors or incomplete items. |
| `python3 -B checks/submission.py examples/penguins-revision` | 0 | `ready`, eight final Word claims matched, none missing, no open revisions. The post-manifest evidence audit also reported manuscript and submission `ready`. |
| QR calculation below | 0 | NumPy 2.4.4; all rows, summary fields and cohort hashes matched. |

For each `<path>` in `original.sha256`, I checked the SHA-256 of the archive entry, the working `examples/penguins/<path-without-original/>` bytes and `git show 1c5d24060e1a1a67b551b1724427db3f77fefcb8:examples/penguins/<path-without-original/>`. All three matched the recorded digest for each of the 13 files, including the original paper, review, plan, input, script, run and results. The supplement plan pins the [archive inventory](../original.sha256) (`9549a9775684d9e56019b84d3e0ad7bb5e536bebe87628a920075abae21116b0`); the [author-stage inventory](../artifacts.sha256) itself hashed to `1076e81bc877abe2058690320dbed723e5bd65292ff2d94bf5edc0d532458322`.

I also fetched [DataCite release metadata](https://api.datacite.org/dois/10.5281/zenodo.3960218), the [pinned CSV](https://raw.githubusercontent.com/allisonhorst/palmerpenguins/e5bfd5f2c7da95b0823e9501b9013eb2ef124fa7/inst/extdata/penguins.csv) and [release dictionary](https://raw.githubusercontent.com/allisonhorst/palmerpenguins/e5bfd5f2c7da95b0823e9501b9013eb2ef124fa7/man/penguins.Rd). The release identifies Horst, Hill and Gorman, v0.1.0; the dictionary confirms Gorman/LTER attribution, setting, grams and millimeters. The remote CSV was 15,241 bytes, SHA-256 `f204db2c753b0937caac3cb35258562c14f073e4bbc76be24b4c51ce22767a93`, identical to the archived input.

## Inspection of the submitted Word file

I opened a byte-identical copy of **`paper/final.docx`** (10,992 bytes, SHA-256 `fae0abd6f8c6376771aec693bb109eb558adedb03878893ab5518b881be4377c`) with an isolated **LibreOffice Writer 25.2.3.2**. I inspected both full page images from its PDF export. The Letter pages are legible: p. 1 shows the concern and median rationale, linked source, split, sample counts, all three MAEs and both signed advantages with units, followed by the warning that this is not confirmation on fresh data. The last three lines on p. 2 complete the interpretation about complete cases, species composition, causality and prediction in another year. This is a sparse final page, not missing text. There is no clipping, overlap, detached heading or cropped number. There are no tables, figures, equations or captions in this submission. This verifies this Writer layout (DejaVu Serif), not identical pagination in Microsoft Word.

The DOCX ZIP passed its integrity test. I parsed `word/document.xml` (4,899 bytes, SHA-256 `381964cd831b5f2c4dab74d5b0e9509698592e357bef26be119df18ba0d6df3f`), inspected its hyperlink relationship to the release DOI and read all 16 body paragraphs. They match all 16 canonical paragraphs after removing Markdown syntax and ledger markers. There were no tables, drawings, fields, tracked insertions/deletions or directly hidden runs. Each of C1–C8 also appears verbatim on p. 1 of the Writer PDF. Comparing the complete visible text with the XML found only a line wrap after the literal hyphen in the title's “training-median.”

The renderer was extracted locally from signed Debian `trixie`/`trixie-security` packages (`libreoffice-writer-nogui` 4:25.2.3-2+deb13u12), without a system install. Its `BRAND_BASE_DIR`, suite symlinks and packaged `main.xcd` registry were relocated within the ignored cache. The fresh profile requested one restart (81); the conversion below, `pdfinfo` and `pdftoppm` all exited 0. Writer warned about the system language-subtag XML path in this relocated suite; the inspected pages contained the complete English text. Commands from checkout root with the staged suite:

```sh
D="$PWD/.local/maturity-render"; R="$D/root"; P="$R/usr/lib/libreoffice/program"
cmp examples/penguins-revision/paper/final.docx "$D/input/final.docx"
env -i HOME="$D/home" TMPDIR="$D/tmp" XDG_CACHE_HOME="$D/cache" XDG_CONFIG_HOME="$D/xdg" XDG_DATA_HOME="$D/home/data" LANG=C.UTF-8 PATH=/usr/bin:/bin LD_LIBRARY_PATH="$P:$R/usr/lib/x86_64-linux-gnu" SAL_USE_VCLPLUGIN=svp URE_BOOTSTRAP="vnd.sun.star.pathname:$P/fundamentalrc" "$P/soffice.bin" "-env:UserInstallation=file://$D/profile" --headless --norestore --convert-to pdf:writer_pdf_Export --outdir "$D/pages" "$D/input/final.docx"
pdfinfo "$D/pages/final.pdf"
pdftoppm -r 128 -png "$D/pages/final.pdf" "$D/pages/final"
sha256sum "$D/pages/final.pdf" "$D/pages"/final-*.png
```

| Local rendering receipt (`.local/maturity-render/pages/`) | SHA-256 of inspected bytes |
|---|---|
| `final.pdf` (2 pages, 612 × 792 pt, 39,173 bytes) | `6a377cf27fba32bfd4125f9d0c2e3cf0466fbf17f2c973b69278ab334ef185ca` |
| `final-1.png` | `f552f65b90967fa0fd37d9a91dc8d97af1d1dbe5a23c239c32f8ff9dbb636681` |
| `final-2.png` | `61bc36396dc313f9cf952144e9ee19391495653b3e48c2639a95afd8bb896cac` |

The separate Markdown reading proofs of the *earlier* paper, reviewer paragraph and reply used Pandoc HTML and PyMuPDF Story. Those images are in the ignored `companion/` cache; none was used as the Word proof. The [delivery record](delivery-review.json) binds this decision to the exact Word file, canonical manuscript and ledger.

## Reproducible numerical check

From the repository root, the following read-only check uses NumPy's reduced QR factorization on a two-column training matrix. Subtracting 200 mm from its second column changes the intercept's parameterization, not the fitted line. Neither study script nor the earlier reviewer's verifier is imported or executed. Expected tables are opened only after training, prediction and scoring.

```sh
cd examples/penguins-revision
OPENBLAS_NUM_THREADS=1 python3 -B - <<'PY'
import csv, json
from hashlib import sha256
from pathlib import Path
import numpy as np

def rows(path):
    with Path(path).open(newline='') as f: return list(csv.DictReader(f))
raw = Path('original/data/penguins.csv')
data = rows(raw)
def field(r, k): return np.nan if r[k] in ('', 'NA') else float(r[k])
x, y = (np.array([field(r, k) for r in data]) for k in ('flipper_length_mm', 'body_mass_g'))
years = np.array([int(r['year']) for r in data]); ids = np.arange(1, len(y)+1)
assert set(years) == {2007, 2008, 2009}
ok = np.isfinite(x) & np.isfinite(y); tr = ok & (years != 2009); te = ok & (years == 2009)
X = np.column_stack((np.ones(len(y)), x - 200)); Q, R = np.linalg.qr(X[tr])
a, b = np.linalg.solve(R, Q.T @ y[tr]); const = np.mean(y[tr]); med = np.quantile(y[tr], .5)
obs = y[te]; pred = np.column_stack((np.full(len(obs), const), np.full(len(obs), med), X[te] @ [a, b]))
err = np.abs(pred - obs[:, None]); em, ed, el = err.mean(axis=0); dm, dd = (err[:, :2]-err[:, [2]]).mean(axis=0)
print('NumPy', np.__version__, 'year counts', np.unique(years, return_counts=True)[1], 'excluded IDs', ids[~ok]); print('eligible', tr.sum(), te.sum(), 'retained missing sex', *[sum(data[i-1]['sex'] in ('','NA') for i in ids[v]) for v in (tr,te)])
print('mean, median, intercept, slope', *[f'{v:.9f}' for v in (const,med,a-200*b,b)])
print('MAEs and reductions (g)', *[f'{v:.9f}' for v in (em,ed,el,dm,dd)])
values = dict(test_year=2009, train_total=sum(years!=2009), train_used=tr.sum(), train_excluded=sum((years!=2009)&~ok), test_total=sum(years==2009), test_used=te.sum(), test_excluded=sum((years==2009)&~ok), train_mean_g=const, train_median_g=med, intercept_g=a-200*b, slope_g_per_mm=b, mean_mae_g=em, median_mae_g=ed, linear_mae_g=el, mean_minus_linear_g=dm, median_minus_linear_g=dd, reduction_g=dm)
expected_arms = {'training_mean','flipper_ols'}
conditions = dict(input_sha256=sha256(raw.read_bytes()).hexdigest(),metric='MAE (g)')
for split, mask in [('train',tr),('test',te)]:
    conditions[split+'_row_ids_sha256']=sha256(''.join(f'{i}\n' for i in ids[mask]).encode('ascii')).hexdigest()
for original in (True,False):
    root = Path('original/research' if original else 'research')
    result, = rows(root/'results.csv')
    assert all((f'{values[k]:.9f}' if '.' in v else str(values[k]))==v for k,v in result.items())
    records = rows(root/'predictions.csv'); byid={int(r['row_id']):r for r in records}
    assert len(records)==len(byid)==len(obs) and set(byid)==set(ids[te]); compared=0
    for idx, length, mass, pr in zip(ids[te],x[te],obs,pred):
        r=byid[idx]; assert (int(r['flipper_length_mm']),int(r['body_mass_g']))==(length,mass)
        for j,k in enumerate(['mean_prediction_g','median_prediction_g','linear_prediction_g']):
            if j==1 and original: continue
            assert f'{pr[j]:.9f}'==r[k]; compared+=1
    receipt=json.loads((root/'run.json').read_bytes())
    assert {arm['id'] for arm in receipt['arms']}==expected_arms | (set() if original else {'training_median'})
    assert all(arm['conditions']==conditions for arm in receipt['arms'])
    print(root, len(result),'summary fields,',len(records),'distinct IDs,',compared,'predictions match')
print('ID/source hashes and metric:', conditions)
PY
```
