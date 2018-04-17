#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 18:49
# @Author  : Betafringe
# @Site    : 
# @File    : operate.py
# @Software: PyCharm
import pandas as pd
import datetime
import math

def preprocessing_pd(df):
    df_drop_na = df.drop(['householder_name', 'address', 'city', 'city_id', 'county', 'town', 'village_name',
                          'phone_num', 'helper_number', 'input_user', 'input_time', 'city_recorder',
                          'county_recorder', 'helper', 'real_time', 'check_status'], axis=1)

    df_income = df_drop_na[df_drop_na['income'] < 100000]
    df_ = df_income[df_income['year'] < datetime.datetime.now().year]
    ID_card = df_['ID_card']
    ID_list = []
    for item in ID_card:
        sl_item = datetime.datetime.now().year - int(item[6:10])
        ID_list.append(sl_item)
    df_.loc[:, 'ID_card'] = ID_list

    income_mean = df_['income'].mean()
    df_['income'] = df_.loc[:, 'income'].replace(0, income_mean)
    df_['out_poverty'] = df_['out_poverty'].replace('否', '0')
    df_['out_poverty'] = df_['out_poverty'].replace('是', '1')
    df_['level'] = df_['level'].replace('一般农户', '0')
    df_['level'] = df_['level'].replace('低保户', '0')
    df_['level'] = df_['level'].replace('低保贫苦户', '0')
    df_['level'] = df_['level'].replace('县级', '1')
    df_['level'] = df_['level'].replace('区级', '1')
    df_['level'] = df_['level'].replace('县', '1')
    df_['level'] = df_['level'].replace('县级示范', '2')
    df_['level'] = df_['level'].replace('省级', '3')
    df_['level'] = df_['level'].replace('省', '3')
    df_['level'] = df_['level'].replace('省级示范', '3')
    df_['level'] = df_['level'].replace('四川省', '3')
    df_['level'] = df_['level'].replace('国家级', '4')

    return df_

def compute_credit(pernum, year, age, income):
    credit_init = 100
    PI = math.pi
    def sigmoid(inX):
        return 1.0 / (1 + math.exp(-inX))
    def normal_distribution(X):
        return math.exp(1)**(-(X**2)/2)*(1.0/2*PI)**0.5
    if pernum < 3:
        value_pernum = 3
    elif 3 <= pernum < 5:
        value_pernum = 2
    else:
        value_pernum = 1
    if  year == 2016:
        value_year = 2
    else:
        value_year = 1
    if age < 20:
        value_age = 1
    elif 20 <= age < 50:
        value_age = 3
    else:
        value_age = 0
    if income < 3000:
        value_income = 1
    elif 3000 <= income < 10000:
        value_income = 2
    else:
        value_income = 3

    credit_update = ((value_age + value_income + value_year + value_pernum)/12) * credit_init
    print("该自然人的信用评分为：", credit_update)
    return credit_update
def handle_sql(args):
    pass


