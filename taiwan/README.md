# Taiwan AirBox: where this project started

**University project, February 2026 — Andrea Bianco, Emidio Grillo and Luca Nudo**

Our original question was about *dimensionality*: what happens when we want to model hundreds of correlated time series, but have relatively little history for each one?

The available March 2017 Taiwan AirBox matrix contained **744 hourly rows and 516 anonymous PM2.5 sensor series**. The original group project explored high-dimensional time-series modeling, including regularized vector autoregressive methods in R.

### Why this is a difficult problem

In a conventional VAR, the number of coefficients grows quickly with the number of series and lags. With hundreds of sensors and only 744 observations, naive unrestricted estimation becomes impractical. Regularization offers a way to control complexity and encourage sparse dependencies.

### What is — and isn't — published here

The original R BigVAR implementation, slides and raw matrix are **not redistributed**: the group authorship and underlying dataset rights need to be respected. The original BigVAR experiment has **not been rerun independently** in this repository.

A later exploratory Python analysis was conducted on the same source matrix, with 20 selected target columns and a 50-predictor subset chosen by column order. It is **not** the original group implementation, a full 516-sensor forecasting result, or an untouched test.

The separate Beijing benchmark in [../beijing/](../beijing/) is a methodological extension, **not** a claim that the original Taiwan model was tested on Beijing.

### Data limitations

The supplied matrix does not establish the original device identifiers or trustworthy per-reading timestamps. Some associated geographic information is inconsistent. These constraints matter when interpreting network structure and make us cautious about spatial claims.

For the broader project story, start with the [main README](../README.md). For integrity and attribution, see [research integrity](../docs/RESEARCH_INTEGRITY.md).
