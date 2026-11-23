# Annotated reading list: does “linear” prove identical default quartiles?

*Scope: prepared only from the four supplied texts in `/mnt`; no external sources, code execution, or simulation.*

**Short answer: no.** In the supplied packet, “linear” is not a shared method identifier. In CPython it is prose describing interpolation; in NumPy it is one named entry in a nine-method taxonomy. No supplied record defines the two defaults on a common scale or states that they coincide. A shared English word cannot establish the universal claim that the two functions return identical default quartiles for *every* finite sample.

## Records

### 1. CPython 3.11.14, `Lib/statistics.py`, `quantiles`
**Record:** primary implementation excerpt (partial), `cpython.txt`, citing `https://github.com/python/cpython/blob/v3.11.14/Lib/statistics.py`.

**Relevant passages:** the signature is `def quantiles(data, *, n=4, method='exclusive'):`; the docstring says, “Set *n* to 4 for quartiles (the default)” and “The cut points are linearly interpolated between data points.” It also says that with `method='inclusive'`, “*data* is treated as population data.” The visible branch structure sets `m = ld - 1` under `if method == 'inclusive':`, then separately sets `m = ld + 1` and computes `j = i * m // n  # rescale i to m/n`.

**Annotation:** this is the primary record for CPython’s behaviour, but it is explicitly truncated: validation and parts of both loops are omitted (`[excerpt omitted]` at lines 22 and 27). It establishes that the default is quartiles (`n=4`) using `method='exclusive'`, that CPython offers two endpoint conventions, and that the exclusive default uses a different index scale (`ld + 1`) from the inclusive branch (`ld - 1`). It does **not** use `linear` as a method name, does not cite Hyndman–Fan, and does not give the interpolation weights in the supplied text. It therefore cannot by itself establish agreement with NumPy’s `linear`.

### 2. NumPy 2.4.4, `numpy.percentile`, Parameters > `method`, and References
**Record:** primary method documentation excerpt, `numpy.txt`, citing `https://numpy.org/doc/2.4/reference/generated/numpy.percentile.html`.

**Relevant passages:** “This parameter specifies the method to use for estimating the percentile. There are many different methods, some unique to NumPy.” The options are listed as nine entries, “sorted by their R type as summarized in the H&F paper [1]”; entry 7 is `'linear'  (default)`. Reference [1] is R. J. Hyndman and Y. Fan, “Sample quantiles in statistical packages,” *The American Statistician*, 50(4), pp. 361–365, 1996.

**Annotation:** this establishes that NumPy’s default token is `linear`, that it is one of several distinct methods, and that NumPy attributes the ordering to Hyndman–Fan. The documentation excerpt does not state that NumPy’s `linear` is the same rule as CPython’s `exclusive`, nor does it supply the formula for entry 7. The warning that some methods are “unique to NumPy” makes a blanket “linear means the same thing everywhere” claim especially unsafe.

### 3. Hyndman & Fan (1996), “Sample quantiles in statistical packages”
**Record:** the journal article itself is **not supplied**. The only accessible record is its bibliographic citation, as reference [1] in the NumPy documentation above.

**Annotation:** this citation supports only limited facts: that such a paper exists with the stated title, authors, journal, volume, issue and pages; and that NumPy reports its method ordering as a summary of that paper. No abstract, definitions, recommendation, or quotation from the article is present. It therefore **cannot** support the digest’s claim that the paper “definitively endorsed every library’s default.” To assess that sentence one would need the article itself and the relevant passage, not its citation.

### 4. `digest.txt` — unsigned tutorial digest
**Record:** secondary commentary, not a primary source; no author, provenance, or full text of the cited article.

**Relevant passage:** “The Hyndman–Fan paper definitively endorsed every library's default and linear means the same thing everywhere.”

**Annotation:** this is the claim under test, not evidence for it. It conflicts with the identifiable primary records, which show that CPython’s default is named `exclusive` and that NumPy distinguishes nine methods. With no attribution or full text, the digest should not be cited as support for algorithmic identity.

## What the accessible journal record actually supports

The accessible record for the journal paper supports **bibliographic identification only**, plus NumPy’s own statement that its ordered options are “as summarized in the H&F paper [1].” It does not support any statement about what the paper “definitively endorsed,” nor any claim that libraries’ defaults are identical. The phrase “linear means the same thing everywhere” is an unsourced secondary assertion.

## What the primary records establish about the comparison

- CPython’s default is `n=4`, `method='exclusive'`; NumPy’s default is `method='linear'`. The defaults are not presented under the same name or in the same taxonomy.
- CPython’s visible exclusive branch uses `m = ld + 1`; its inclusive branch uses `m = ld - 1`. The method switch changes the index scale, so the two conventions are not interchangeable by label alone.
- The CPython excerpt is incomplete and the NumPy excerpt gives a name list rather than a formula. The packet therefore does not contain enough to prove an exact crosswalk, and certainly not enough to prove equality for every finite sample.
- Equality for all finite samples is a universal mathematical claim. It would require a demonstrated common definition, including endpoint and indexing conventions, not an occurrence of the adjective “linear.”

## What a researcher should specify to compare results

1. **Exact records and versions:** CPython 3.11.14 `statistics.quantiles`; NumPy 2.4.4 `numpy.percentile`.
2. **Exact call:** `statistics.quantiles(data, n=4, method=...)` with `'exclusive'` or `'inclusive'`; `numpy.percentile(a, q=[25, 50, 75], method=...)` with the chosen method token.
3. **Quantile definition:** the probability convention, the plotting-position/index formula, whether indexing is zero- or one-based, the interpolation rule, and the treatment of the minimum and maximum (sample/exclusive versus population/inclusive).
4. **Taxonomy crosswalk, if claimed:** the Hyndman–Fan type number and the page or passage that defines it. Do not write “both use linear” as a substitute for a mapping.
5. **Data conditions:** sorted order, sample size, ties, dtype, missing values, axis, and the minimum sample size accepted by each function.
6. **Output contract:** the three default quartile cut points, their order, container type, and the numerical tolerance used for comparison.
7. **Evidence for any equivalence claim:** a worked definition-level comparison or a cited source passage. The supplied packet supports neither an identity claim nor its universal quantifier.

**Bottom line for the reading list:** cite CPython’s `quantiles` excerpt for its `exclusive` default and partial interpolation description; cite NumPy’s `numpy.percentile` page for its nine-method list and default `linear`; cite Hyndman–Fan only as bibliographic metadata unless the full article is obtained; and treat `digest.txt` as an unverified secondary claim.
