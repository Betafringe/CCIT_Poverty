#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 02/04/2018 09:07
# @Author  : Betafringe
# @Site    : 
# @File    : Randomforest.py
# @Software: PyCharm

from random import seed
from random import randrange
import math
import pandas as pd
import numpy as np
from csv import reader


class RandomForestClassifier:
    def __init__(self):
        pass

    # Load a CSV file
    def load_csv(self, filename):
        dataset = list()
        csv_reader = reader(open(filename, encoding='utf-8'))
        for row in csv_reader:
            if not row:
                continue
            dataset.append(row)
        return dataset

    # Convert string column to float
    def str_column_to_float(self, dataset, column):
        for row in dataset:
            row[column] = float(row[column].strip())

    # Convert string column to integer
    def str_column_to_int(self, dataset, column):
        class_values = [row[column] for row in dataset]
        unique = set(class_values)
        lookup = dict()
        for i, value in enumerate(unique):
            lookup[value] = i
        for row in dataset:
            row[column] = lookup[row[column]]
        return lookup

