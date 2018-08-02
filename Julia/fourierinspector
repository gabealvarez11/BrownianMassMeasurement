#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 14:27:36 2018

@author: juliaorenstein
"""
import numpy as np
import matplotlib.pyplot as plt
import parameters
import glob

datalocs = glob.glob(parameters.raw_data_location + '*.txt')
runs = []
for i in datalocs:
    runs.append(i[67:-4])
    
noiseruns = []
for i in runs:
    if '_n' in i:
        noiseruns.append(i)
 
fftdata = {}

def readfile(run):
    print 'reading file into dictionary...'
    freqtmp = []
    fftrealtmp = []
    fftimagtmp = []
    with open(parameters.fft_data_location + run + '_fft.txt') as ffttext:
        print ffttext
        for line in ffttext:
            freqtmp.append(float(line.split()[0]))
            fftrealtmp.append(float(line.split()[1]))
            fftimagtmp.append(float(line.split()[2]))
    
    fftcomplex = [complex(fftrealtmp[i], fftimagtmp[i]) for i in range(len(fftrealtmp))]
    fft = np.array(fftcomplex)
    freq = np.array(freqtmp)
    
     
    fftdata[run] = [freq, fft]    

## plot
def plotffts(runs):
    for i in runs:
        readfile(i)
    fig, ax = plt.subplots(figsize = (10,5))
    ax.legend(markerscale = 10)  
    for i in runs:
        freq = fftdata[i][0].tolist()
        fft = fftdata[i][1]
        power = (abs(fft)**2).tolist()
        ax.plot(freq, power, ',', label = i)
        print
        print 'peaks in ' + i + ':'
        j = max(power[1:-1])
        print str(freq[power.index(j)]) + 'Hz, ' + str(j)            
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('frequency (Hz)')