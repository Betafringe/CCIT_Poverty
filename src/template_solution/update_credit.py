#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/8 20:25
# @Author  : Betafringe
# @Site    : 
# @File    : update_credit.py
# @Software: PyCharm
import pymysql.cursors
import pymysql
from analyse import update
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
                                                                                history_,stickiness_, relations_, id_)


        try:
            cur.execute(sql_update)  # 像sql语句传递参数
            print(cur.execute(sql_update))
            self.connect.commit()
        except Exception as e:
            print(e)
            # 错误回滚
            self.connect.rollback()
        finally:
            self.connect.close()
def run():
    update_instance = UpdateCredit
    update_instance.connectSQL()
