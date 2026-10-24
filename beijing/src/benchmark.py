"""Retrospective fixed-config PM2.5 benchmark; 2017 observations are excluded."""
import zipfile, hashlib, json, time, argparse
from pathlib import Path
import numpy as np
import pandas as pd
from lightgbm import LGBMRegressor

STATIONS = ('Aotizhongxin','Changping','Dingling','Dongsi','Guanyuan','Gucheng','Huairou','Nongzhanguan','Shunyi','Tiantan','Wanliu','Wanshouxigong')
LAGS = (1,2,3,6,12,24)
VARIABLES = ('TEMP','PRES','DEWP','RAIN','WSPM','PM10','SO2','NO2','CO','O3')
CHECKSUM = 'd1b9261c54132f04c374f762f1e5e512af19f95c95fd6bfa1e8ac7e927e3b0b8'

def load(archive):
    frames, extra = {}, {}
    with zipfile.ZipFile(archive) as z:
        for station in STATIONS:
            matches = [n for n in z.namelist() if Path(n).name == f'PRSA_Data_{station}_20130301-20170228.csv']
            assert len(matches) == 1
            with z.open(matches[0]) as f:
                d = pd.read_csv(f)
            d = d.loc[d.year < 2017].copy()
            idx = pd.to_datetime(d[['year','month','day','hour']])
            assert not idx.duplicated().any()
            frames[station] = pd.Series(d['PM2.5'].to_numpy(), index=idx)
            for v in VARIABLES:
                extra[f'{station}_{v}'] = pd.Series(d[v].to_numpy(), index=idx)
    levels = pd.DataFrame(frames).sort_index()
    environment = pd.DataFrame(extra).sort_index()
    assert len(levels) == 33648 and levels.index.equals(environment.index)
    return levels, environment

def features(levels, environment):
    base = {f'{s}_pm_lag{k}': levels[s].shift(k).to_numpy(dtype='float32') for s in STATIONS for k in LAGS}
    idx = levels.index
    base.update(hour_sin=np.sin(2*np.pi*idx.hour/24), hour_cos=np.cos(2*np.pi*idx.hour/24),
                dayofyear_sin=np.sin(2*np.pi*idx.dayofyear/365.25),
                dayofyear_cos=np.cos(2*np.pi*idx.dayofyear/365.25))
    full = dict(base)
    for s in STATIONS:
        for v in VARIABLES:
            full[f'{s}_{v}_lag1'] = environment[f'{s}_{v}'].shift(1).to_numpy(dtype='float32')
    return pd.DataFrame(base,index=idx,dtype='float32'), pd.DataFrame(full,index=idx,dtype='float32')

def model():
    return LGBMRegressor(n_estimators=70, learning_rate=.045, num_leaves=31,
                        max_depth=-1, min_child_samples=80, reg_lambda=10,
                        verbosity=-1, n_jobs=2, random_state=2026)

def run(archive, output):
    output.mkdir(parents=True, exist_ok=True)
    if hashlib.sha256(archive.read_bytes()).hexdigest() != CHECKSUM:
        raise ValueError('Dataset checksum mismatch: use audited official inner ZIP')
    started = time.time()
    levels, environment = load(archive)
    base, full = features(levels, environment)
    idx = levels.index
    tr = idx < '2015-01-01'
    va = (idx >= '2015-01-01') & (idx < '2016-01-01')
    ev = idx >= '2016-01-01'
    predictions, validations = [], []
    for station in STATIONS:
        y = levels[station]
        previous = y.shift(1)
        valid = y.notna() & previous.notna()
        delta = y - previous
        train, validation, test = tr & valid, va & valid, ev & valid
        assert train.sum() > 10000 and test.sum() > 7000
        for name, X in [('pm_only',base),('pm_plus_lagged_covariates',full)]:
            fitted = model()
            fitted.fit(X.loc[train], delta.loc[train])
            p = previous.loc[validation].to_numpy() + fitted.predict(X.loc[validation])
            validations.append((station,name,float(np.abs(y.loc[validation].to_numpy()-p).mean()),int(validation.sum())))
            fitted = model()
            fitted.fit(X.loc[train | validation],delta.loc[train | validation])
            p = previous.loc[test].to_numpy() + fitted.predict(X.loc[test])
            predictions.append(pd.DataFrame({'timestamp':idx[test], 'station':station, 'model':name,
                                             'truth':y.loc[test].to_numpy(), 'prediction':p}))
        predictions.append(pd.DataFrame({'timestamp':idx[test], 'station':station, 'model':'persistence',
                                         'truth':y.loc[test].to_numpy(), 'prediction':previous.loc[test].to_numpy()}))
        print('completed',station,round(time.time()-started,1),flush=True)
    pred = pd.concat(predictions,ignore_index=True)
    pred['ae'] = (pred.truth-pred.prediction).abs()
    pred['se'] = (pred.truth-pred.prediction)**2
    pred.to_csv(output/'predictions_2016_RETROSPECTIVE.csv',index=False)
    pd.DataFrame(validations,columns=['station','model','validation_2015_mae','n']).to_csv(output/'validation_2015.csv',index=False)
    summary = pred.groupby('model').agg(n=('ae','size'),mae=('ae','mean'),mse=('se','mean'),
                                         negative=('prediction',lambda x:int((x<0).sum())))
    summary['rmse'] = np.sqrt(summary.pop('mse'))
    summary.to_csv(output/'summary.csv')
    pred.groupby(['station','model']).ae.mean().unstack().to_csv(output/'station_mae.csv')
    manifest = {'source_sha256':CHECKSUM,'target':'one-hour-ahead PM2.5 with observed t-1',
                'training':'2013-03 through 2014-12','validation':'2015',
                'refit':'2013-03 through 2015-12','evaluation':'2016: retrospective, repeatedly inspected',
                '2017_loaded':False,'covariates':'all-station t-1 weather and pollutants',
                'selection':'fixed configuration for ablation, selected after exploratory inspection',
                'elapsed_seconds':round(time.time()-started,2)}
    (output/'manifest.json').write_text(json.dumps(manifest,indent=2))
    print(summary.to_string(),flush=True)

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--data',type=Path,required=True)
    parser.add_argument('--output',type=Path,default=Path('results'))
    args=parser.parse_args()
    run(args.data,args.output)
