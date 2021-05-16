#%% import and read
import pandas as pd
from linearmodels import PooledOLS
import statsmodels.api as sm

iMapp = pd.read_stata("/Users/oliverwidder/PycharmProjects/ma/data/iMapp_Q_credit_gdp.dta")
iMapp["Year-Q"] = iMapp["Year"].astype(str) + "-" + iMapp["Quarter"].astype(str)
iMapp.set_index(["iso3", "dateq"], inplace=True)
del iMapp["index"]
del iMapp["Country"]
del iMapp["Year"]
del iMapp["Quarter"]

#%% AE / EMDE

iMapp_AE = iMapp[iMapp["AE"]==1]
iMapp_EMDE = iMapp[iMapp["EMDE"]==1]

#%% pooled OLS

exog_cols = iMapp.columns[2:-6]

exog_AE = sm.tools.tools.add_constant(iMapp_AE[["SUM_17", "Conservation", "CCB", "LTV_Qmean"]])
endog_AE = iMapp_AE["credit_yoy"]
mod_AE = PooledOLS(endog_AE, exog_AE)
pooledOLS_AE_res = mod_AE.fit(cov_type='clustered', cluster_entity=True)
print(pooledOLS_AE_res)
