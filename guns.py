#%% imports and read data
import pandas as pd
from linearmodels import PooledOLS
import statsmodels.api as sm

gunsraw = pd.read_csv("/Users/oliverwidder/PycharmProjects/ma/data/guns.csv", usecols=["stateid", "year", "avginc", "vio"],
                      index_col=["stateid", "year"])
guns = gunsraw.rename(columns={"avginc": "income", "stateid": "state", "vio": "violent"})


#%% transform data
years = guns.index.get_level_values("year").to_list()
guns["year"] = pd.Categorical(years)

#%% pooled OLS

exog = sm.tools.tools.add_constant(guns['income'])
endog = guns['violent']
mod = PooledOLS(endog, exog)
pooledOLS_res = mod.fit(cov_type='clustered', cluster_entity=True)

print(pooledOLS_res)
