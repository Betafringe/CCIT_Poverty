#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/3 21:32
# @Author  : Betafringe
# @Site    : 
# @File    : config.py
# @Software: PyCharm


def origin_sql_settings():
    origin_sql_args = {
        'ip': '120.78.129.209',
        'port': 13306,
        'user': 'test',
        'password': 'test123456',
        'db': 'CUser',
    }
    return origin_sql_args


def update_sql_settings():
    update_sql_args = {
        'ip': '120.78.129.209',
        'port': 13306,
        'user': 'test',
        'password': 'test123456',
        'db': 'CUser',
    }
    return update_sql_args


# test = origin_sql_settings()
# # print(test['ip'])