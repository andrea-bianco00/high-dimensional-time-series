# Beijing PM2.5 forecasting benchmark

This folder contains a retrospective one-hour-ahead benchmark using the official [UCI Beijing Multi-Site Air Quality dataset](https://archive.ics.uci.edu/dataset/501/beijingmultisiteairqualitydata), covering 12 stations. Raw data are not redistributed.

Install dependencies: `python -m pip install -r beijing/requirements.txt`.

Download the official UCI archive and extract the inner ZIP with 12 station CSVs. From the repository root, run:

```bash
python beijing/src/benchmark.py --data /absolute/path/to/beijing_official_inner.zip --output beijing/results
```

The script checks the SHA-256 of the audited inner ZIP. Training: 2013–2014; validation: 2015; refit: 2013–2015; retrospective evaluation: 2016. All covariates are lagged at least one hour. 2017 observations are not loaded. Real-time cross-station latency is unverified.

**2016 is not an untouched independent test**; it was inspected during prior model development. The saved aggregate metrics are archived outputs, not evidence of a fresh-environment rerun of the published source. Negative forecasts are not clipped.
