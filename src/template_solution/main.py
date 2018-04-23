#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 19:16
# @Author  : Betafringe
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from data import connectSQL, load2pd
from analyse import ComputeCredit, add_all
import pandas as pd


def handle_sql(arg_id):
    model = connectSQL(ip='120.78.129.209', port=13306, user='test', password='test123456', db='CUser', lookup_id=arg_id)
    credit = add_all(model[1], model[2], model[3], model[4])
    # print(model)
    print(credit, model[0])


def handle_dataframes(data, arg_id):
    id_ = arg_id
    try:
        id_list = data['id_'].values
        list_index = id_list.tolist().index(id_)
    except ValueError as e:
        print('ValueError:', e)
    finally:
        temp = data.values[list_index, :].tolist()[2:-2]
    print("该人的各项属性为：", temp)
    return temp


def main():
    path = '../../data/csv/preprocessing_data.csv'
    id = str(input())
    dataframe = load2pd(path)
    handle_sql(arg_id=id)


if __name__ == '__main__':
    main()