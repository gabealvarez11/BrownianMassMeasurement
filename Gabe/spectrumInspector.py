# -*- coding: utf-8 -*-
"""
Created on Thu Aug 02 15:45:30 2018

@author: alvar
"""

import numpy as np
import matplotlib.pyplot as plt

files = {}
#files.update({"around AOM but through trap, split onto both PDs":"../data/rawdata/2018_08_02_4_n.txt"})
#files.update({"with vacuum pump":"../data/rawdata/2018_08_02_2_n.txt","without vacuum pump":"../data/rawdata/2018_08_02_3_n.txt"})
files.update({"AOMs off":"../data/rawdata/2018_08_06_1_n.txt","AOMs on":"../data/rawdata/2018_08_06_2_n.txt"})

def fourier(data,samplingFreq):
    print 'running fourier analysis...'
    freq = np.fft.fftfreq(len(data), 1/samplingFreq)
    fft = np.fft.fft(data)
    return [freq, fft]

samplingFreq_ = 1e7
length = 1000000

t = range(0,length)
for i in files:
    input_file = open(files[i],"r")
    sample = []
    for lines in range(length):
        sample.append(float(input_file.readline()[:-1]))
    input_file.close()
    
    freq_, fft_ = fourier(sample,samplingFreq_)
    #plt.figure()
    plt.plot(freq_,np.power(np.abs(fft_),2),",",label=i)
    plt.title(i)
    plt.xlabel("frequency (Hz)")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()