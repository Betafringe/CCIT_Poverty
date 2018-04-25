#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 19:16
# @Author  : Betafringe
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from data import SQL
from analyse import ComputeCredit, add_all
import datetime


def handle_sql(input_id):
    model = SQL.sql(input_id)
    credit = add_all(model[1], model[2], model[3], model[4], model[5],
                     model[6], model[7], model[8], model[9], model[10])
    # print(model)
    print(model[0], credit)
    return model[0], credit


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

    connect = SQL()
    connect.connectSQL(ip='120.78.129.209', port=13306, user='test', password='test123456', db='CUser')
    list = connect.get_id()
    starttime = datetime.datetime.now()
    print(list)
    for i in list:
        ID = str(i[-1])
        user_data = connect.sql(ID)
        print('user_info:', user_data)
        after_data = add_all(user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6],
             user_data[7], user_data[8], user_data[9], user_data[10], user_data[11])
        print('score:', after_data)
        connect.insert_sql(int(ID), user_data[0], after_data[0], after_data[1], after_data[2],
                       after_data[3], after_data[4], after_data[5])
    stoptime = datetime.datetime.now()
    print("used time:", stoptime-starttime)

if __name__ == '__main__':
    main()