#%% imports
import pandas as pd

#%% read data
ma_data = pd.read_stata("/Users/oliverwidder/PycharmProjects/ma/data/adjustet_data.dta")
ltv_average = pd.read_excel("/Users/oliverwidder/PycharmProjects/ma/data/ltv.xlsx")

#%% merge data
ltv_average_small = ltv_average[["iso3", "Year", "Month", "LTV_average"]]
ma_ltv = pd.merge(ma_data, ltv_average_small, on=["iso3", "Year", "Month"])

#%% clean data
ma_ltv_2005 = ma_ltv[ma_data["Year"] > 2004]
ma_ltv_2005_q = ma_ltv_2005[ma_ltv_2005["Month"] % 3 == 0]


#%% write data
ma_ltv_2005_q.to_stata("/Users/oliverwidder/PycharmProjects/ma/data/adjustet_data_ltv_average_2005q.dta")