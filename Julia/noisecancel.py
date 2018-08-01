#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 11:19:13 2018

@author: juliaorenstein
"""

# when back from lunch
    # create dictionaries!!

import numpy as np
import matplotlib.pyplot as plt

samplingfreq = 10000000.
window = 5000

dates = ['2018_06_05_1', '2018_06_05_3', '2018_06_06_1', '2018_07_17_2', '2018_07_17_3', '2018_07_24_1', '2018_07_24_2']


def plotdata(date):
    
    data = np.loadtxt('../Data/' + date + '.txt')
    
    plt.title('voltage data -- ' + date)
    plt.xlabel('time (s)')
    plt.ylabel('voltage difference (V)')
    plt.plot(np.arange(window)/samplingfreq, data[:window], ',')

def data(date):
    inputdata = np.loadtxt('../Data/ffts/' + date + '_fft.txt')
    freqs = []
    ffts = []
    
    for i in inputdata:
        freqs.append(i[0])
        ffts.append(complex(i[1], i[2]))
        
    freq = np.array(freqs)
    fft = np.array(ffts)
    
    return [freq, fft]
    
def plotfft(date):
    
    freq, fft = data(date)[0], data(date)[1]
        
    plt.plot(freq, abs(fft)**2, ',')
    plt.xscale('log')
    plt.yscale('log')
    #plt.xlim(lowerbound, upperbound)
    plt.show()
 
    
# new idea: what if we just subtract entire noise fft from data fft?
    
def subtract(datadate, noisedate, plot = False): # for now, only works for 06 05 noise and 06 06 data / attempting for 07 24 data
    
    freq = data(noisedate)[0]
    fftdata = data(datadate)[1]
    fftnoise = data(noisedate)[1]
        
    
    subtracted = fftdata - fftnoise
     
    for i, val in enumerate(freq):
        # get rid of everything above a certain frequency (10^5) / get rid of everything above a certain fft value (10^3)
        if abs(val) > 10**5 or val == 0 or abs(subtracted[i]) > 10**3:
            subtracted[i] = 0

    
    if plot == True:
        
        plt.plot(data(datadate)[0], subtracted, ',')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('frequency (Hz)')
        plt.show()
    
    return subtracted
    
def position(datadate, noisedate, plot = False):
    
    newdata = np.fft.ifft(subtract(datadate, noisedate))
    
    if plot == True:
        plotdata(datadate)
        plt.plot(np.arange(window)/samplingfreq, newdata[:window], ',')
        plt.xlabel('time (s)')
        plt.ylabel('position')
        plt.show()
    
    return newdata

def exportdata(datadate, noisedate): # only june 6 and july 24 for now
    filename = '../Data/subtracted/' + datadate + '_sub.txt'
    newfile = open(filename, 'w')
    for val in position(datadate, noisedate):
        newfile.write(str(val.real))
        newfile.write('\n')
    newfile.close()
    