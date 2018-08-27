# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 09:54:36 2018

@author: alvar
"""

import matplotlib.pyplot as plt

files = {}
files.update({"harryNoise":"../data/rawdata/2018_06_05_3_n.txt","harryData":"../data/rawdata/2018_06_06_1.txt"})
#files.update({"ourNoise":"../data/rawdata/2018_07_17_2_n.txt","ourData":"../data/rawdata/2018_07_17_3.txt"})

#files.update({"7/30 data":"../data/rawdata/2018_07_30_20.txt","7/30 noise":"../data/rawdata/2018_07_30_26_n.txt"})
#files.update({"updated 7/30 data":"../data/rawdata/2018_07_30_28.txt","updated 7/30 noise":"../data/rawdata/2018_07_30_31_n.txt"})

#files.update({"pre noise cancellation":"../data/rawdata/2018_07_24_1.txt","noise cancelled":"../data/subtracted/2018_07_24_1_sub.txt"})

#files.update({"lights on":"../data/rawdata/2018_07_30_31_n.txt","lights off":"../data/rawdata/2018_07_30_32_n.txt"})

#files.update({"intensity noise on close PD":"../data/rawdata/2018_07_31_7_n.txt", "intensity noise on far PD":"../data/rawdata/2018_07_31_8_n.txt"})
#files.update({"beam blocked":"../data/rawdata/2018_07_31_9_n.txt"})
#files.update({"pointing noise, close PD covered":"../data/rawdata/2018_07_31_10_n.txt","pointing noise, far PD covered":"../data/rawdata/2018_07_31_11_n.txt"})
#files.update({"pointing noise, both PD illuminated":"../data/rawdata/2018_07_31_12_n.txt"})

#files.update({"7/31 data":"../data/rawdata/2018_07_31_13.txt"})

#files.update({"laser noise":"../data/rawdata/2018_08_01_1_n.txt"})

#files.update({"bead":"../data/rawdata/2018_08_16_3.txt"})
#files.update({"nc":"../data/filtered/2018_08_16_3_fil.txt"})
#files.update({"low power":"../data/rawdata/2018_08_16_5.txt"})

#files.update({"aligned":"../data/rawdata/2018_08_17_1.txt"})
"""
for i in range(5):
    name = "../Data/filtered/2018_08_17_" + str(13+i) + "_fil.txt"
    files.update({str(i+13):name})
   """ 
files.update({str(20):"../Data/rawdata/2018_08_17_27_n.txt"})
files.update({str(21):"../Data/filtered/2018_08_17_27_n_fil.txt"})

#for i in range(5):
 #   noise = "../Data/rawdata/2018_08_17_" + str(25+i) + "_n.txt"
  #  files.update({str(i+25):noise})
    
length = 200000
width = 10000
start = 200
t = range(0,width)
for i in files:
    input_file = open(files[i],"r")
    sample = []
    for lines in range(length):
        sample.append(float(input_file.readline()[:-1]))
    input_file.close()
    
    slicedSample = sample[start:start+width]
    #print sample
    plt.figure()
    plt.plot(t,slicedSample)
    plt.title(i)
