# Exact reference and trapezoid bias

Original educational note for this study; no external text is quoted.

An antiderivative of x² is x³/3. Evaluation at 1 and 0 gives the integral 1/3.

On a panel from a to a+h, set x=a+t. The straight line joining the endpoint values of x² has value a²+(2a+h)t. Subtract (a+t)² to get the pointwise difference t(h−t). Its integral from 0 to h is h³/6. The trapezoid area is the integral of this straight line, so it overestimates by h³/6 on each panel. There are n panels of width h=1/n.

The signed trapezoid error (estimate minus integral) is 1/(6n²).
