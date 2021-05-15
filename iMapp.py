#%% import and read data
import pandas as pd

#%% iMapp
iMapp = pd.read_excel("/Users/oliverwidder/PycharmProjects/ma/data/Mapp.xlsx")
iMapp = iMapp.dropna()

iMapp = iMapp.astype({"AE": int, "EMDE": int})
del iMapp["iso2"]
del iMapp["ifscode"]

#%% ltv
ltv = pd.read_excel("/Users/oliverwidder/PycharmProjects/ma/data/ltv.xlsx", usecols=["iso3", "Year", "Month", "LTV_average"])
iMapp_ltv = pd.merge(iMapp, ltv, on=["iso3", "Year", "Month"])

del iMapp
del ltv

#%% money
money = pd.read_csv("/Users/oliverwidder/PycharmProjects/ma/data/18-04-21 04_05_44_theglobaleconomy_money.csv",
                    usecols=["Code", "Year", "Month", "Household credit billion currency units"])
money.rename(columns={"Code": "iso3"}, inplace=True)
money = money[money["Household credit billion currency units"].notna()]
iMapp_ltv_money = pd.merge(iMapp_ltv, money, on=["iso3", "Year", "Month"])

del iMapp_ltv

#%% quarterly
iMapp_ltv_money_data_cols = iMapp_ltv_money.columns[8:]
for data_col in iMapp_ltv_money_data_cols:
    iMapp_ltv_money[data_col] = [(iMapp_ltv_money.iloc[i][data_col] + iMapp_ltv_money.iloc[i-1][data_col] + iMapp_ltv_money.iloc[i-2][data_col])/3
                       if iMapp_ltv_money.iloc[i]["Month"]%3==0
                       else float("NaN")
                       for i in range(len(iMapp_ltv_money.index))]

iMapp_ltv_money = iMapp_ltv_money.dropna()

#%% gdp
gdp = pd.read_csv("/Users/oliverwidder/PycharmProjects/ma/data/18-04-21 03_56_36_theglobaleconomy_gdp.csv",
                  usecols=["Code", "Year", "Month", "Economic growth percent change in quarterly real GDP"])
gdp = gdp.rename(columns={"Code": "iso3", "Economic growth percent change in quarterly real GDP": "gdp_yoy"})
iMapp_ltv_money_gdp = pd.merge(iMapp_ltv_money, gdp, on=["iso3", "Year", "Month"])

del iMapp_ltv_money

#%% credit_yoy
def compute_growth(column, year, month, iso3):
    if((iMapp_ltv_money_gdp["Year"]==year-1) & (iMapp_ltv_money_gdp["Month"]==month) & (iMapp_ltv_money_gdp["iso3"]==iso3)).any():
        last_year = iMapp_ltv_money_gdp[(iMapp_ltv_money_gdp["Year"]==year-1) & (iMapp_ltv_money_gdp["Month"]==month) & (iMapp_ltv_money_gdp["iso3"]==iso3)][column]
        this_year = iMapp_ltv_money_gdp[(iMapp_ltv_money_gdp["Year"]==year) & (iMapp_ltv_money_gdp["Month"]==month) & (iMapp_ltv_money_gdp["iso3"]==iso3)][column]
        print(f'{iso3}:{year}-{month} -> {last_year.values[0]} - {this_year.values[0]} -> {(this_year.values[0] - last_year.values[0]) / last_year.values[0]}')
        return (this_year.values[0] - last_year.values[0]) / last_year.values[0]
    else:
        return float("NaN")

iMapp_ltv_money_gdp["credit_yoy"] = [
    compute_growth("Household credit billion currency units", iMapp_ltv_money_gdp.iloc[i]["Year"], iMapp_ltv_money_gdp.iloc[i]["Month"], iMapp_ltv_money_gdp.iloc[i]["iso3"])
    for i in range(len(iMapp_ltv_money_gdp.index))
]

del iMapp_ltv_money_gdp["Household credit billion currency units"]

#%% write
iMapp_ltv_money_gdp.to_stata("/Users/oliverwidder/PycharmProjects/ma/data/fertig_iMaPP_Q_all.dta")
