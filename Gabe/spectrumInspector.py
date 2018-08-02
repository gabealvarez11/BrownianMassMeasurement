# -*- coding: utf-8 -*-
"""
Created on Thu Aug 02 15:45:30 2018

@author: alvar
"""

import numpy as np
import matplotlib.pyplot as plt

files = {}
files.update({"around AOM but through trap, split onto both PDs":"../data/rawdata/2018_08_02_4_n.txt"})


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
    
    plt.plot(freq_,np.abs(fft_),",")
    plt.title(i)
    plt.xscale("log")
    plt.yscale("log")