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


class SQL:
    def __init__(self):
        self.connect = None
        self.config=None

    def connectSQL(self, ip=None, port=None, user=None, password=None, db=None):
        '''
        :param ip:
        :param port:
        :param user:
        :param password:
        :param db:
        :return:
        '''
        if self.config==None:
            self.config = {
            'host': ip,
            'port': port,  # MySQL默认端口
            'user': user,  # mysql默认用户名
            'passwd': password,
            'db': db,  # 数据库
            'charset': 'utf8', #数据库编码
            # 'cursorclass': pymysql.cursors.DictCursor,
             }

        # 创建连接
        self.connect = pymysql.connect(**self.config)

    def sql(self, lookup_id):
        if self.connect is None:
            self.connectSQL()
        cur = self.connect.cursor()
        # 执行sql语句
        try:
            cur.execute('select * from lead_poor where id = ' + lookup_id)
            dataset = cur.fetchone()
        except (TypeError, pymysql.err.InternalError) as e:
            print(e)
        finally:
             cur.close()
        #     conn.close()
        #print("connect server!")
        if dataset is None:
            print("错误ID")
        else:
            count = 0
            for index in dataset:
                if index is not None:
                    count += 1
            name = dataset[1]
            per_num = dataset[2]
            year = dataset[3]
            age = datetime.datetime.now().year - int(dataset[4][6:10])
            income = dataset[-9]
            lvl = dataset[5]

            def get_sex(x):  # is_sex==0 女  is_sex==1 男
                if x == "X" or "x":
                    is_sex = 1
                elif int(x) % 2 == 0:
                    is_sex = 1
                else:
                    is_sex = 0
                return is_sex

            sex = get_sex(dataset[4][-1])
            landsize = dataset[9]
            sale_income = dataset[12]
            out_poverty = dataset[-7]
            industrial_scale = dataset[-11]
            # print(name, per_num, year, age, income, lvl, count, sex, landsize, sale_income, out_poverty)
            if landsize or sale_income or industrial_scale is None:
                landsize, sale_income, industrial_scale = 0, 0, 0
            else:
                landsize, sale_income, industrial_scale = 1, 1, 1
            # print(name, per_num, year, age, income, lvl, count, sex, landsize, sale_income, out_poverty)
            return name, per_num, year, age, income, lvl, count, sex, landsize, sale_income, out_poverty, industrial_scale

    def insert_sql(self, id_, name_, score_, character_, appointment_, history_, stickiness_, relations_):
        # SQL 插入语句
        sql = """INSERT INTO `credit_user_info` (`id`,
                 `name`, `score`,`character`, `appointment`, `history`, `stickiness`, `relations`)
                 VALUES (%d, \"%s\", %f, %f, %f, %f, %f, %f)""" % (id_, name_, score_, character_, appointment_,
                                                                   history_, stickiness_, relations_)
        cur = self.connect.cursor()

        try:
            print(cur.execute(sql))
            # 提交到数据库执行
            self.connect.commit()
        except Exception as e:
            # 如果发生错误则回滚
            print(e)
            self.connect.rollback()

        # 关闭数据库连接
            #self.connect.close()

    def get_id(self):
        id_list = []
        sql = 'select id from lead_poor'
        cur = self.connect.cursor()
        try:
            cur.execute(sql)
            data = cur.fetchall()
        except (TypeError, pymysql.err.InternalError) as e:
            print(e)
        finally:
             pass
        return data

    def loadcsv(self, path):
        dataset = ()
        with open(path, 'r') as file:
            csv2file = csv.reader(file)
            for data_item in csv2file:
                dataset.append(data_item)
        return dataset

    def load2pd(self, path):  # pass
        dataset = pd.read_csv(path)
        return dataset

    def __del__(self):
        if self.connect is not None:
            self.connect.close()


sql = SQL()
sql.connectSQL(ip='120.78.129.209', port=13306, user='test', password='test123456', db='CUser')
sql.get_id()

