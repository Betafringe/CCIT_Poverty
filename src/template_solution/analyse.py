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


class Pre:
    def preprocessing_pd(self, df):
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


class ComputeCredit(object):
    def __init__(self, per, year, age, income):
        self.per = per
        self.year = year
        self.age = age
        self.income = income
        # self.level = level

    def sigmoid(self, inX):
        return 1.0 / (1 + math.exp(-inX))

    def normal_distribution(self, X):
        PI = 3.141
        return math.exp(1)**(-(X**2)/2)*(1.0/2*PI)**0.5

    def per_part(self, per_weights):
        if self.per < 3:
            value = 5
        elif 3 <= self.per <= 5:
            value = 3
        else:
            value = 2
        return per_weights*value

    def year_part(self, year_weights):
        if int(self.year) == 2017 or 2018:
            value = 1
        else:
            value = 2017-int(self.year)
        return value*year_weights

    def age_part(self, age_weights):
        if self.age < 20 or self.age > 50:
            value = 2
        else:
            value = (self.age-20) * 0.2
        return value*age_weights

    def income_part(self, income_weights):
        ratio = self.income/self.per
        if ratio < 1:
            value = 2
        elif 1 <= ratio < 1.6:
            value = 3
        elif 1.6 <= ratio < 3:
            value = 4
        else:
            value = 1
        return value*income_weights


def add_all(per, year, age, income):
    test = ComputeCredit(per, year, age, income)
    is_full = test.year_part(0.5)
    ###要显示别的部分
    total_credit = int(230*(test.per_part(0.2) + test.year_part(0.1) + test.age_part(0.4) + test.income_part(0.3)))
    return total_credit
