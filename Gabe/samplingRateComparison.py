# -*- coding: utf-8 -*-
"""
Created on Thu Aug 09 14:36:43 2018

@author: alvar
"""
import numpy as np
import matplotlib.pyplot as plt

files = {}
#files.update({"data":"../data/rawdata/2018_08_09_1.txt","noise":"../data/rawdata/2018_08_09_2_n.txt"})
files.update({"10":"../data/rawdata/2018_08_09_3_n.txt","2":"../data/rawdata/2018_08_09_4_n.txt"})

def fourier(data,samplingFreq):
    print 'running fourier analysis...'
    freq = np.fft.fftfreq(len(data), 1/samplingFreq)
    fft = np.fft.fft(data)
    return [freq, fft]

samplingFreq_ = {"10":1e7,"2":2e6}
length = 4000128

t = range(0,length)
for i in files:
    input_file = open(files[i],"r")
    sample = []
    for lines in range(length):
        sample.append(float(input_file.readline()[:-1]))
    input_file.close()
    
    freq_, fft_ = fourier(sample,samplingFreq_[i])
    plt.figure()
    plt.plot(freq_,np.power(np.abs(fft_),2),",",label=i)
    plt.title(i)
    plt.xlabel("frequency (Hz)")
    plt.xscale("log")
    plt.yscale("log")
    plt.legend()