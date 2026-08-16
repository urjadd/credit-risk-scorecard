# Math Intuition: Logistic Regression and Scorecard Metrics

## What is the sigmoid function doing?
Logistic regression does not predict 0 or 1 directly. It predicts a number on a continuous scale from negative infinity to positive infinity (the log-odds). The sigmoid function squashes that number into a value between 0 and 1, which we interpret as a probability. A log-odds of 0 becomes probability 0.5. Large positive log-odds become probabilities close to 1. Large negative log-odds become probabilities close to 0. Without the sigmoid, the model output would be unbounded and could not be read as a probability.

## What are log-odds?
Odds are the ratio of something happening vs not happening. If 8 out of 100 applicants default, the odds of default are 8/92 = 0.087. Log-odds is the natural log of that: ln(0.087) = -2.44. Logistic regression works in log-odds space because it makes the math linear. The model learns a straight line in log-odds space, then the sigmoid converts it back to probability space. This is why logistic regression is called a linear model even though its output is a curve.

## Why does L2 regularization help?
When two features are highly correlated (say two similar external scores), the model cannot decide how to split credit between them. One gets a huge positive coefficient, the other a huge negative one. Both are unstable. L2 regularization adds a penalty for large coefficients. It forces the model to spread the weight more evenly across correlated features instead of going extreme on one. The C parameter controls how strong this penalty is. Smaller C means heavier penalty, more stable but potentially underfitting. C=1.0 is a balanced default.

## What does the Gini coefficient measure geometrically?
The ROC curve plots true positive rate against false positive rate. A perfect model hugs the top-left corner. A random model follows the diagonal. The area between the ROC curve and the diagonal is the Gini coefficient divided by 2. So Gini = 2 * AUC - 1. A Gini of 0 means the model is no better than random. A Gini of 1 means perfect separation. Our Gini of 0.48 means the model captures about 48% of the maximum possible separation between defaulters and non-defaulters. In credit risk, anything above 0.40 is considered acceptable for production use.

## What does the KS statistic measure?
KS measures the maximum distance between two cumulative distribution curves: one for defaulters, one for non-defaulters. Imagine plotting both curves on the same chart. At some score threshold, the gap between them is widest. That gap is the KS statistic. Our KS of 0.355 means at the optimal threshold, 35.5% more non-defaulters have been captured than defaulters (or vice versa). It tells you the single best point at which the model separates the two groups.
