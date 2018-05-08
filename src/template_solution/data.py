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
import datetime
import config
'''
include LookupSQL and updateSQL class
'''


class LookupSQL:
    def __init__(self):
        self.connect = None
        self.config = None

    def connectSQL(self, ip=None, port=None, user=None, password=None, db=None):
        '''
        :param ip:
        :param port:
        :param user:
        :param password:
        :param db:
        :return:
        '''
        if self.config == None:
            self.config = {
            'host': ip,
            'port': port,  # MySQL默认端口
            'user': user,  # mysql默认用户名
            'passwd': password,
            'db': db,  # 数据库
            'charset': 'utf8',  #数据库编码
             }

        # 创建连接
        self.connect = pymysql.connect(**self.config)
        print('link target database successful!')

    def sql(self, lookup_id):
        '''

        :param lookup_id:
        :return: list
        '''
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
                if int(x) % 2 == 1:
                    is_sex = 1
                else:
                    is_sex = 0
                return is_sex

            sex = get_sex(dataset[4][-2])
            land_size = dataset[9]
            sale_income = dataset[12]
            out_poverty = dataset[-7]
            industrial_scale = dataset[-11]
            if land_size or sale_income or industrial_scale is None:
                land_size, sale_income, industrial_scale = 0, 0, 0
            else:
                land_size, sale_income, industrial_scale = 1, 1, 1
            print(name, per_num, year, age, income, lvl, count, sex,
                  land_size, sale_income, out_poverty, industrial_scale)
            return name, per_num, year, age, income, lvl, count, sex, land_size, sale_income, out_poverty, industrial_scale


    def batch_lookup_sql(self, batch_size=1000):
        '''

        :param lookup_id:
        :return: list
        '''


        if self.connect is None:
            self.connectSQL()
        cur = self.connect.cursor()
        # 执行sql语句
        try:
            cur.execute('select * from lead_poor ')
            dataset = cur.fetchmany(batch_size)
        except (TypeError, pymysql.err.InternalError) as e:
            print(e)
        finally:
            pass
        while(dataset is not None and dataset != ()):
            template_store_list = []
            for item in dataset:
                count = 0
                for index in item:
                    if index is not None:
                        count += 1
                id_ = item[0]
                name = item[1]
                per_num = item[2]
                year = item[3]
                age = datetime.datetime.now().year - int(item[4][6:10])
                income = item[-9]
                lvl = item[5]

                def get_sex(x):  # is_sex==0 女  is_sex==1 男
                    if int(x) % 2 == 1:
                        is_sex = 1
                    else:
                        is_sex = 0
                    return is_sex

                sex = get_sex(item[4][-2])
                land_size = item[9]
                sale_income = item[12]
                out_poverty = item[-7]
                industrial_scale = item[-11]
                if land_size or sale_income or industrial_scale is None:
                    land_size, sale_income, industrial_scale = 0, 0, 0
                else:
                    land_size, sale_income, industrial_scale = 1, 1, 1
                template_store_list.append((id_, name, per_num, year, age, income, lvl, count,
                                            sex, land_size, sale_income, out_poverty, industrial_scale))
                # print(name, per_num, year, age, income, lvl, count, sex,
                #       land_size, sale_income, out_poverty, industrial_scale)

            yield template_store_list
            dataset = cur.fetchmany(batch_size)
        pass


    def get_id(self):
        sql = 'select id from lead_poor'
        cur = self.connect.cursor()
        try:
            cur.execute(sql)
            data = cur.fetchall()
        except (TypeError, pymysql.err.InternalError) as e:
            print(e)
        return data

    def __del__(self):
        if self.connect is not None:
            self.connect.close()


class UpdateSQL:
    def __init__(self):
        self.connect = None
        self.config = None
        self.count = 0
        self.cur = None

    def connectSQL(self, ip=None, port=None, user=None, password=None, db=None):
        if self.config is None:
            self.config = {
            'host': ip,
            'port': port,  # MySQL默认端口
            'user': user,  # mysql默认用户名
            'passwd': password,
            'db': db,  # 数据库
            'charset': 'utf8',  #数据库编码
             }
        self.connect = pymysql.connect(**self.config)
        print('link update database successful!')  # log

    def insert_sql(self, id_, name_, score_, character_,
                   appointment_, history_, stickiness_, relations_, is_batch=True, batch_size=500):
        # SQL 插入语句
        sql = """INSERT INTO `credit_user_info` (`id`, `name`, `score`,`character`, `appointment`, `history`, 
                 `stickiness`, `relations`)VALUES (%d, \"%s\", %f, %f, %f, %f, %f, %f)""" % \
              (id_, name_, score_, character_, appointment_, history_, stickiness_, relations_)
        if self.cur is None:
            self.cur = self.connect.cursor()
            # self.connect.autocommit(1)
        try:
            self.cur.execute(sql)
            self.count += 1
            print(self.count)
            if is_batch:
                if self.count % batch_size == 0:
                # 提交到数据库执行
                    self.connect.commit()
                    # print("commit")
                else:
                    pass
        except Exception as e:
            # 如果发生错误则回滚
            print(e)
            self.connect.rollback()
            self.connect.close()

    def batch_insert_sql(self, id_, name_, score_, character_, appointment_, history_, stickiness_, relations_,
                         is_batch=True, batch_size=500, count_all_users=0):
        # SQL 插入语句
        sql = """INSERT INTO `credit_user_info` (`id`, `name`, `score`,`character`, `appointment`, `history`, 
                 `stickiness`, `relations`)VALUES (%d, \"%s\", %f, %f, %f, %f, %f, %f)""" % \
              (id_, name_, score_, character_, appointment_, history_, stickiness_, relations_)
        if self.cur is None:
            self.cur = self.connect.cursor()
            # self.connect.autocommit(1)
        try:
            self.cur.execute(sql)
            self.count += 1
            print(self.count)
            if is_batch:
                if self.count % batch_size == 0:
                # 提交到数据库执行
                    self.connect.commit()
                    print("commit")
                else:
                    # print("waiting to commit, hold")
                    if self.count >= count_all_users-batch_size:
                        try:
                            self.connect.commit()
                        except Exception as e:
                            self.connect.rollback()
                            self.connect.close
                        finally:
                            pass
        except Exception as e:
            # 如果发生错误则回滚
            print(e)
            self.connect.rollback()
            self.connect.close()



#
# '''
# test function code
# '''
# select_test = LookupSQL()
# select_test.connectSQL(ip='120.78.129.209', port=13306, user='test', password='test123456', db='CUser')
# test = select_test.batch_lookup_sql(batch_size=1000)
# print(test)
# for i in test:
#     print(i)
# # insert_test = UpdateSQL()
# # insert_test.connectSQL(ip='120.78.129.209', port=13306, user='test', password='test123456', db='CUser')
# # insert_test.insert_sql(1, 'abcd', 299, 1, 1, 1, 1, 1)
