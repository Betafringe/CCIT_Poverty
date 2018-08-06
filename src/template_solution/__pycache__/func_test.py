#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/17 12:20
# @Author  : Betafringe
# @Site    : 
# @File    : func_test.py
# @Software: PyCharm
import datetime


def get_sex(x):
    if int(x) % 2 == 1:
        is_sex = 1
    else:
        is_sex = 0
    return is_sex


def test(id_card):
    print(type(id_card) is str)
    print(id_card[6:10].isdigit())
    print(len(id_card) == 18 or 15)
    if (type(id_card) is str) and (id_card[6:10].isdigit()) and (len(id_card) == 18 or 15):
        try:
            print(len(id_card), "id_card length log info")
            sex = get_sex(id_card[-2])
            age = datetime.datetime.now().year - int(id_card[6:10])
        except IndexError as e:
            print(e)
        finally:
            pass
    else:
        sex = 0
        age = 20
    print(sex, age)
    return sex, age


a = "370502199408242412"
test(a)