#%% import and read data
import pandas as pd
import numpy as np

def compute_quarter_mean(df, i, iso3_col, data_col, month_col):
    if((df.iloc[i][month_col]%3==0) & (df.iloc[i-1][iso3_col]==df.iloc[i][iso3_col]) & (df.iloc[i-2][iso3_col]==df.iloc[i][iso3_col])).any():
        return (df.iloc[i][data_col] + df.iloc[i-1][data_col] + df.iloc[i-2][data_col]) / 3
    else:
        return float("NaN")

def create_quarterly(df, data_col, month_col, q_col, iso3_col):
    df[q_col] = [compute_quarter_mean(df, i, iso3_col, data_col, month_col) for i in range(len(df.index))]

def compute_yoy(df, i, iso3_col, data_col, quarter_col, year_col):
    i_4 = df.iloc[i-4]
    i_0 = df.iloc[i]
    if((i_4[iso3_col]==i_0[iso3_col]) & (i_4[quarter_col]==i_0[quarter_col]) & (i_4[year_col]==(i_0[year_col]-1))):
        return (i_0[data_col]-i_4[data_col])/i_4[data_col]
    else:
        return float("NaN")

def compute_growth_2(df, iso3_col, data_col, quarter_col, year_col, growth_col):
    df[growth_col] = [compute_yoy(df, i, iso3_col, data_col, quarter_col) for i in range(len(df.index))]

def compute_growth(df, column, year, month, iso3):
    if((df["Year"]==year-1) & (df["Month"]==month) & (df["iso3"]==iso3)).any():
        last_year = df[(df["Year"]==year-1) & (df["Month"]==month) & (df["iso3"]==iso3)][column]
        this_year = df[(df["Year"]==year) & (df["Month"]==month) & (df["iso3"]==iso3)][column]
        print(f'{iso3}:{year}-{month} -> {last_year.values[0]} - {this_year.values[0]} -> {(this_year.values[0] - last_year.values[0]) / last_year.values[0]}')
        yoy = (this_year.values[0] - last_year.values[0]) / last_year.values[0]
        if(abs(yoy) == np.inf):
            print(f'inf: {iso3}:{year}-{month}')
            return float("NaN")
        else:
            return yoy
    else:
        return float("NaN")

#%% iMapp
iMapp_Q = pd.read_stata("/Users/oliverwidder/PycharmProjects/ma/data/iMaPP_Q.dta")
iMapp_Q = iMapp_Q.dropna()
iMapp_Q = iMapp_Q.astype({"AE": int, "EMDE": int, "Year": int, "Quarter": int})
del iMapp_Q["iso2"]
del iMapp_Q["ifscode"]

#%% money
money = pd.read_csv("/Users/oliverwidder/PycharmProjects/ma/data/18-04-21 04_05_44_theglobaleconomy_money.csv",
                    usecols=["Code", "Year", "Month", "Household credit billion currency units"])
money.rename(columns={"Code": "iso3"}, inplace=True)
money = money[money["Household credit billion currency units"].notna()]

create_quarterly(money, "Household credit billion currency units", "Month", "credit_Q", "iso3")
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
iMapp_Q_money_gdp["credit_yoy"] = [
    compute_growth(iMapp_Q_money_gdp, "credit_Q", iMapp_Q_money_gdp.iloc[i]["Year"], iMapp_Q_money_gdp.iloc[i]["Month"], iMapp_Q_money_gdp.iloc[i]["iso3"])
    for i in range(len(iMapp_Q_money_gdp.index))
]

iMapp_Q_money_gdp.dropna(inplace=True)
del iMapp_Q_money_gdp["Month"]
del iMapp_Q_money_gdp["Household credit billion currency units"]

#%% write
iMapp_Q_money_gdp.to_stata("/Users/oliverwidder/PycharmProjects/ma/data/iMapp_Q_credit_gdp.dta")
