# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 11:07:21 2018

@author: alvar
"""

files = []
for i in range(5):
    name = "2018_08_17_" + str(13+i)
    files.append(name)
    
for j in files:
    export_filtered_data(j)
    
