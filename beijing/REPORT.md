# Beijing benchmark: what the numbers mean

## Setup

The task is a **rolling one-hour-ahead forecast** of PM2.5 for 12 monitoring stations. Each forecast at time t can use PM2.5 measurements at t−1, t−2, t−3, t−6, t−12 and t−24, and — for the full model — weather and other pollutant readings from t−1. Calendar cycles are known in advance.

Each station is modeled separately, but its predictors include observations from the wider network. Models learn a change relative to the station's previous observed PM2.5 level. Training and evaluation respect chronological boundaries.

| Period | Use |
|---|---|
| March 2013–December 2014 | Fit candidates |
| January–December 2015 | Historical validation |
| March 2013–December 2015 | Refit fixed candidates |
| January–December 2016 | **Retrospective evaluation; previously inspected** |

## Main comparison

| Model | Scored station-hours | MAE | RMSE | Negative predictions |
|---|---:|---:|---:|---:|
| Persistence | 102,298 | 9.6632 | 18.6158 | 0 |
| LightGBM, PM2.5 only | 102,298 | 8.7970 | 16.7055 | 55 |
| LightGBM, PM2.5 + lagged environment | 102,298 | **8.6822** | **16.4617** | 102 |

The full model has **10.15% lower MAE than persistence** and **1.30% lower MAE than the PM2.5-only LightGBM** in this retrospective comparison. It improves over the PM2.5-only version in all 12 station-level MAEs in the archived table.

[Per-station MAE](results/station_mae.csv) · [Machine-readable summary](results/summary.csv) · [Run manifest](results/manifest.json)

## Why we cannot call this a final test

During earlier experimentation, model families, feature sets and hyperparameters were compared while looking at historical outcomes, including 2016. Therefore the evaluation is affected by potential model-selection bias. The published configuration is a fixed historical benchmark, **not** a prospective estimate of generalization.

Also, only hours with observed PM2.5 at t and t−1 are scored. Some target hours are excluded. Cross-station readings may arrive late in an operational system. Negative forecasts are left unchanged in primary scores rather than clipped after seeing results.

## Reproduction status

The corresponding local benchmark was rerun against the audited UCI inner ZIP and produced **102,298 aligned station-hour targets**, with recalculated MAEs matching the archived summary. That is evidence for the local archived benchmark, **not yet a certified clean-environment rerun of the exact GitHub commit**. Automated tests on GitHub check temporal feature integrity without redistributing the dataset.

A genuinely independent evaluation remains future work, with a [predeclared protocol](../docs/PROSPECTIVE_PROTOCOL.md).
