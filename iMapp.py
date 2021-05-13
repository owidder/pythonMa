#%% import and read data
import pandas as pd

iMapp = pd.read_excel("/Users/oliverwidder/PycharmProjects/ma/data/Mapp.xlsx")
ltv = pd.read_excel("/Users/oliverwidder/PycharmProjects/ma/data/ltv.xlsx")
money = pd.read_csv("/Users/oliverwidder/PycharmProjects/ma/data/18-04-21 04_05_44_theglobaleconomy_money.csv")
money.rename(columns={"Code": "iso3"}, inplace=True)

#%% merge and transform
merged_iMapp_ltv = pd.merge(iMapp, ltv, on=["iso3", "Year", "Month"])
merged_iMapp_ltv_money = pd.merge(merged_iMapp_ltv, money, on=["iso3", "Year", "Month"])