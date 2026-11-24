# Encoding the interleaved counters

On one synthetic trace of 256 interleaved counter readings, encoding the signed values directly took 396 payload bytes. Predicting each value from its immediate predecessor increased the payload to 512 bytes. Predicting from two positions back, within the same counter stream, took 257 bytes. The resulting residuals formed just nine runs. Storing a count and a code for each run took 19 bytes: nine for the counts and ten for the codes.

The 19-byte payload was the smallest of the four tested on this trace. Its receiver must know to expand the runs and add each residual to the value two positions back, using zero when no such value exists. These counts exclude headers. Both comparisons used the same readings; they establish neither a complete file size for a receiver without that prior agreement nor a ranking on other traces.
