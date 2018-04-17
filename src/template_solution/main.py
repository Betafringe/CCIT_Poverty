#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 19:16
# @Author  : Betafringe
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from load_data import connectSQL, load2pd
from analyse import compute_credit
import pandas as pd
# model = connectSQL(ip='120.78.129.209', port=13306, user='test', password='test123456', db='CUser')
path = '../../data/csv/preprocessing_data.csv'
data = load2pd(path)


def get_input(data):
    print(data.info())
    id = int(input("请输入你要查询的用户的信用id:"))
    try:
        id_list = data['id_'].values
        list_index = id_list.tolist().index(id)
    except ValueError as e:
        print('ValueError:', e)
    finally:
        print("")
    temp = data.values[list_index, :].tolist()[2:-2]
    print(temp)
    return temp




temp = get_input(data=data)
compute_credit(pernum=temp[0], year=temp[1], age=temp[2], income=temp[-1])
