#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/20 20:12
# @Author  : Betafringe
# @Site    :
# @File    : data_preprocessing.py
# @Software: PyCharm

import numpy as np
import re
import pandas as pd
df = pd.read_csv("user_info.csv")

df_dropna = df.dropna()
df_drop_nacolumn = df_dropna.drop(['householder_name', 'address', 'city', 'county', 'town', 'village_name', 'phone_num',
                                   'helper_number', 'input_user', 'input_time', 'city_recorder', 'county_recorder'], axis=1)

for index, row in df_drop_nacolumn.iterrows():
    print(row["income"])

# age_IDcard_columns = df_drop_nacolumn['ID_card']
# #
# collist = df_dropna.columns.tolist()[1:]
# df_lng = pd.melt(df[collist])=
# print(pd.crosstab(df.year, df.per_num))


def deal_error_data():
    pass

def get_age_idcard(arguments):
    age = []
    for item in arguments:
        current_age = int(item[6:10])
        age.append(current_age)locals()
    yield age

def deal_income():
    aveIncome = df_drop_nacolumn['ave_time'].mean()

    pass

def deal_chinesechar():
    pass



def  main():
    if __name__ == '__main__':
        pass

