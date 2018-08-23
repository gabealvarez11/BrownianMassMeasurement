#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 12:41:40 2018

@author: juliaorenstein
"""

import numpy as np

files = []
for loc in glob.glob('../Data/rawdata/2018_08_22*.txt'):
    name = loc[16:-4]
    files.append(name)

currents = []

with open('../Data/Note.txt') as note:
    for line in note:
        if '2018_08_22' in line:
            currents.append(line[line.index('A')-3:line.index('A')])