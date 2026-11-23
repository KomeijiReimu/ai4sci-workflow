# Reading list: does “linear” prove equal default quartiles?

**Short answer: no.** The supplied records show two different defaults — NumPy's
`method='linear'` and CPython's `method='exclusive'` — and none of the records
defines “linear” precisely enough to identify a single estimator for every finite
sample. The claim in `digest.txt` is unsigned commentary, not a primary record,
and is not supported by anything in the packet.

## Annotated list

### 1. NumPy 2.4.4, `numpy.percentile`, “method” parameter and References
`numpy.txt` (lines 2–26); record: <https://numpy.org/doc/2.4/reference/generated/numpy.percentile.html>

Relevant passages:

> “This parameter specifies the method to use for estimating the percentile.
> There are many different methods, some unique to NumPy.”

> “The options sorted by their R type as summarized in the H&F paper [1]_ are:”
> … `7. 'linear'  (default)`

What it establishes: NumPy's default is the string `'linear'`, and that string is
item 7 in a list ordered by “R type” as attributed to Hyndman–Fan. It also
establishes that NumPy itself says there are *many* methods, some unique to
NumPy. What it does **not** establish in the accessible excerpt: the formula or
plotting position behind `'linear'` (the notes are marked `[excerpt omitted]`),
or any equivalence with another library. So the record supports “NumPy's default
is type 7 in that ordering,” not “linear is a universal method.”

### 2. CPython 3.11.14, `Lib/statistics.py`, `quantiles`
`cpython.txt` (lines 2–31); record: <https://github.com/python/cpython/blob/v3.11.14/Lib/statistics.py>

Relevant passages:

> `def quantiles(data, *, n=4, method='exclusive'):`

> “The cut points are linearly interpolated between data points.”

> “If *method* is set to *inclusive*, *data* is treated as population data.
> The minimum value is treated as the 0th percentile and the maximum value is
> treated as the 100th percentile.”

What it establishes: the default is `'exclusive'`, not `'inclusive'`; “linearly
interpolated” is a description of how cut points are formed, not the name of a
Hyndman–Fan/R type. The record is truncated (`[excerpt omitted]`) before the
branch arithmetic, so it does not show the exclusive formula, argument-count
guards, or boundary behaviour at small sample sizes. On the endpoint wording,
CPython's population-style `'inclusive'` (min = 0th, max = 100th percentile) is
the branch whose description matches an endpoint-anchored type-7 rule; the
default `'exclusive'` is a different convention. That mapping is an inference
from the wording, not something the packet's formulas prove.

### 3. Hyndman & Fan (1996) — the journal record as it appears in the packet
`numpy.txt` (lines 24–26): R. J. Hyndman and Y. Fan, “Sample quantiles in
statistical packages,” *The American Statistician*, 50(4), pp. 361–365, 1996.

This is the only accessible record for the journal paper: a bibliographic
reference entry inside NumPy's documentation, not the article. It supports:
the paper's existence, its title/venue/volume/pages/year, and NumPy's
attribution to it of the R-type ordering of percentile methods. It does **not**
support: that the paper endorsed any library's default, that “linear” means the
same thing in every package, or any specific estimator formula. The packet
contains no article text, table, section, or quotation, so the digest's
“definitively endorsed” claim cannot be checked here. A 1996 paper also
predates the NumPy 2.4.4 and CPython 3.11.14 records above, so a claim about
“every library's default” would need explicit evidence that the packet lacks.

### 4. `digest.txt` — unsigned secondary commentary (not a primary record)
`digest.txt` (line 1): “The Hyndman–Fan paper definitively endorsed every
library's default and linear means the same thing everywhere.”

Annotate with caution: no author, no page or section, no quotation, and no full
text of the cited article. It conflicts with the two primary records, which show
different default method names (`'linear'` vs `'exclusive'`). Reading it as
evidence for the equivalence would be circular: it asserts the conclusion the
packet is being asked to test.

## Why the word “linear” does not settle the question

1. **The defaults are different names.** NumPy defaults to `'linear'`; CPython
   defaults to `'exclusive'`. Identical wording about interpolation does not make
   two differently named defaults identical, and nothing in the packet says
   CPython's `'exclusive'` is type 7.
2. **“Linear” is not a unique identifier.** NumPy's own list contains nine
   methods (items 1–9) and warns that some are unique to NumPy. The word
   “linear” names one of them but does not tell a reader which plotting position
   the others use, or which one CPython implements. CPython's phrase “linearly
   interpolated” is a property of its interpolation, not a type label.
3. **The H&F record is metadata only.** The article's formulas are not in the
   packet, so the type number → estimator mapping cannot be verified from the
   supplied evidence. A claim of identity “for every finite sample” would need
   that mapping, not just the citation.
4. **“Every finite sample” includes boundary sizes.** The accessible CPython
   excerpt omits the checks and the exclusive-branch arithmetic, so it cannot
   certify behaviour for N = 0, 1, 2, or constant/duplicate samples. Universal
   identity is therefore not established even between the two “linear” branches.

The defensible comparison suggested by the records is **NumPy
`method='linear'` (type 7) against CPython `method='inclusive'`**, not against
CPython's default `'exclusive'`; but that pairing must be verified against the
H&F table, which is not in this packet.

## What a researcher should specify to compare results

- **Versions and records:** NumPy 2.4.4 and CPython 3.11.14 (or the exact builds
  used), with the documentation/source URL for each.
- **Function and full call:** e.g. `numpy.percentile(x, [25, 50, 75], method=...)`
  and `statistics.quantiles(x, n=4, method=...)`.
- **Method explicitly, never by adjective:** NumPy `method='linear'`; CPython
  `method='inclusive'` if the intended convention is endpoint-anchored type 7.
  State that CPython's default is `'exclusive'` and is a different convention.
- **Estimator definition:** the H&F type number *plus* the plotting-position
  formula as printed in the H&F table itself (the table is not in this packet),
  since library names are not portable.
- **Sample/population framing:** whether the minimum and maximum are defined as
  the 0th and 100th percentiles.
- **Sample sizes and edge cases:** N = 0, 1, 2, 3, and N below any minimum
  required by the exclusive method; constant and duplicate-valued samples.
- **Numeric semantics:** integer vs floating-point input, exact-rational vs
  binary-float interpolation, output dtype, and the equality criterion
  (bit-identical vs tolerance).
- **Input handling:** whether data must be sorted, whether the call sorts a
  copy, and how NaN/inf are treated (the question restricts to finite samples,
  but the comparison should say so).
- **Reporting:** publish the library method string, the H&F type number, and the
  formula together, so a reader can reproduce the comparison without relying on
  the word “linear.”
