#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 18:49
# @Author  : Betafringe
# @Site    : 
# @File    : load_data.py
# @Software: PyCharm
import os
import pymysql.cursors
import pymysql
import csv
import pandas as pd

def connectSQL(ip, port, user, password, db):  # pass
    config = {
        'host': ip,
        'port': port,  # MySQL默认端口
        'user': user,  # mysql默认用户名
        'passwd': password,
        'db': db,  # 数据库
        'charset': 'utf8',
        # 'cursorclass': pymysql.cursors.DictCursor,
    }

    # 创建连接
    conn = pymysql.connect(**config)
    cur = conn.cursor()
    # 执行sql语句
    try:
        cur.execute('select * from user_info')
        dataset = cur.fetchall()
    finally:
        cur.close()
        conn.close()
    print(dataset)
    return dataset

def loadcsv(path):
    dataset = ()
    with open(path, 'r') as file:
        csv2file = csv.reader(file)
        for data_item in csv2file:
            dataset.append(data_item)
    return dataset

def load2pd(path):  # pass
    dataset = pd.read_csv(path)
    print("load csv as pandas dataframe successful!")
    # print(dataset)
    return dataset


# filename = '../../data/csv/preprocessing_data.csv'
# dataset = test.load2pd(filename)
# sql = test.connectSQL(ip='120.78.129.209', port=13306, user='test', password='test123456', db='CUser')
