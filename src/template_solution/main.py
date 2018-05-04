#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 19:16
# @Author  : Betafringe
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from data import LookupSQL, UpdateSQL
from analyse import ComputeCredit, init_add_all
import datetime
import config

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
    startime = datetime.datetime.now()
# 原始数据库参数
    origin_sql_connection = LookupSQL()
    origin_sql_settings = config.origin_sql_settings()
    origin_sql_connection.connectSQL(ip=origin_sql_settings['ip'], port=origin_sql_settings['port'],
                                     user=origin_sql_settings['user'],
                                     password=origin_sql_settings['password'], db=origin_sql_settings['db'])
# 更新数据库参数
    update_sql_connection = UpdateSQL()
    update_sql_settings = config.update_sql_settings()
    update_sql_connection.connectSQL(ip=update_sql_settings['ip'], port=update_sql_settings['port'],
                                     user=update_sql_settings['user'],
                                     password=update_sql_settings['password'], db=update_sql_settings['db'])

# 获取用户 ID
    all_user_list = origin_sql_connection.get_id()
    print(all_user_list)
    
    for i in all_user_list:
        user_id_ = str(i[-1])
        user_data = origin_sql_connection.sql(user_id_)
        print('user_info:', user_data)
        after_data = init_add_all(user_data[1], user_data[2], user_data[3], user_data[4], user_data[5], user_data[6],
             user_data[7], user_data[8], user_data[9], user_data[10], user_data[11])
        print('score:', after_data)
        update_sql_connection.insert_sql(int(user_id_), user_data[0], after_data[0], after_data[1], after_data[2],
                    after_data[3], after_data[4], after_data[5])
    stoptime = datetime.datetime.now()
    print("used time:", stoptime-startime)


if __name__ == '__main__':
    main()