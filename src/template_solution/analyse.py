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
import random

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
    def __init__(self, per, year, age, income, lvl, count, sex, landsize, sale_income, out_poverty, industrial_scale):
        self.per = per
        self.year = year
        self.age = age
        self.income = income
        self.lvl = lvl
        self.count = count
        self.sex = sex
        self.landsize = landsize
        self.sale_income = sale_income
        self.out_poverty = out_poverty
        self.industrial_scale = industrial_scale

    def per_part(self, per_weights):
        if self.per < 3:
            value = 5
        elif 3 <= self.per <= 5:
            value = 3
        else:
            value = 2
        return per_weights*value

    def year_part(self, year_weights):
        if self.year is int:
            if int(self.year) == 2017 or 2018:
                value = 1
            elif int(self.year) > datetime.datetime.now().year:
                value = 0
            else:
                value = 2018-int(self.year)
        else:
            value = 1
        return value*year_weights

    def age_part(self, age_weights):
        if self.age < 20 or self.age > 45:
            value = 2
        else:
            value = (self.age-20) * 0.32 + 2
        return value*age_weights

    def income_part(self, income_weights):
        if self.income < 1000:
            value = 1
        elif 1000 <= self.income < 4000:
            value = 3
        elif 3500 <= self.income < 100000:
            value = 4
        else:
            value = 2
        return value*income_weights

    def lvl_part(self, lvl_weights):
        if self.lvl == "一般农户" or "低保户" or "低保贫苦户":
            value = 1
        elif self.lvl == "县级" or "区级" or "县":
            value = 2
        elif self.lvl == "省级" or "省级示范" or "省":
            value = 3
        else:
            value = 4
        return value*lvl_weights

    def count_part(self, count_weights):
        if self.count/39 < 0.5:
            value = 3
        else:
            value = 7
        return value*count_weights

    def sex_part(self, sex_weights):
        if self.sex == 0:
            value = 7
        else:
            value = 3
        return value*sex_weights

    def landsize(self, landsize_weights):
        pass

    def sale_income(self, sale_income_weights):
        pass

    def out_poverty(self, out_poverty_weights):
        if self.out_poverty == "否":
            value = 0
        else:
            value = 10
        return value*out_poverty_weights


def sigmoid(X):
    return 1.0 / (1 + math.exp(-X))


def normal_distribution(X):
    PI = 3.141
    return math.exp(1) ** (-(X ** 2) / 2) * (1.0 / 2 * PI) ** 0.5


def init_add_all(per, year, age, income, lvl, count, sex, landsize, sale_income, out_poverty, industrial_scale):
    single_user = ComputeCredit(per, year, age, income, lvl,
                                count, sex, landsize, sale_income, out_poverty, industrial_scale)
    character = single_user.per_part(0.2*0.2) + single_user.income_part(0.2*0.3) + single_user.age_part(0.2*0.2) \
                + single_user.lvl_part(0.2*0.1) + single_user.sex_part(0.2*0.2)

    appointment = single_user.income_part(0.07) + single_user.sex_part(0.03) + 0.35

    history = single_user.year_part(0.6*0.5) + single_user.income_part(0.2*0.5)

    stickiness = single_user.count_part(0.03) + single_user.year_part(0.04) + single_user.count_part(0.03) + 0.35

    relations = single_user.sex_part(0.01) + single_user.per_part(0.06) + single_user.income_part(0.02) + 0.35
    random_bias = int(random.randint(5, 50))
    total_credit = int((character + appointment + history + stickiness + relations)*850/5) + random_bias

    return total_credit, character, appointment, history, stickiness, relations


def update(user_id, para):
    pass
