**Weight of Evidence (WOE):**

A method to encode the predictive strength of each feature bin relative to the target. For each bin, it measures the ratio of the share of good customers (non-events, repayers) to the share of bad customers (events, defaulters), then takes the natural log of that ratio.

WOE = ln(% distribution of non-events / % distribution of events)

In this dataset: event = defaulter (TARGET = 1), non-event = repayer (TARGET = 0).

A positive WOE means that bin contains proportionally more good customers than bad, it is a low-risk group. A negative WOE means the bin contains proportionally more bad customers than good, it is a high-risk group. Zero means the bin is neutral, no separation from the population average.

The reference point is 0, not 1. Positive means low risk, negative means high risk, magnitude tells you how strong the separation is.

For continuous features, the range is divided into bins (typically 10 using quantile binning) and WOE is calculated per bin. Bins must not be too small or too narrow, otherwise a bin may contain zero events or zero non-events, which makes the log undefined.

To handle this, an epsilon is added:

Adjusted WOE = ln(((non-events + ε) / total non-events) / ((events + ε) / total events))

Epsilon is typically a small value like 0.0001 or 0.5, both are used in practice. The purpose is identical: prevent log of zero.

**Why WOE outperforms one-hot encoding for logistic regression:**

One-hot encoding assigns a 0 or 1 to each category and forces the model to discover the relationship with the target from scratch during training. The numbers carry no pre-existing meaning.

WOE encodes the log-odds relationship with the target directly into the feature value before the model sees it. Logistic regression operates in log-odds units internally. So when you feed WOE-encoded features into logistic regression, you are adding log-odds to log-odds. Everything is in the same unit, the model's job becomes much simpler, coefficients are more stable, and the output is directly interpretable.


**Information Value (IV):**

IV measures the total predictive power of a feature across all its bins combined.

IV = sum of (% non-events - % events) x WOE

For a high-risk bin, % events is large and % non-events is small, so the difference is negative. WOE for that same bin is also negative (more bads than goods). Negative times negative gives a positive IV contribution. For a low-risk bin, % non-events is large, difference is positive, WOE is positive, positive times positive is again a positive contribution. Every bin adds to IV regardless of direction. IV only accumulates, it never cancels. That is why it measures total separation rather than net direction, and why a higher IV always means a more predictive feature.

| IV Value    | Interpretation                          |
|-------------|-----------------------------------------|
| Below 0.02  | No predictive power, drop               |
| 0.02 to 0.1 | Weak                                    |
| 0.1 to 0.3  | Medium                                  |
| Above 0.3   | Strong                                  |
| Above 0.5   | Suspiciously strong, check for leakage  |
