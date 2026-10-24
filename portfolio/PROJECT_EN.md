# High-Dimensional Time Series and PM2.5 Forecasting

**Andrea Bianco — research portfolio**

The original university study (with Emidio Grillo and Luca Nudo) investigated high-dimensional time series from 516 Taiwan AirBox sensors, including regularized VAR-related modeling in R. A subsequent, distinct Python extension studied one-hour-ahead PM2.5 forecasting using 12 stations from the UCI Beijing Multi-Site Air Quality dataset.

In a retrospective 2016 evaluation of 102,298 station-hours, a fixed LightGBM configuration using lagged environmental variables achieved MAE 8.682 compared with 9.663 for persistence, a 10.15% reduction. This is **exploratory development performance**, not a genuinely untouched test, because the evaluation period was repeatedly inspected during development. Beijing is not a direct external validation of Taiwan. Reproducibility scripts and research limitations are documented in the repository.
