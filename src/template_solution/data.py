#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 18:49
# @Author  : Betafringe
# @Site    : 
# @File    : data.py
# @Software: PyCharm
import os
import pymysql.cursors
import pymysql
import csv
import pandas as pd
import datetime


def connectSQL(ip, port, user, password, db, lookup_id):
    '''
    :param ip:
    :param port:
    :param user:
    :param password:
    :param db:
    :param lookup_id:
    :return:
    '''
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
        cur.execute('select * from lead_poor where id = ' + lookup_id)
        dataset = cur.fetchone()
    finally:
        cur.close()
        conn.close()
    print("connect server!")
    name = dataset[1]
    per_num = dataset[2]
    year = dataset[3]
    age = datetime.datetime.now().year - int(dataset[4][6:10])
    income = dataset[-9]
    args = []
    return name, per_num, year, age, income

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
