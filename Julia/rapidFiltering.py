# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 11:07:21 2018

@author: alvar
"""

import filter_noise

files = []
for i in range(4):
    name = "2018_08_15_" + str(2+i)
    files.append(name)
    
for j in files:
    filter_noise.export_filtered_data(j)
    
