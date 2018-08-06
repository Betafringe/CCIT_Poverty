#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/12 18:49
# @Author  : Betafringe
# @Site    : 
# @File    : data.py
# @Software: PyCharm
import os
# import pymysql.cursors
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

    def batch_lookup_sql(self, batch_size=1000):
        '''

        :param batch_size:
        :return:
        '''

        if self.connect is None and self.connect.ping() is False:
            self.connectSQL()
        cur = self.connect.cursor(pymysql.cursors.SSCursor)
        # 执行sql语句
        try:
            cur.execute('select * from lead_poor')
            dataset = cur.fetchmany(batch_size)
        except (TypeError, pymysql.err.InternalError) as e:
            print(e)
        finally:
            pass

        while(dataset is not None and dataset != []):
            temp_list = []
            for item in dataset:
                origin_to_format_data = origin_data_to_format(item)
                temp_list.append(origin_to_format_data)
            # print("log yield")
            yield temp_list

            #print(type(dataset), dataset)
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

    def batch_insert_sql(self, id_, name_, score_, character_, appointment_, history_, stickiness_, relations_,
                         is_batch=True, batch_size=500, count_all_users=0):

        if self.connect is None or self.connect.ping() is False:
            self.conncetSQL()
        else:
            if self.cur is None:
                self.cur = self.connect.cursor()
            else:
                pass
        # SQL 插入语句
        sql = """INSERT INTO `credit_user_info` (`id`, `name`, `score`,`character`, `appointment`, `history`, 
                 `stickiness`, `relations`)VALUES (%d, \"%s\", %f, %f, %f, %f, %f, %f)""" % \
              (id_, name_, score_, character_, appointment_, history_, stickiness_, relations_)

        try:
            if self.cur is None:
                print("log info： cur is None ")
            else:
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
                            print(e)
                        finally:
                            pass
        except Exception as e:
            print(e, "log info")
        finally:
            pass


class UpdateCredit:
    def __init__(self):
        self.connect = None
        self.config = None

    def connectSQL(self, ip=None, port=None, user=None, password=None, db=None):
        if self.config is None:
            self.config = {
                'host': ip,
                'port': port,  # MySQL默认端口
                'user': user,  # mysql默认用户名
                'passwd': password,
                'db': db,  # 数据库
                'charset': 'utf8',  # 数据库编码
            }
        self.connect = pymysql.connect(**self.config)
        print('link update database successful!')  # log

    def update_credit_sql(self, id_, score_, character_, appointment_, history_, stickiness_, relations_):
        # 使用cursor()方法获取操作游标
        cur = self.connect.cursor()
        sql_update = """UPDATE `credit_user_info` SET `score` = %f, `character`= %f, `appointment`=%f, `history`=%f, 
                        `stickiness`=%f, `relations` = %f WHERE `id` = %d""" % (score_, character_, appointment_,
                                                                                history_, stickiness_, relations_, id_)
        if cur is None:
            cur = self.connect.cursor()
            # self.connect.autocommit(1)
        try:
            if cur is None:
                print("log info： cur is None ")
            else:
                cur.execute(sql_update)
                try:
                    self.connect.commit()
                except Exception as e:
                    self.connect.rollback()
                    print(e)
                finally:
                    pass
        except Exception as e:
            print(e)
        finally:
            pass


class DirectGetData:
    def handle_rawdata(self, is_list):
        if is_list is None:
            print('log data loss')
        else:
            try:
                user_info = origin_data_to_format(is_list)
            finally:
                pass
        return user_info

    def save_data(self):
        pass


def origin_data_to_format(single_data):

    def get_sex(x):
        if int(x) % 2 == 1:
            is_sex = 1
        else:
            is_sex = 0
        return is_sex

    def get_count(total):
        count = 0
        for index in total:
            if index is not None:
                count += 1
        return count

    id_ = single_data[0]

    name = single_data[1]

    count = get_count(single_data)

    per_num = single_data[2]
    if per_num is not None:
        per_num = per_num
    else:
        per_num = 1

    year = single_data[3]
    if year is not None and year.isdigit():
        year = int(year)
    else:
        year = datetime.datetime.now().year

    id_card = single_data[4].strip()
    if (type(id_card) is str) and (id_card[6:10].isdigit()) and (len(id_card) == 18 or 15):
        try:
            sex = get_sex(id_card[-2])
            age = datetime.datetime.now().year - int(id_card[6:10])
        except IndexError as e:
            print(e)
        finally:
            pass
    else:
        sex = 0
        age = 20

    lvl = single_data[5]
    if lvl is not None:
        lvl = lvl
    else:
        lvl = 0

    income = single_data[-9]
    if income is not None:
        income = income
    else:
        income = 800

    land_size = single_data[9]
    if land_size is not None:
        land_size = land_size
    else:
        land_size = 0

    sale_income = single_data[12]
    if land_size is not None:
        sale_income = sale_income
    else:
        sale_income = 0

    out_poverty = single_data[-7]
    if out_poverty is not None:
        out_poverty = out_poverty
    else:
        out_poverty = 0

    industrial_scale = single_data[-11]
    if industrial_scale is not None:
        industrial_scale = industrial_scale
    else:
        industrial_scale = 0

    kinds = single_data[-2]
    if kinds is not None:
        kinds = kinds
    else:
        kinds = '1'

    kinds_num = single_data[-1]
    if kinds_num is not None:
        kinds_num = kinds_num
    else:
        kinds_num = 0

    user_info_handle = (id_, name, per_num, year, age, income, lvl, count, sex, land_size, sale_income,
                             out_poverty, industrial_scale, kinds, kinds_num)
    return user_info_handle


'''
test function code
'''
# select_test = LookupSQL()
# select_test.connectSQL(ip='192.168.56.142', port=3306, user='poor', password='password_poor', db='initial')
# test = select_test.batch_lookup_sql(batch_size=100)
# for i in test:
#     print(i)
# insert_test = UpdateSQL()
# insert_test.connectSQL(ip='120.78.129.209', port=13306, user='test', password='test123456', db='CUser')
# insert_test.batch_insert_sql(12312, 'abcd', 299, 1, 1, 1, 1, 1)
testdata_list = [571526, 'abc', 2, '2016', '512927196902212917', '省级', '', '', '', '', '', '', '', '南充市 仪陇县 金城镇 罩板村', 511300000000, '南充市', 511324000000, '仪陇县', 511324100000, '金城镇', 511324100205, '罩板村', '', '', '', '', '2017', '', '', '', 0, '', '否', '', '', 0, 1, '', '', '', '']
directdata_test = DirectGetData()
directdata_test.handle_rawdata(testdata_list)