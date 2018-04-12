#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/9 21:15
# @Author  : Betafringe
# @Site    : 
# @File    : cluster_test.py
# @Software: PyCharm

import numpy as np
from csv import reader
from sklearn.cluster import k_means
class Cluster:
    def __init__(self):
        pass

    def load_csv(self, filename):
        dataset = list()
        with open(filename, 'r') as file:
            csv_reader = reader(file)
            for row in csv_reader:
                if not row:
                    continue
                dataset.append(row)
        return dataset

    def spilt_data(self, dataset):
        para_pernum = []
        para_year = []
        para_age = []
        para_level = []
        para_villageid = []
        para_income = []
