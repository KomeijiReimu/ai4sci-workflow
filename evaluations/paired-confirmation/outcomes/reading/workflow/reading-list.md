# Annotated reading list — “linear” and default quartiles in CPython and NumPy

**Question.** Does seeing the word “linear” establish that `statistics.quantiles` (CPython 3.11.14) and `numpy.percentile` (NumPy 2.4.4) return identical default quartiles for every finite sample?

**Answer.** No. The two defaults are different named rules: CPython defaults to `method='exclusive'`, while NumPy defaults to a method labelled `'linear'`. On the standard Hyndman–Fan mapping—whose CPython side and cross-library equivalence are not printed in the supplied excerpts and should be checked in the full records—CPython’s default is type 6 while NumPy’s default is type 7; CPython’s non-default `inclusive` method is the one that corresponds to NumPy’s default. The packet contains only a citation to the Hyndman–Fan article, not the article itself, so it cannot support the digest’s claim of universal endorsement or of identical defaults.

## Annotated records

### 1. CPython 3.11.14 — `Lib/statistics.py`, `quantiles`

**Record:** `/mnt/cpython.txt`, lines 1–31 (primary implementation excerpt; source URL at line 3: `https://github.com/python/cpython/blob/v3.11.14/Lib/statistics.py`).

**Relevant passages.**

> `def quantiles(data, *, n=4, method='exclusive'):` (line 5)

> “Set *n* to 4 for quartiles (the default).” (line 10)

> “The cut points are linearly interpolated between data points.” (line 15)

> “If *method* is set to *inclusive*, *data* is treated as population data. The minimum value is treated as the 0th percentile and the maximum value is treated as the 100th percentile.” (lines 17–19)

**Annotation.** The default is a named endpoint rule, `exclusive`, not a method called `linear`. “Linearly interpolated” describes the interpolation step, not the knot positions or the endpoint convention; `inclusive` is explicitly a different convention. The excerpt is truncated at lines 22 and 27 and stops at line 31 before the interpolation expression, so it does not by itself give the formula, a Hyndman–Fan type number, or a bridge to NumPy.

### 2. NumPy 2.4.4 — `numpy.percentile`, method parameter

**Record:** `/mnt/numpy.txt`, lines 1–26 (primary documentation excerpt; source URL at line 3: `https://numpy.org/doc/2.4/reference/generated/numpy.percentile.html`).

**Relevant passages.**

> “There are many different methods, some unique to NumPy. See the notes for explanation. The options sorted by their R type as summarized in the H&F paper [1]_ are:” (lines 7–9)

> `7. 'linear'  (default)` (line 17), in a list of nine method names (lines 11–19).

**Annotation.** NumPy’s `'linear'` is a label for one of nine methods, not a synonym for “any method that interpolates linearly.” The excerpt gives the names and the default but not the formulas, and it does not state that `'linear'` equals CPython’s `exclusive`. The numbered order is consistent with one method per R type, but the excerpt does not print the type definitions.

### 3. Hyndman & Fan (1996) — citation-only record

**Record:** the reference in `/mnt/numpy.txt`, lines 22–26:

> R. J. Hyndman and Y. Fan, “Sample quantiles in statistical packages,” *The American Statistician*, 50(4), pp. 361-365, 1996.

**What this accessible record supports.** It identifies the article bibliographically and shows that NumPy says its method options are “sorted by their R type as summarized in the H&F paper.” That is all the packet contains. It does not contain the article’s text, definitions, recommendations, or any statement about CPython or NumPy defaults. In particular, it cannot support the digest’s claims that the paper “definitively endorsed every library's default” or that “linear means the same thing everywhere.” A 1996 article also cannot have endorsed the defaults of CPython 3.11.14 or NumPy 2.4.4 as such. To use the article, obtain the full text and cite the section that defines the types and any recommendation.

### 4. Unsigned tutorial digest — secondary commentary

**Record:** `/mnt/digest.txt`, line 1.

> “The Hyndman–Fan paper definitively endorsed every library's default and linear means the same thing everywhere.”

The same record notes: “No full text of the cited journal article accompanies this packet.”

**Annotation.** This is an unsigned, unlocated assertion, not a primary record. It is the claim to test, not evidence for it. No author, date, URL, or page number is supplied, and its own note concedes that the article is absent.

## Why “linear” does not settle the question

- **Different objects.** In NumPy, `'linear'` is a method-name string among nine. In CPython, “linearly” is an adverb describing interpolation. Shared vocabulary is not a shared rule.
- **Different defaults.** CPython defaults to `exclusive`; NumPy defaults to `linear`. CPython also exposes `inclusive` as a distinct endpoint convention (minimum as 0th percentile, maximum as 100th). Endpoint convention is precisely the kind of choice that changes a quartile.
- **The universal claim is too strong.** “Identical for every finite sample” would require the same position formula, interpolation arithmetic, tie handling, and floating-point evaluation. The excerpts establish none of these. Even if two rules agreed on some samples (for example, symmetric or repeated values), that would not make them identical for all finite samples.
- **The mapping needs a source.** The usual formal mapping—CPython `exclusive` ↔ H&F type 6, NumPy `linear` ↔ H&F type 7, and CPython `inclusive` ↔ the type-7 rule—is not stated in full in the supplied excerpts. It is the mapping to verify in the full CPython source and the full Hyndman–Fan article before asserting equivalence. If the full records confirm it, the defaults still differ: type 6 and type 7 use different positions, so the default quartiles are not identical in general.

A definition-level check (arithmetic, not a library run): under the type-6 rule for `x = [0, 1, 2, 3]`, Q1 is 0.25; under the type-7 rule, Q1 is 0.75. Confirm both formulas in the full sources before quoting those numbers.

## What a researcher should specify to compare results

1. **Software:** CPython version and NumPy version (here 3.11.14 and 2.4.4), plus build or floating-point details if exactness matters.
2. **Call:** `statistics.quantiles(data, n=4, method=...)`; `numpy.percentile(data, [25, 50, 75], method=...)`. NumPy percentile has no default `q`, so state the probabilities explicitly.
3. **Method and formal rule:** the method string, the H&F type number, and the position formula (for example, `h = (N+1)p` versus `h = 1 + (N−1)p`), including endpoint treatment (`exclusive` versus `inclusive`) and whether the sample is framed as a sample or a population. If matching CPython’s default is the goal, state and verify the candidate mapping to NumPy’s `'weibull'` entry (position 6 in the supplied list); the excerpt does not print that formula.
4. **Sample:** N, sorted values, ties and duplicates, NaN/missing policy, dtype, and precision.
5. **Output convention:** list versus array, order, rounding, and any tolerance used for comparison.
6. **Mapping justification:** cite the primary-source passage that equates the two method names; do not infer it from the word “linear.”

## Bottom line

Seeing “linear” does not establish identical default quartiles. It establishes at most that linear interpolation is involved. CPython’s default is `exclusive`; NumPy’s default is the `'linear'` member of a nine-method, Hyndman–Fan-referenced taxonomy. The packet’s only journal record is a citation, which supports the article’s existence and its role as NumPy’s taxonomy source—not a universal endorsement or cross-library identity. To compare results, name the versions, calls, type or formula, endpoint rule, sample properties, and output conventions, and verify the mapping in the full primary records.
