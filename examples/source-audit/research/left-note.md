# Why left endpoints are a negative control

Original educational note for this study; no external text is quoted.

On a panel [a,b] of width h, the trapezoid contribution minus the left-rectangle contribution is h(f(b)−f(a))/2. On the uniform mesh these differences telescope: all interior endpoint values cancel. Since f(1)−f(0)=1, the composite trapezoid estimate exceeds the left sum by h/2. Combining this identity with the trapezoid bias in [the companion note](trapezoid-note.md), the left sum equals 1/3 + 1/(6n²) − 1/(2n).

The absolute left-sum error is 1/(2n) − 1/(6n²), whose leading term scales as 1/n.

The finite-mesh error need not halve exactly. As n grows, E(n)/E(2n) tends to two, so its base-two logarithm tends to one. This distinguishes a convergent method from one with second-order convergence.
