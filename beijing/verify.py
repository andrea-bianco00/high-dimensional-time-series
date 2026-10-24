"""Verify row alignment and archived MAE after running the benchmark."""
import argparse, json
from pathlib import Path
import numpy as np
import pandas as pd
parser=argparse.ArgumentParser()
parser.add_argument('--results',type=Path,default=Path('results'))
args=parser.parse_args()
d=pd.read_csv(args.results/'predictions_2016_RETROSPECTIVE.csv')
counts=d.groupby('model').size()
assert counts.nunique()==1 and counts.iloc[0]==102298
for _,g in d.groupby('model'):
    assert not g[['timestamp','station']].duplicated().any()
pairs=[set(zip(g.timestamp,g.station)) for _,g in d.groupby('model')]
assert all(p==pairs[0] for p in pairs[1:]),'Different scored target rows'
expected={'persistence':9.663209,'pm_only':8.796995,'pm_plus_lagged_covariates':8.682193}
actual={name:float(np.abs(g.truth-g.prediction).mean()) for name,g in d.groupby('model')}
for k,v in expected.items():
    assert abs(actual[k]-v)<0.0001,(k,actual[k],v)
print('PASS: aligned target rows and archived MAE')
print(json.dumps(actual,indent=2))
