# High-Dimensional Time Series Analysis

Research and reproducible forecasting benchmarks involving high-dimensional air-quality time series.

## Project structure

This repository distinguishes two related but separate projects:

1. **Taiwan AirBox (original university group project)** — high-dimensional PM2.5 time-series analysis using approximately 516 sensors. Original university work by Andrea Bianco, Emidio Grillo and Luca Nudo. The original third-party/group datasets and presentation are not redistributed here.
2. **Beijing multi-site PM2.5 forecasting (subsequent extension)** — independent methodological extension using the UCI Beijing Multi-Site Air-Quality dataset (12 stations), including lagged meteorological and pollutant variables and comparative statistical/machine-learning models.

## Retrospective Beijing results

For the previously explored 2016 evaluation period, the reported one-hour-ahead MAE is **9.6632** for persistence, **8.7970** for PM2.5-only LightGBM, and **8.6822** for LightGBM with environmental covariates (102,298 scored station-hours). The latter represents an approximately **10.15% reduction in MAE relative to persistence**, **not** relative to the original Taiwan university project.

**Important limitations:** The 2016 period was consulted repeatedly during model development, so these numbers are retrospective and **not an untouched independent test**. Prospective external validation and clean-environment reproducibility remain open. These datasets differ in geography, dimensionality, and prediction setup; results should not be compared as if they were the same benchmark.

## Data and licensing

- Beijing dataset: [UCI Beijing Multi-Site Air-Quality](https://archive.ics.uci.edu/dataset/501/beijingmultisiteairqualitydata), CC BY 4.0; cite the original dataset creators and source when using it.
- Taiwan data: not redistributed pending confirmation of provenance and redistribution permissions.
- No license is currently granted for this repository's original code. Licensing will be reviewed separately.

## Publication status

Initial repository setup. Source code, reproducibility scripts and detailed reports are being reviewed for publication; their absence from this initial commit should not be mistaken for a complete reproducibility package.
