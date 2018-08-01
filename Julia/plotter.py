#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 11:03:59 2018

@author: juliaorenstein
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 09:54:36 2018

@author: alvar
"""
import numpy as np
import matplotlib.pyplot as plt

dates = ['2018_06_05_1', '2018_06_05_3', '2018_06_06_1', '2018_07_17_2', '2018_07_17_3', '2018_07_24_1', '2018_07_24_2']

length = 50000
samplingfreq = 10000000.
t = np.arange(0,length)/samplingfreq
def plotter(date):
    input_file = open('../Data/newdata/' + date + '_nc.txt', "r")
    sample = []
    for lines in range(length):
        sample.append(float(input_file.readline()[:-1]))
    input_file.close()
    
    #print sample
    plt.figure()
    plt.plot(t,sample)
    plt.title(date)
