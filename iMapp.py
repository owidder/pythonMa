#%% import and read data
import pandas as pd

#%% iMapp
iMapp = pd.read_excel("/Users/oliverwidder/PycharmProjects/ma/data/Mapp.xlsx")
iMapp = iMapp.dropna()

iMapp_data_cols = iMapp.columns[8:]
col_dict = {col: int for col in iMapp_data_cols}
iMapp = iMapp.astype(col_dict)
iMapp = iMapp.astype({"AE": int, "EMDE": int})
del iMapp["iso2"]
del iMapp["ifscode"]

#%% quarterly
for data_col in iMapp_data_cols:
    iMapp[data_col] = [(iMapp.iloc[i][data_col] + iMapp.iloc[i-1][data_col] + iMapp.iloc[i-2][data_col])/3
                       if iMapp.iloc[i]["Month"]%3==0
                       else float("NaN")
                       for i in range(len(iMapp.index))]

#%% ltv
ltv = pd.read_excel("/Users/oliverwidder/PycharmProjects/ma/data/ltv.xlsx")

#% money
money = pd.read_csv("/Users/oliverwidder/PycharmProjects/ma/data/18-04-21 04_05_44_theglobaleconomy_money.csv",
                    usecols=["Code", "Year", "Month", "Household credit billion currency units"])
money.rename(columns={"Code": "iso3"}, inplace=True)
money = money[money["Household credit billion currency units"].notna()]

#%% gdp
gdp = pd.read_csv("/Users/oliverwidder/PycharmProjects/ma/data/18-04-21 03_56_36_theglobaleconomy_gdp.csv")

#%% compute columns

#%% merge and transform
merged_iMapp_ltv = pd.merge(iMapp, ltv, on=["iso3", "Year", "Month"])
merged_iMapp_ltv_money = pd.merge(merged_iMapp_ltv, money, on=["iso3", "Year", "Month"])