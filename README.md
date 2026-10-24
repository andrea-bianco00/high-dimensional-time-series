# From 516 sensors to better air-quality forecasts

### High-dimensional time series · Statistical learning · PM2.5 forecasting

**Andrea Bianco** · Statistics & Data Science  
Python · R · Time-series forecasting · Regularization · LightGBM · Reproducible research

> **The question:** Can information from a network of air-quality sensors help us understand — and predict — how pollution changes over time?

Air pollution is not a single time series. Each monitoring station records its own measurements, but nearby stations are affected by shared weather, transport and local emissions. The challenge is to learn from the network without being overwhelmed by hundreds of correlated signals.

This repository brings together **two connected but distinct pieces of work**: an original university study of 516 Taiwanese sensor series, and a later, independently developed forecasting benchmark using 12 Beijing stations.

## The project at a glance

| | Taiwan AirBox — university study | Beijing — subsequent extension |
|---|---|---|
| **Question** | How do we model a time series when the number of sensors is large relative to the time dimension? | Can lagged network and weather information improve one-hour-ahead PM2.5 forecasts? |
| **Data** | 516 sensor series × 744 hourly observations, March 2017 | 12 monitoring stations, hourly observations from the UCI Beijing dataset |
| **Approach** | High-dimensional time-series methods, including regularized VAR analysis in R | Persistence baseline, regularized regression and tree-based forecasting experiments |
| **Authorship** | **Andrea Bianco, Emidio Grillo, Luca Nudo** | Subsequent Python extension by Andrea Bianco |
| **Status** | Original group work documented; original BigVAR analysis **not independently rerun here** | Code and retrospective results available; no untouched external test |

**Important:** Beijing is *not* a validation dataset for the Taiwan model. They are different networks, with different dimensionalities and forecasting setups.

## What did the Beijing experiment find?

A simple benchmark is **persistence**: predict that the next hour will look exactly like the previous hour. It is surprisingly difficult to beat, especially for short forecasting horizons.

In the **2016 retrospective evaluation**, using the same 102,298 valid station-hour observations for each model:

| Model | MAE ↓ | RMSE ↓ |
|---|---:|---:|
| Persistence — use the previous hour | 9.663 | 18.616 |
| LightGBM — lagged PM2.5 only | 8.797 | 16.706 |
| **LightGBM — PM2.5 + lagged weather and pollutants** | **8.682** | **16.462** |

**10.15% lower MAE than persistence** for the environment-aware LightGBM in this retrospective benchmark. The full model also improves MAE over the PM2.5-only version at all 12 stations in the archived comparison.

**The essential caveat:** these 2016 observations were repeatedly consulted while exploring models. This is **development performance, not an untouched independent test**. It would be misleading to present this improvement as guaranteed out-of-sample performance or as an improvement over the original Taiwan project.

### What made this interesting?

- **Cross-station signals:** a forecast for one station can use historical observations from the wider network.
- **Weather matters:** lagged temperature, pressure, humidity-related variables, wind and other pollutants provided additional information in the retrospective comparison.
- **The baseline matters:** every model is measured against the same simple, interpretable reference.
- **Research discipline matters:** missing observations, temporal leakage, negative forecasts, reporting latency and the limits of model selection are explicitly documented.

## How the forecast works

At hour **t**, the model predicts PM2.5 using only measurements timestamped at **t−1 or earlier**, plus known calendar features. It predicts the *change* from the last observed PM2.5 value and adds that change back to the observed level.

- PM2.5 lags: 1, 2, 3, 6, 12 and 24 hours, across 12 stations.
- Additional lag-1 weather and pollutant measurements in the full model.
- Train: 2013–2014; validation: 2015; refit: 2013–2015; retrospective evaluation: 2016.
- Hours missing the target or its previous observed value are excluded and counted.
- Predictions below zero are **not silently clipped** in the reported scores.

A real-world deployment would additionally need to verify that readings from every station are actually available at prediction time.

## Explore the repository

| Where to go | What you will find |
|---|---|
| [Beijing benchmark](beijing/README.md) | Method, how to run it, archived results and verification scripts |
| [Taiwan study](taiwan/README.md) | Original university research context and a clearly separated later exploratory reanalysis |
| [Research integrity](docs/RESEARCH_INTEGRITY.md) | What was tested, what was not, and why the distinction matters |
| [Data and permissions](docs/DATA_AND_LICENSES.md) | Dataset provenance and publication boundaries |
| [Prospective evaluation plan](docs/PROSPECTIVE_PROTOCOL.md) | How a genuinely new test should be conducted |
| [Portfolio summary](portfolio/PROJECT_EN.md) | A shorter, recruiter-friendly description |

## Reproduce the Beijing benchmark

1. Download the [UCI Beijing Multi-Site Air Quality dataset](https://archive.ics.uci.edu/dataset/501/beijingmultisiteairqualitydata).
2. Extract its **inner ZIP containing the 12 station CSV files**. The script checks its SHA-256 checksum.
3. Install Python dependencies and run:

```bash
python -m pip install -r beijing/requirements.txt
python beijing/src/benchmark.py --data /path/to/beijing_official_inner.zip --output /tmp/beijing-results
python beijing/verify.py --results /tmp/beijing-results
```

The benchmark outputs timestamp-level predictions, per-station results, validation scores and aggregate metrics. Archived summary tables are under [`beijing/results/`](beijing/results/). The exact published code still needs a separately documented clean-environment run; **a stored metric alone is not proof of reproducibility**.

## What I would do next

The most valuable next experiment is **not another round of hyperparameter tuning on 2016**. It is a genuinely independent evaluation using new, eligible measurements, following a protocol fixed *before* looking at their outcomes. Until such data exist, the correct conclusion is that the models look promising in retrospective analysis, with generalization still unproven.

## Credits and data rights

The original university project was completed by **Andrea Bianco, Emidio Grillo and Luca Nudo (2026)**. The later Beijing forecasting extension is separate from that submission. Beijing data are from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/501/beijingmultisiteairqualitydata), released under **CC BY 4.0**; please follow its attribution requirements.

Raw Taiwan observations, group slides, third-party archives and original shared R scripts are **not redistributed** because their publication rights have not been confirmed. No software license is assigned to this repository at present.

---

*Built around a simple principle: a model is only as credible as the way it is evaluated.*
