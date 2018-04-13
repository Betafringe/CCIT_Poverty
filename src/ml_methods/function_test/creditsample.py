#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 02/04/2018 17:22
# @Author  : Betafringe
# @Site    : 
# @File    : creditsample.py
# @Software: PyCharm

import pandas as pd
import re
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
import re
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
import pylab as pl

'''
data preprocessing
'''

def camel_to_snake(column_name):
    """
    converts a string that is camelCase into snake_case
    Example:
        print camel_to_snake("javaLovesCamelCase")
        > java_loves_camel_case
    Reference:
        http://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-camel-case
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', column_name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

path = "cs-training.csv"
df = pd.read_csv(path, sep=',')
df.columns = [camel_to_snake(col) for col in df.columns]
collist = df.columns.tolist()[1:]
df_lng = pd.melt(df)
df_lng = pd.melt(df[collist])
df_out = df.number_of_dependents = df.number_of_dependents.fillna(0)


'''
cross validation
'''
is_test = np.random.uniform(0, 1, len(df)) > 0.75
train = df[is_test == False]
test = df[is_test == True]
income_imputer = KNeighborsRegressor(n_neighbors=1)
train_w_monthly_income = train[train.monthly_income.isnull() == False]
train_w_null_monthly_income = train[train.monthly_income.isnull() == True]
result = train_w_monthly_income.corr().ix[: 5]
features = ['revolving_utilization_of_unsecured_lines', 'debt_ratio',
            'monthly_income', 'age', 'number_of_times90_days_late']
