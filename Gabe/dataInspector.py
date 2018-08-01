# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 09:54:36 2018

@author: alvar
"""

import numpy as np
import matplotlib.pyplot as plt

files = {}
#files.update({"harryNoise":"../data/rawdata/2018_06_05_3_n.txt","harryData":"../data/rawdata/2018_06_06_1.txt"})
#files.update({"ourNoise":"../data/rawdata/2018_07_17_2_n.txt","ourData":"../data/rawdata/2018_07_17_3.txt"})

#files.update({"7/30 data":"../data/rawdata/2018_07_30_20.txt","7/30 noise":"../data/rawdata/2018_07_30_26_n.txt"})
#files.update({"updated 7/30 data":"../data/rawdata/2018_07_30_28.txt","updated 7/30 noise":"../data/rawdata/2018_07_30_31_n.txt"})

#files.update({"pre noise cancellation":"../data/rawdata/2018_07_24_1.txt","noise cancelled":"../data/subtracted/2018_07_24_1_sub.txt"})

#files.update({"lights on":"../data/rawdata/2018_07_30_31_n.txt","lights off":"../data/rawdata/2018_07_30_32_n.txt"})

files.update({"intensity noise on close PD":"../data/rawdata/2018_07_31_7_n.txt", "intensity noise on far PD":"../data/rawdata/2018_07_31_8_n.txt"})
#files.update({"beam blocked":"../data/rawdata/2018_07_31_9_n.txt"})
#files.update({"pointing noise, close PD covered":"../data/rawdata/2018_07_31_10_n.txt","pointing noise, far PD covered":"../data/rawdata/2018_07_31_11_n.txt"})
files.update({"pointing noise, both PD illuminated":"../data/rawdata/2018_07_31_12_n.txt"})

#files.update({"7/31 data":"../data/rawdata/2018_07_31_13.txt"})

files.update({"laser noise":"../data/rawdata/2018_08_01_1.txt"})
length = 100000

t = range(0,length)
for i in files:
    input_file = open(files[i],"r")
    sample = []
    for lines in range(length):
        sample.append(float(input_file.readline()[:-1]))
    input_file.close()
    
    #print sample
    plt.figure()
    plt.plot(t,sample,)
    plt.title(i)
