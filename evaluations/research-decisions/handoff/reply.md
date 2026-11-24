# Reply to the collaborator

You propose citing this as evidence that “one method always yields the smallest transferable file” ([request](../handoff-brief.md)). Please cite it instead as a comparison of four **payloads on one trace**. The distinction matters even for these exact readings: what does a receiver need in order to turn the 19 bytes back into the original counters?

After expanding the nine runs, I recovered all 256 readings using the two-place predictor. With prediction switched off, the same signed residuals still give 256 integers, but the third is 1 instead of −80. Knowing the sample count alone does not select the right interpretation. If both ends agree on the method in advance, no in-band method identifier is needed. For a self-describing transfer, the study supplies no container or protocol whose overhead we could count. Against the next-smallest measured payload (257 bytes), equal overhead preserves the 238-byte advantage; if the run-packed transfer needed 238 more overhead bytes than that alternative, they would tie. That is a break-even calculation, not a measured header size.

The small result also depends on repetition: four stretches of 62 equal residuals each contributed just one count and one code apiece. Checking the arithmetic on the same trace is not a second test of how often other counters behave this way. I would use the two paragraphs in [the returned manuscript](manuscript.md) in place of the [original passage](../../../examples/branch-decision/research/paper.md). The original already calls the measurements payload sizes; the revision makes the receiver assumption explicit and gives the citation a clear comparison set.

## How I checked the numbers

I used the supplied [integer trace](../../../examples/branch-decision/research/trace.txt) and the rules in the [method description](../../../examples/branch-decision/README.md); the zero start, signed-to-unsigned map, and ordering of the count and code are specified in lines 15–23 of [the archived source](../../../examples/branch-decision/run.py). My [independent calculation](count_lengths.py) reads only the trace. It counts one UTF-8 byte per code point below 128 and two up to 2047; no larger point occurred. For packing, it finds changes between successive codes, then counts the widths of the run lengths and codes separately. It neither imports nor runs the archived encoder.

From `evaluations/research-decisions/handoff/`, I ran:

```sh
python3 count_lengths.py ../../../examples/branch-decision/research/trace.txt > counts.txt
```

Exit status: 0. The [captured output](counts.txt) gives the width counts, run pairs and decoding check. The four totals agree exactly with rows `raw`, `adjacent`, `paired` and `runs` of [the supplied table](../../../examples/branch-decision/research/bytes.csv). The trace digest in the output matches the [original run record](../../../examples/branch-decision/research/run.json). The supplied manuscript remains unchanged (SHA-256 `dd63cadd98ac0cac20d2ff94466f8db0d158eac2f1c377cd4c734ceb6b5d682d`).
