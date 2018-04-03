#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 02/04/2018 16:56
# @Author  : Betafringe
# @Site    : 
# @File    : givemesomecredit.py
# @Software: PyCharm
import csv
import sys
import numpy as np
import pandas as pd
import pymysql.cursors
import pymysql
import pandas as pd

class ReadData():

    def __init__(self):
        pass


    def read_csv(self, filepath):
        dataset = ()
        with open(filepath, 'r') as file:
            csv2file = csv.reader(file)
            for data_item in csv2file:
                dataset.append(data_item)
        return dataset

    def read_sql(self, ip, port, user, root, password):
        # 连接配置信息
        config = {
            'host': ip,
            'port': port,  # MySQL默认端口
            'user': root,  # mysql默认用户名
            'password': password,
            'db': 'house',  # 数据库
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor,
        }

        # 创建连接
        con = pymysql.connect(**config)
        # 执行sql语句
        try:
            with con.cursor() as cursor:
                sql = "select * from community_view"
                cursor.execute(sql)
                dataset = cursor.fetchall()
        finally:
            con.close();
        return dataset

