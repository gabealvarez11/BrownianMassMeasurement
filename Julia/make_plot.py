#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 31 11:36:59 2018

@author: juliaorenstein
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.rcParams.update({'font.size': 15})


default_run = '2018_08_22_11' #w'yyyy_mm_dd'
default_noiserun = '2018_08_17_27_n'#'yyyy_mm_dd(_n)'
samplingfreq = 10000000.
calibration_fac = 4*10**(-7)

def fourier(run):
    
    data = np.array(list(open('../Data/rawdata/' + run + '.txt', 'r')), dtype = float)
    print 'running fourier analysis...'
    freq = np.fft.fftfreq(data.size, 1/samplingfreq)
    fft = np.fft.fft(data)
    return data, freq, fft

def calc_filters(run = default_run):
    filters = [(229000, 236000),(65400, 65500),(3.3*10**6, 3.35*10**6),(3.45*10**6, 3.5*10**6),(4.9*10**6, 5*10**6)]
    data, freq, fft = fourier(run)
    
    testffts = []
    
    for i, val in enumerate(fft):
        if abs(freq[i]) > 10**5:
            testffts.append(abs(val))
            
    l_bound = freq[testffts.index(max(testffts))]-150000
    u_bound = freq[testffts.index(max(testffts))]+500000
    
    filters.append((l_bound, u_bound))
    
    return filters, data, freq, fft

def filter_fft(run = default_run): 
    filters, data, freq, fft = calc_filters(run)
    fftnew = np.array(fft)
    for i, val in enumerate(freq):
        # apply filters
        for pair in filters:
            if abs(val) > pair[0] and abs(val) < pair[1]:
                fftnew[i] = 0  
        if val == 0:
            fftnew[i] = 0   
            
    return fftnew

def make_plot(run = default_run, noise = default_noiserun, plot = True):
    
    window = 500
    
    freq, fft_noise = fourier(default_noiserun)[1:]
    power_noise = abs(fft_noise)**2
    
    filters, data, freq, fft = calc_filters(run) # ranges that will be filtered
    power = abs(fft)**2
    
    fftnew = filter_fft(run)
    
    
    plt.figure(figsize = (12,12))
    plt.subplots_adjust(hspace = .25)
    plt.suptitle('Power spectra and positional data, before and after noise filtering', fontsize = 20)

    plt.subplot(221)
    plt.xlabel('Frequency (Hz)')   
    plt.ylabel('Power spectrum')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Power spectrum of noise')
    plt.plot(freq, power_noise, ',') 
    
    
    plt.subplot(222)
    for pair in filters:
        plt.axvspan(pair[0], pair[1], alpha=0.25, color='red')
    plt.xlabel('Frequency (Hz)')
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Power spectrum of data')
    plt.plot(freq, power, ',')
    
    window = 500
    t = np.arange(window)*1000/samplingfreq
    
    data = calibration_fac*(10**9)*data
    new_data = calibration_fac*(10**9)*np.fft.ifft(fftnew)
    
    plt.subplot(223)
    plt.xlabel('Time (ms)')
    plt.ylabel('Position (nm)')
    plt.title('Position before filtering')
    plt.plot(t, data[1000:window+1000], lw = 1)
    
    plt.subplot(224)
    plt.xlabel('Time (ms)')
    plt.title('Position after filtering')
    plt.plot(t, new_data[1000:window+1000], lw = 1)
    
    plt.show()
    
    

    