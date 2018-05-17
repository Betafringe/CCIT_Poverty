#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/3 21:32
# @Author  : Betafringe
# @Site    : 
# @File    : config.py
# @Software: PyCharm


def origin_sql_settings():
    origin_sql_args = {
        'ip': '172.16.254.71',
        'port': 3306,
        'user': 'fpjr',
        'password': '123456',
        'db': 'poor',
    }
    return origin_sql_args


def update_sql_settings():
    update_sql_args = {
        'ip': '172.16.254.71',
        'port': 3306,
        'user': 'fpjr',
        'password': '123456',
        'db': 'fpjr',
    }
    return update_sql_args


# test = origin_sql_settings()
# # print(test['ip'])