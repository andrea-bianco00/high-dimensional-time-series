# Prospective evaluation plan — not a test result

**Status:** Predeclared plan drafted after extensive historical exploration. No new independent data have been evaluated under this protocol.

## The question

Will the retrospective advantage of lagged environmental information persist on *new, genuinely unseen* measurements?

## Eligibility

All available Beijing 2013–2017 observations have already influenced exploratory decisions. **None of them may be called an untouched test.** A future evaluation requires new observations or a separately identified external network, whose provenance, units, station coverage, timestamps and availability are checked *before* examining target outcomes.

A new city is a **transfer** evaluation, not necessarily an in-distribution Beijing replication.

## Forecast definition

Predict PM2.5 at hour t from measurements timestamped no later than t−1. Report forecast coverage, including when the last observed PM2.5 value is missing. Operational use additionally requires proof that other stations' t−1 readings have actually arrived by the prediction deadline.

## Frozen candidates

1. **LightGBM:** 70 estimators, 31 leaves, learning rate 0.045, minimum child samples 80, L2 penalty 10, seed 2026. Features: network PM2.5 lags 1, 2, 3, 6, 12, 24; ten environmental lag-1 variables; calendar cycles.
2. **XGBoost:** 100 trees, maximum depth 5, learning rate 0.05, subsample 0.9, column subsample 0.9, L2 penalty 10, seed 2026, same features.
3. **Persistence:** the previous observed PM2.5 level.

These are **predeclared finalists, not globally optimized models**. Their historical selection was exploratory.

## Evaluation and reporting

- **Primary:** pooled station-hour MAE.
- **Secondary:** pooled RMSE, MAE by station, negative prediction fraction, forecast coverage and predefined ground-truth PM2.5 bins (0–25, 25–75, 75–150, >150).
- Score identical station-hour targets for all candidates; publish excluded-hour counts and reasons.
- Keep negative forecasts unchanged in primary metrics; do not apply post-hoc clipping.
- Use paired day-block resampling to describe uncertainty, with a declared seed and sampling scheme.
- Publish failures, missing features and data drift. Do not adjust features or parameters after viewing test outcomes.

**If eligible new data are unavailable, the correct result is “independent test unavailable.”**
