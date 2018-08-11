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
import os.path
import time

datalocs = glob.glob(parameters.raw_data_location + '*.txt')
runs = []
for i in datalocs:
    runs.append(os.path.basename(i)[:-4])
    
noiseruns = []
for i in runs:
    if '_n' in i:
        noiseruns.append(i)
        
augustnoise = []
for i in noiseruns:
    if '08' in i:
        augustnoise.append(i)

fftdata = {}

def readfile(run):
    start = time.time()
    print 'reading file...'
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
    print time.time() - start
    
def makedata(run):
    start = time.time()
    print 'doing fft...'
    position = np.array(list(open(parameters.raw_data_location + run + '.txt', 'r')), dtype = float)
    fft = np.fft.fft(position)
    freq = np.fft.fftfreq(position.size, 1/parameters.sampling_freq)
    print time.time() - start
    fftdata[run] = freq, abs(fft)**2

## plot
def plotffts(runs):
    for i in runs:
        makedata(i)
        freq, power = fftdata[i]
        plt.plot(freq, power, ',')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('frequency (Hz)')
    #plt.xlim(1000, 4000)