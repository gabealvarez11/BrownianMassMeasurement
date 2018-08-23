# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 11:07:21 2018

@author: alvar
"""

import filter_noise
import glob

files = []
for loc in glob.glob('../Data/rawdata/2018_08_22*.txt'):
    name = loc[16:-4]
    files.append(name)
    
for j in files:
    filter_noise.export_filtered_data(j)
    
