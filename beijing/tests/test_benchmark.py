import sys, unittest, hashlib, os
from pathlib import Path
import numpy as np
import pandas as pd
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import benchmark as b

class Integrity(unittest.TestCase):
    def test_source_hash(self):
        p=Path(os.environ.get('HDTS_DATA','data/beijing_official_inner.zip'))
        if not p.exists():
            self.skipTest('Dataset not available locally')
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),b.CHECKSUM)
    def test_features_no_future_leakage(self):
        idx=pd.date_range('2015-01-01',periods=72,freq='h')
        levels=pd.DataFrame({s:np.arange(72,dtype=float) for s in b.STATIONS},index=idx)
        met=pd.DataFrame({f'{s}_{v}':np.arange(72,dtype=float) for s in b.STATIONS for v in b.VARIABLES},index=idx)
        x1=b.features(levels,met)[1]
        levels.iloc[40:,:]=9999
        met.iloc[40:,:]=9999
        x2=b.features(levels,met)[1]
        pd.testing.assert_frame_equal(x1.iloc[:41],x2.iloc[:41])
        self.assertFalse(x1.iloc[41].equals(x2.iloc[41]))
    def test_split(self):
        idx=pd.date_range('2014-12-31 23:00',periods=4,freq='h')
        self.assertEqual(list(idx<'2015-01-01'),[True,False,False,False])
    def test_model_config(self):
        m=b.model()
        self.assertEqual(m.n_estimators,70)
        self.assertEqual(m.num_leaves,31)
if __name__=='__main__':
    unittest.main()
