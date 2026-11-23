# Reading list: “linear” is not a shared quantile definition

**Short answer: No.** “Linear” describes interpolation between order statistics; it does not identify a unique sample-quantile estimator. The supplied records give different defaults: CPython’s `statistics.quantiles` defaults to `method='exclusive'` (with `m = ld + 1`), while NumPy’s `numpy.percentile` defaults to the enumerated method `'linear'`, item 7 of nine H&F types. Nothing in the packet equates those defaults, and no record states an equivalence for all finite samples.

## Annotated reading list

### 1. CPython 3.11.14 — `Lib/statistics.py`, `quantiles`
Primary implementation excerpt: `cpython.txt`, lines 5–31; https://github.com/python/cpython/blob/v3.11.14/Lib/statistics.py.

**Read:** the signature at line 5 and the docstring at lines 6–19. The signature fixes `n=4` and `method='exclusive'`; line 10 says: “Set *n* to 4 for quartiles (the default).” Line 15 says: “The cut points are linearly interpolated between data points.” Lines 17–19 say the alternative `inclusive` method treats the data as population data and the minimum/maximum as the 0th/100th percentiles.

**Annotation:** “Linear” is a property shared by both CPython branches, not the name of the default. The code makes the spacing rule explicit: `inclusive` uses `m = ld - 1` (line 24), while the non-inclusive path uses `m = ld + 1` (line 28). So CPython’s default is chosen by `method='exclusive'`, not by the word “linear.” The excerpt is partial (`[excerpt omitted]` at lines 22 and 27), so do not infer unshown error handling from it.

### 2. NumPy 2.4.4 — `numpy.percentile`, Parameters > method; References
Primary method documentation excerpt: `numpy.txt`, lines 5–26; https://numpy.org/doc/2.4/reference/generated/numpy.percentile.html.

**Read:** lines 7–19. NumPy says “[t]here are many different methods, some unique to NumPy,” that the options are “sorted by their R type as summarized in the H&F paper,” and that item 7 is `'linear' (default)`. Read lines 24–26 for the H&F citation.

**Annotation:** `'linear'` is one named member of a nine-method taxonomy, not a generic synonym for “interpolated.” NumPy’s own list places Hazen, Weibull, median-unbiased, and normal-unbiased in the same list, so “interpolated” alone does not identify a single rule. NumPy’s ordering makes `linear` item 7. CPython’s default is `exclusive`, with `m = ld + 1`; that is a different named method and the `ld + 1` spacing, not the `ld - 1` spacing of CPython’s `inclusive` branch. (In the standard H&F numbering these are the type-6 and type-7 families respectively; the packet does not reproduce H&F’s formula table, so the type labels are an interpretive aid, not a quoted passage.)

### 3. Hyndman & Fan (1996) — the journal record actually available
R. J. Hyndman and Y. Fan, “Sample quantiles in statistical packages,” *The American Statistician* 50(4), pp. 361–365, 1996, as cited at `numpy.txt` lines 24–26.

**What the accessible record supports:** the bibliographic identity of the paper, and NumPy’s attribution to it of the R-type summary. That is all. `digest.txt` itself states: “No full text of the cited journal article accompanies this packet.”

**What it does not support:** the digest’s claims that the paper “definitively endorsed every library’s default” and that “linear means the same thing everywhere.” No such passage is present. Even a genuine recommendation in the paper would not establish what CPython and NumPy currently implement; those defaults are fixed by the source and documentation records, not by the paper’s existence.

### 4. `digest.txt` — secondary commentary, not evidence
An unsigned, one-sentence tutorial digest. Read it as the claim under test, not as a primary record. Its two universal claims are unsupported by the packet and conflict with the differently named defaults in items 1–2.

## What follows

- “Linear” underdetermines the estimator: linear interpolation still needs an index/plotting-position rule. CPython’s two branches demonstrate this internally: `exclusive` uses `m = ld + 1`; `inclusive` uses `m = ld - 1`; both are covered by the same “linearly interpolated” sentence. The excerpt omits the interpolation body (lines 22, 27, and the remainder after line 31), so the packet does not by itself permit a numerical comparison; it does show that the branches are parameterized differently.
- The universal claim “every finite sample” is not supported by either record. There is no equivalence theorem in the packet; the defaults are explicitly different named methods. At most one can say both use linear interpolation; that is not identity.
- For a like-for-like comparison, CPython’s `inclusive` branch (`m = ld - 1`) is the natural counterpart of NumPy’s `linear` (item 7), since both use the `ld - 1` spacing; CPython’s default `exclusive` (`m = ld + 1`) belongs to the type-6 family that NumPy lists as `weibull` (item 6). Verify the formulas and endpoint behavior against the H&F table, which is not in the packet.

## What to specify in a comparison

- **Versions and functions:** CPython 3.11.14 `statistics.quantiles`; NumPy 2.4.4 `numpy.percentile`.
- **Grid:** CPython `n=4` (number of intervals) versus NumPy `q=[25, 50, 75]` (percent units); state the quartile definition.
- **Method:** CPython `method='exclusive'` (default) or `'inclusive'`; NumPy `method='linear'` (default) or one of the other eight. Record the H&F type if the comparison is method-level.
- **Conventions and edges:** sample versus population, endpoint/clamping rule, ties, sorted-input assumption, NaN/masked/weighted data, dtype/rounding, output order/shape, and minimum sample size or error behavior.
- **Claim scope:** if claiming equality “for every finite sample,” state the domain and prove it; otherwise report the exact sample(s) and the exact methods used.
