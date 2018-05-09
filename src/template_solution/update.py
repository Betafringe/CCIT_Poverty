#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/8 20:25
# @Author  : Betafringe
# @Site    : 
# @File    : update.py
# @Software: PyCharm
import pymysql.cursors
import pymysql
from analyse import update
from data import LookupSQL, UpdateCredit, UpdateSQL
import config


def run():
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

    update_credit_connection = UpdateCredit()
    update_credit_settings = config.update_sql_settings()
    update_credit_connection.connectSQL(ip=update_credit_settings['ip'], port=update_credit_settings['port'],
                                     user=update_credit_settings['user'],
                                     password=update_credit_settings['password'], db=update_credit_settings['db'])

    user_data = origin_sql_connection.batch_lookup_sql(batch_size=1000)

    for batch in user_data:
        for item in batch:
            after_data = update(item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9],
            item[10], item[11], item[12])
            update_credit_connection.update_credit_sql(int(item[0]), after_data[0], after_data[1],
                                                   after_data[2], after_data[3], after_data[4], after_data[5])

run()