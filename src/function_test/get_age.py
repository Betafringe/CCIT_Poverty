#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 26/03/2018 21:21
# @Author  : Betafringe
# @Site    : 
# @File    : get_age.py
# @Software: PyCharm

def get_age_idcard(arguments):
    age = []
    for list in arguments:
        current_age = int(list[6:10])
        age.append(current_age)
    print(age)

def main():
        test_dict = ['51082319810726302x', '513027194301281223']
        get_age_idcard(test_dict)

if __name__ == '__main__':
    main()








