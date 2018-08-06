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


def sql_config():
    origin_data = []
    after_data = []
    origin_data.append(item)
    after_data.append(compute)
    return after_data


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

# 获取用户 ID
    all_user_list = origin_sql_connection.get_id()
    num_all_user_list = len(all_user_list)
    print("USER ID INFO NUM: ", num_all_user_list)
    user_data = origin_sql_connection.batch_lookup_sql(batch_size=5000)
    # print(user_data)
    # print(type(user_data))
    # 更新数据库参数
    update_sql_connection = UpdateSQL()
    update_sql_settings = config.update_sql_settings()
    update_sql_connection.connectSQL(ip=update_sql_settings['ip'], port=update_sql_settings['port'],
                                     user=update_sql_settings['user'],
                                     password=update_sql_settings['password'], db=update_sql_settings['db'])
    flag = True
    while flag:
        time2 = datetime.datetime.now()
        print("load time", time2 - startime)
        try:
            batch = next(user_data)
            for item in batch:
                after_data = init_add_all(item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9],
                item[10], item[11], item[12], item[13], item[14])
                update_sql_connection.batch_insert_sql(int(item[0]), item[1], after_data[0], after_data[1],
                                                       after_data[2], after_data[3], after_data[4], after_data[5],
                                                       is_batch=True, batch_size=5000, count_all_users=num_all_user_list)
        except StopIteration:
            flag = False



    stoptime = datetime.datetime.now()
    print("used time:", stoptime-startime)


if __name__ == '__main__':
    main()