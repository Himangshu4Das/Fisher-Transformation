# Fisher-Transformation
The following python code is an implementation of Fisher's transformation on pandas dataframe and can be used as a technical indicator ( momentum).
It returns two columns:
  1. Fisher transform (default period = 9)
  2. Signal           (default shift = 1)
 
You are free to use it as a package.
Call the fisher method from fisher_transform package.

The Fisher Z-Transformation is a way to transform the sampling distribution of Pearson’s r (i.e. the correlation coefficient) so that it becomes normally distributed. The “z” in Fisher Z stands for a z-score.
The formula to transform r to a z-score is:
z’ = .5[ln(1+r) – ln(1-r)]

In statistics, the Fisher transformation (or Fisher z-transformation) of a Pearson correlation coefficient is its inverse hyperbolic tangent (artanh).

Note: The example code uses yfinance to get stock data as a sample to demonstrate fisher's transformation.
