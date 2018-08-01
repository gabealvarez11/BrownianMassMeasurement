#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 13:40:15 2018

@author: juliaorenstein
"""

import numpy as np
import matplotlib.pyplot as plt

dates = ['2018_06_05_1', '2018_06_05_3', '2018_06_06_1', '2018_07_17_2', '2018_07_17_3', '2018_07_24_1', '2018_07_24_2']

lowerbound = -10
upperbound = 10



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
    
def plot(date):
    
    freq, fft = data(date)[0], data(date)[1]
        
    plt.plot(freq, fft, ',')
    #plt.xscale('log')
    #plt.yscale('log')
    plt.xlim(lowerbound, upperbound)
    plt.show()
    
def findpeaks(date):
    
    print 'peaks for ' + date
    
    freq, fft = data(date)[0], data(date)[1]
    power = abs(fft)**2
    
    # create list of running averages to identify when several dots are rising above normal values
    averages = []
    for i in range(len(freq)/5):
        averages.append(np.mean(power[5*i : 5*(i+1)]))
    
    # corresponding frequencies to averages list    
    newfreqs = []
    for i in range(len(freq)-5):
        if i%5 == 0:
            newfreqs.append(freq[i])
    
    # plot the new fft (should look like old one but less dense)   
    plt.plot(newfreqs, averages, ',')
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('frequency (Hz)')
    plt.title('averaged fft -- ')
    
    # now identify peaks by looking for dots that are a) above 10 and b) 5x greater that dots on either side    
    peaks = []
    peakfreqs = []
    for i, val in enumerate(averages):
        try:
            if val > 10 and val > 5*(averages[i+1]) and val > 5*(averages[i-1]):
                peaks.append(val)
                peakfreqs.append(newfreqs[i])
        except: IndexError
        
    '''for i in range(len(peaks)):
        print str(peakfreqs[i]) + ': ' + str(peaks[i])'''
        
    # plot the peaks to show what the code has found (should overlay other plots)
    
    plt.plot(peakfreqs, peaks, ',')
    plt.show()
    
    # now identify where the peaks start and end to the left and right
    
    
        