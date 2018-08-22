# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 11:07:21 2018

@author: alvar
"""

import filter_noise

files = []
for i in range(3):
    name = "2018_08_17_" + str(1+i)
    files.append(name)
    
for j in files:
    filter_noise.export_filtered_data(j)
    
