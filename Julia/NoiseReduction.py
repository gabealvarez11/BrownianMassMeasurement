#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 13:55:47 2018

@author: juliaorenstein
"""

import numpy as np
import matplotlib.pyplot as plt
import glob
import time

datalocs = glob.glob('../Data/201*.txt')
window = 50000
samplingfreq = 10000000


## create a dictionary 'rawdata' that stores all the data. ##
## keys are of the form 'yyyy_mm_dd_#', with # indicating the run. ##
## all functions will call for 'run' which will be dictionary keys ##

rawdata = {}

for location in datalocs:
    tmp = np.array(list(open(location, 'r')), dtype = float)
    rawdata[location[8:-4]] = np.array(tmp)

## plot raw data ##
 
def plotrawdata(run):
    data = rawdata[run]
    
    plt.title('voltage data -- ' + run)
    plt.xlabel('time (s)')
    plt.ylabel('voltage difference (V)')
    plt.plot(np.arange(window)/samplingfreq, data[:window], ',')
    plt.show()
    
def fouriertransform(run, plot = False):
    data = rawdata[run]
    
    fft = np.fft.fft(data)
    freq = np.fft.fftfreq(data.size, 1/samplingfreq)
    
    if plot == True:
        plt.title('fourier transform -- ' + run)
        plt.xlabel('frequencies (Hz)')
        plt.xscale('log')
        plt.yscale('log')
        plt.plot(freq, fft, ',')
        plt.show()
        
