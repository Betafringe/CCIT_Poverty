#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/1 18:49
# @Author  : Betafringe
# @Site    : 
# @File    : analyse.py
# @Software: PyCharm
import datetime
import math
import random


class ComputeCredit(object):
    def __init__(self, per, year, age, income, lvl, count, sex, landsize, sale_income, out_poverty, industrial_scale,
                 kinds, kinds_num):
        self.per = per
        self.year = year
        self.age = age
        self.income = income
        self.lvl = lvl
        self.count = count
        self.sex = sex
        self.land_size = landsize
        self.sale_income = sale_income
        self.out_poverty = out_poverty
        self.industrial_scale = industrial_scale
        self.kinds = kinds
        self.kinds_num = kinds_num

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
        if self.income < 1500:
            value = 1
        elif 1500 <= self.income < 3500:
            value = 3
        elif 3500 <= self.income < 100000:
            value = 4
        else:
            value = 2
        return value*income_weights

    def lvl_part(self, lvl_weights):
        if self.lvl == "一般农户" or "低保户" or "低保贫苦户":
            value = 1
        elif self.lvl == "县级" or "区级" or "县" or "县级示范" or "市级":
            value = 2
        elif self.lvl == "省级" or "省级示范" or "省" or "四川省":
            value = 4
        else:
            value = 3
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
        if self.land_size == 0:
            value = 0
        else:
            value = 1
        return value * landsize_weights

    def sale_income(self, sale_income_weights):
        pass

    def out_poverty(self, out_poverty_weights):
        if self.out_poverty == "否":
            value = 0
        else:
            value = 10
        return value*out_poverty_weights

    def industry_scale(self, industry_weights):
        if self.industrial_scale == 0:
            value = 2
        else:
            value = 8
        return value*industry_weights

    def is_kind(self, kind_weights):
        if self.kinds == '生猪':
            if self.kinds_num < 30:
                kinds_value = 1
            elif 30 <= self.kinds_num < 100:
                kinds_value = 3
            else:
                kinds_value = 5
        elif self.kinds =='牛羊':
            if self.kinds_num < 20:
                kinds_value = 1
            elif  20 <=self.kinds_num <50:
                kinds_value = 3
            else:
                kinds_value = 5
        elif self.kinds == '蔬菜' or '水稻' or '玉米' or '果树':
            if self.kinds_num < 1.8:
                kinds_value = 1
            else:
                kinds_value = 3
        else:
            if self.kinds_num < 80:
                kinds_value = 1
            else:
                kinds_value = 3

        kinds_dic = {'生猪':6,'牛羊':8,'家禽':5,'水稻':5,'玉米':5,'蔬菜':4,'果树':5,'0':0,'1':0}  
        baseline_none_key = 10
        value = kinds_dic[self.kinds] * kinds_value / 5 + baseline_none_key
        return value*kind_weights


def sigmoid(X):
    return 1.0 / (1 + math.exp(-X))


def normal_distribution(X):
    PI = 3.141
    return math.exp(1) ** (-(X ** 2) / 2) * (1.0 / 2 * PI) ** 0.5


def init_add_all(per, year, age, income, lvl, count, sex, landsize, sale_income, out_poverty, industrial_scale,
                 kinds, kinds_num):
    single_user = ComputeCredit(per, year, age, income, lvl,
                                count, sex, landsize, sale_income, out_poverty, industrial_scale, kinds, kinds_num)
    character = single_user.per_part(0.03) + single_user.income_part(0.015) + single_user.age_part(0.015) \
                + single_user.lvl_part(0.01) + single_user.sex_part(0.01) + single_user.is_kind(0.02)

    appointment = single_user.income_part(0.07) + single_user.sex_part(0.03) + 0.35

    history = single_user.year_part(0.6*0.5) + single_user.income_part(0.2*0.5)

    stickiness = single_user.count_part(0.03) + single_user.year_part(0.04) + single_user.count_part(0.03) + 0.35

    relations = single_user.sex_part(0.02) + single_user.per_part(0.06) + single_user.income_part(0.02) + 0.32

    if character >= 1 or appointment >= 1 or history >= 1 or stickiness >= 1 or relations >= 1:
        character, appointment, history, stickiness, relations = 0.7, 0.6, 0.6, 0.6, 0.5

    random_bias = int(random.randint(5, 50))
    total_credit = int((character + appointment + history + stickiness + relations)*850/5) + random_bias
    return total_credit, character, appointment, history, stickiness, relations


def update(per, year, age, income, lvl, count, sex, landsize, sale_income, out_poverty, industrial_scale):
    single_user = ComputeCredit(per, year, age, income, lvl,
                                count, sex, landsize, sale_income, out_poverty, industrial_scale)
    character = single_user.per_part(0.2*0.2) + single_user.income_part(0.2*0.2) + single_user.age_part(0.2*0.2) \
                + single_user.lvl_part(0.2*0.15) + single_user.sex_part(0.2*0.15) + 0.02

    appointment = single_user.income_part(0.07) + single_user.sex_part(0.03) + 0.35

    history = single_user.year_part(0.6*0.5) + single_user.income_part(0.2*0.5)

    linear = 0.001
    stickiness = single_user.count_part(0.03) + single_user.year_part(0.04) + single_user.count_part(0.03) + 0.38 + linear

    relations = single_user.sex_part(0.01) + single_user.per_part(0.06) + single_user.income_part(0.02) + 0.35

    if character >= 1 or appointment >= 1 or history >= 1 or stickiness >= 1 or relations >= 1:
        character, appointment, history, stickiness, relations = 0.7, 0.6, 0.6, 0.6, 0.5
    else:
        pass
    total_credit = int((character + appointment + history + stickiness + relations)*850/5) + 10

    return total_credit, character, appointment, history, stickiness, relations


'''
test func code
'''

