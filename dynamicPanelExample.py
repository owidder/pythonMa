#%% imports
import pandas as pd
from linearmodels import PooledOLS
import statsmodels.api as sm

#%% read data
ps_raw = pd.read_stata("/Users/oliverwidder/PycharmProjects/ma/data/psidextract.dta")
ps = ps_raw.astype({"id": int, "t": int})
ps.set_index(["id", "t"], inplace=True)

exog = sm.tools.tools.add_constant(ps["lwage"])
endog = ps["wks"]
mod = PooledOLS(endog, exog)
pooledOLS_res = mod.fit(cov_type='clustered', cluster_entity=True)