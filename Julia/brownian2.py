#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 15:09:20 2018

@author: juliaorenstein
"""

import numpy as np
import matplotlib.pyplot as plt

dates = ['2018_06_05_1', '2018_06_05_3', '2018_06_06_1', '2018_07_17_2', '2018_07_17_3', '2018_07_24_1', '2018_07_24_2']
filelocs = []
for i in dates:
    filelocs.append('../Data/' + i + '.txt')
  
databook = {}
for i in range(len(dates)):
    databook[dates[i]] = np.loadtxt(filelocs[i])

samplingfreq = 10000000.

# plot the raw data

def plotit(date):
    
    data = databook[date]
    
    plt.title('voltage data -- ' + date)
    plt.xlabel('time (s)')
    plt.ylabel('voltage difference (V)')
    plt.plot(np.arange(50000)/samplingfreq, data[:50000], ',')
    plt.show()
    
# calculate fourier transform

def fourier(date, plot = False):
    
    data = databook[date]
    
    fft = np.fft.fft(data)
    freq = np.fft.fftfreq(data.size, 1/samplingfreq)
    
    if plot == True:
        plt.figure
        plt.title('fourier transform -- ' + date)
        plt.xlabel('frequencies (Hz)')
        plt.xscale('log')
        plt.yscale('log')
        plt.plot(freq, abs(fft), ',')
        plt.show()
    
        
    return {'fft':fft, 'freq':freq}

def exportfft(date):
    
    filename = '/Users/juliaorenstein/GitHub/BrownianMotionExperiment/Data/ffts/' + date + '_fft.txt'
    newfile = open(filename, 'w')
    freq = fourier(date)['freq']
    fft = fourier(date)['fft']
    
    for i in range(len(freq)):
        newfile.write(str(freq[i]) + ' ' + str(fft[i].real) + ' ' + str(fft[i].imag))
        newfile.write('\n')
        
    newfile.close()

# get power spectrum        

def powerspectrum(date, plot = False):
    
    freq = fourier(date)['freq']
    fft = fourier(date)['fft']
    power = abs(fft) ** 2
    if plot == True:
        plt.title('power spectrum -- ' + date)
        plt.xlabel('frequencies (Hz)')
        plt.xlim(1000,5000)
        plt.xscale('log')
        plt.yscale('log')
        plt.plot(freq, power, ',')
        #plt.show()
        
    return power

#cancel noise in power spectrum

def noisecancel(date, plot = False):
    
    # current noise data
    noisefft = fourier('2018_06_05_3')['fft']
    noisefreq = fourier('2018_06_05_3')['freq']
    averagelist = []
    
    # whatever data we're evaluating
    datafft = fourier(date)['fft']
    datafreq = fourier(date)['freq']
    
    # datafreq and noise freq are only identical if the data is the same size -- not true for july data
    
    # plot original power spectrum
    if plot == True:
        plt.xscale('log')
        plt.yscale('log')
        plt.plot(datafreq, abs(datafft)**2, ',')
        #plt.plot(datafreq, datafft, ',')            
    
    
    # identify average value in area around peaks in june5 file
    averagelist = []
    
    for i, val in enumerate(noisefreq):
        if abs(val) > 5*10**3 and abs(val) < 10**4:
            averagelist.append(noisefft[i])
    
    average = np.mean(averagelist)
    
    for i, val in enumerate(datafreq):
        # get rid of everything above a certain frequency (10^5)
        if abs(val) > 10**5:
            datafft[i] = 0
        # get rid of everything above a certain fft value (10^4)
        if abs(datafft[i]) > 10**4:
            datafft[i] = 0
        # set known peaks to average value (NEEDS WORK)
        if abs(val) > 10**3.25 and abs(val) < 5*10**3:
            datafft[i] -= (noisefft[i/2] - average) ##### NEED TO MAKE NOISE DATA SIZE COMPATIBLE WITH REAL DATA SIZE

    
    
    if plot == True:
        plt.title('new power spectrum -- ' + date)
        plt.xlabel('frequencies (Hz)')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlim(10**3, 10**5)
        plt.plot(datafreq, abs(datafft)**2, ',')
        #plt.xlim(-10000, 10000)
        #plt.ylim(-100,100)
        #plt.plot(datafreq, datafft, ',')
        plt.show()

    
    return datafft
    
# now use new fourier to ifft back to positional data
    
def takeoutnoise(date, plot = False):
    
    newfft = noisecancel(date)
    newdata = np.fft.ifft(newfft)
    
    if plot == True:
        plt.title('clean voltage data -- ' + date)
        plt.xlabel('time (s)')
        plt.ylabel('voltage difference (V)')
        plt.plot(np.arange(50000)/samplingfreq, newdata[:50000].real, ',')
        
        plotit(date)
        
    return (newdata)
    
    
# export this new positional data into a file
def exportdata(date):
    filename = '../Data/newdata/' + date + '_nc.txt'
    newfile = open(filename, 'w')
    for val in takeoutnoise(date):
        newfile.write(str(val.real))
        newfile.write('\n')
    newfile.close()
# amplitude data
# noise cancel
# calibration factor (later)
# differentiate to find velocity
# fit to equipartition