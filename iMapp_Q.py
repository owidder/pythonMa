#%% import and read data
import pandas as pd
import numpy as np

def compute_quarter_mean(df, i, iso3_col, data_col, month_col, year_col):
    i_0 = df.iloc[i]
    i_1 = df.iloc[i-1]
    i_2 = df.iloc[i-2]
    if((i_0[month_col]%3==0) & (i_1[iso3_col]==i_0[iso3_col]) & (i_2[iso3_col]==i_0[iso3_col])):
        mean = (df.iloc[i][data_col] + df.iloc[i-1][data_col] + df.iloc[i-2][data_col]) / 3
        print(f'q-mean: {i_0[iso3_col]}/{i_0[year_col]}/{i_0[month_col]}: ({i_0[data_col]} + {i_1[data_col]} + {i_2[data_col]})/3 = {mean}')
        return (df.iloc[i][data_col] + df.iloc[i-1][data_col] + df.iloc[i-2][data_col]) / 3
    else:
        return float("NaN")

def create_quarter_mean_col(df, data_col, month_col, quarter_mean_col, iso3_col, year_col):
    df[quarter_mean_col] = [compute_quarter_mean(df, i, iso3_col, data_col, month_col, year_col) for i in range(len(df.index))]

def compute_yoy(df, i, iso3_col, data_col, quarter_col, year_col):
    i_4 = df.iloc[i-4]
    i_0 = df.iloc[i]
    if((i_4[iso3_col]==i_0[iso3_col]) & (i_4[quarter_col]==i_0[quarter_col]) & (i_4[year_col]==(i_0[year_col]-1))):
        growth = (i_0[data_col]-i_4[data_col])/i_4[data_col]
        print(f'yoy: {i_0[iso3_col]}/{i_0[year_col]}/{i_0[quarter_col]}: ({i_0[data_col]} - {i_4[data_col]}) / {i_4[data_col]} = {growth}')
        if(abs(growth) == np.inf):
            return float("NaN")
        else:
            return growth
    else:
        return float("NaN")

def create_yoy_col(df, iso3_col, data_col, quarter_col, year_col, yoy_col):
    df[yoy_col] = [compute_yoy(df, i, iso3_col, data_col, quarter_col, year_col) for i in range(len(df.index))]

def compute_four_quarter_mean(df, i, iso3_col, data_col):
    i_0 = df.iloc[i]
    i_1 = df.iloc[i-1]
    i_2 = df.iloc[i-2]
    i_3 = df.iloc[i-3]
    if(i_3[iso3_col]==i_0[iso3_col]):
        return (i_0[data_col]+i_1[data_col]+i_2[data_col]+i_3[data_col])/4
    else:
        return float("NaN")

def create_four_quarter_mean_col(df, iso3_col, data_col, four_quarter_mean_col):
    print(f'4-quarter-mean: {four_quarter_mean_col}')
    df[four_quarter_mean_col] = [compute_four_quarter_mean(df, i, iso3_col, data_col) for i in range(len(df.index))]

#%% iMapp
iMapp_Q = pd.read_stata("/Users/oliverwidder/PycharmProjects/ma/data/iMaPP_Q.dta")
iMapp_Q = iMapp_Q.dropna()
iMapp_Q = iMapp_Q.astype({"AE": int, "EMDE": int, "Year": int, "Quarter": int})

#%% money
money = pd.read_csv("/Users/oliverwidder/PycharmProjects/ma/data/18-04-21 04_05_44_theglobaleconomy_money.csv",
                    usecols=["Code", "Year", "Month", "Household credit billion currency units"])
money.rename(columns={"Code": "iso3"}, inplace=True)
money = money[money["Household credit billion currency units"].notna()]

create_quarter_mean_col(money, "Household credit billion currency units", "Month", "credit_Q", "iso3", "Year")
money["Quarter"] = [(money.iloc[i]["Month"]/3 if money.iloc[i]["Month"]%3==0 else float("NaN")) for i in range(len(money.index))]
money.dropna(inplace=True)
money = money.astype({"Quarter": int})

iMapp_Q_money = pd.merge(iMapp_Q, money, on=["iso3", "Year", "Quarter"])

del iMapp_Q

#%% gdp
gdp = pd.read_csv("/Users/oliverwidder/PycharmProjects/ma/data/18-04-21 03_56_36_theglobaleconomy_gdp.csv",
                  usecols=["Code", "Year", "Month", "Economic growth percent change in quarterly real GDP"])
gdp = gdp.rename(columns={"Code": "iso3", "Economic growth percent change in quarterly real GDP": "gdp_yoy"})

iMapp_Q_money_gdp = pd.merge(iMapp_Q_money, gdp, on=["iso3", "Year", "Month"])

del iMapp_Q_money

#%% credit_yoy
create_yoy_col(iMapp_Q_money_gdp, "iso3", "credit_Q", "Quarter", "Year", "credit_yoy")

iMapp_Q_money_gdp.dropna(inplace=True)
del iMapp_Q_money_gdp["Month"]
del iMapp_Q_money_gdp["Household credit billion currency units"]

#%% 4-quarter-means
policy_cols = iMapp_Q_money_gdp.columns[9:-3]
for pcol in policy_cols:
    create_four_quarter_mean_col(iMapp_Q_money_gdp, "iso3", pcol, f'{pcol}_4Qmean')

#%% write
iMapp_Q_money_gdp.to_stata("/Users/oliverwidder/PycharmProjects/ma/data/iMapp_Q_credit_gdp_4qmean.dta")
