#%% imports
import pandas as pd
import numpy as np

#%% read data
ma_ltv_2005_q = pd.read_stata("/Users/oliverwidder/PycharmProjects/ma/data/adjustet_data_ltv_average_2005q.dta")

#%% describe
ma_ltv_2005_q['Capital_HH'].astype(float).describe()

#%% columns
ma_ltv_2005_q.columns

#%% count
for c in ['CCB', 'Conservation', 'Capital', 'Capital_Gen', 'Capital_HH',
       'Capital_Corp', 'Capital_FX', 'LVR', 'LLP', 'LCG', 'LCG_Gen', 'LCG_HH',
       'LCG_Corp', 'LoanR', 'LoanR_HH', 'LoanR_Corp', 'LFC', 'LTV', 'DSTI',
       'Liquidity', 'LTD', 'LFX', 'RR', 'RR_FCD', 'SIFI', 'OT',
       'SUM_17', 'household_credit', 'gdp', 'LTV_average']:
    nums = np.count_nonzero(ma_ltv_2005_q[c].astype(float))
    print(f'{c}: {nums}')