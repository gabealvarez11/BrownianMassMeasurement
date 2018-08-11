#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 14:05:17 2018

@author: juliaorenstein
"""

import initializer.*
import parameters
import numpy as np
import matplotlib.pyplot as plt

###########################       
##### NOISE REDUCTION #####
###########################   

## plot
def plotffts(runs):
    fig, ax = plt.subplots(figsize = (10,5))
    ax.legend(markerscale = 10)  
    for i in runs:
        freq = fftdata[i][0].tolist()
        fft = fftdata[i][1]
        power = (abs(fft)**2).tolist()
        ax.plot(freq, power, ',', label = i)
        print
        print 'peaks in ' + i + ':'
        for j in power:
            if j > 10**8:
                print str(freq[power.index(j)]) + ', ' + str(j)            
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('frequency (Hz)')
    plt.xlim(1000, 5000)


# takes in a fourier spectrum of data and one of noise, subtracts the noise from the data
# also makes other noise adjustments (low-pass filter, eliminates 0-peak)
    
def subtract(datarun, noiserun = None, plot = False):
    if noiserun == None:
        noiserun = datarun + '_n'
    print 'subtracting noise from data fft...'
    freq = fftdata[noiserun][0]
    fft_noise = fftdata[noiserun][1]
    fft_data = fftdata[datarun][1]

    subtracted = fft_data - fft_noise
     
    for i, val in enumerate(freq):
        # get rid of everything above a certain frequency (10^5) / get rid of everything above a certain fft value (10^3)
        if abs(val) > 10**5 or val == 0:
            subtracted[i] = 0

    if plot == True:
        plt.figure(figsize = (10, 5))
        
        plt.subplot(121)
        plt.title(datarun)
        plt.plot(freq, abs(fft_noise)**2, ',')
        plt.plot(freq, abs(fft_data)**2, ',')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim(10**3, 10**4)
        plt.xlabel('frequency (Hz)')
        
        plt.subplot(122)
        plt.xlim(10**3, 10**4)
        plt.plot(freq, abs(subtracted)**2, ',')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('frequency (Hz)')
        
        plt.show()
    
    return subtracted

# inverse fourier transforms the noise reduced fourier spectrum

def position(datarun, noiserun = None, plot = False):
    if noiserun == None:
        noiserun = datarun + '_n'
    newdata = np.fft.ifft(subtract(datarun, noiserun))
    
    if plot == True:
###        plotdata(datarun)
        plt.plot(np.arange(window)/samplingfreq, newdata[:window], ',')
        plt.xlabel('time (s)')
        plt.ylabel('position')
        plt.title('noise-reduced position for ' + run)
        plt.show()
    
    return newdata

# exports noise-reduced positional data

def exportdata(datarun, noiserun = None):
    if noiserun == None:
        noiserun = datarun + '_n'
    print 'exporting noise reduced data'
    with open(parameters.subtracted_data_location + datarun + '_sub.txt', 'w') as newfile:
        for val in position(datarun, noiserun):
            newfile.write(str(val.real))
            newfile.write('\n')
 
    
# takes a run and noise reduces the data
# there should be an noise file associated with the raw data, with the form:
    # yyyy_mm_dd_#_n.txt
    
def executenoisereduction(run, noise = None):
    if noise == None:
        exportdata(run, run + '_n')
    else:
        exportdata(run, noise)

# plots old position versus new position
    
def plotcheck(run):
    
    position = np.array(list(open(parameters.subtracted_data_location + run + '_sub.txt', 'r')), dtype = float)
    plt.figure(figsize=(10,5))
    plt.title('positional data -- ' + run)
    plt.plot(np.arange(window)/samplingfreq, rawdatadict[run][:window], ',')
    plt.plot(np.arange(window)/samplingfreq, position[:window], ',')
    plt.xlabel('time (s)')
    plt.ylabel('position')
    
    