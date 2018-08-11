#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 10:13:59 2018

@author: juliaorenstein
"""

import numpy as np
import parameters
import sys


#input the names of
    #1: a data run of the form 'yyyy_mm_dd'
    #2: a noise run of the form 'yyyy_mm_dd_n'

datarun = sys.argv[1]
noiserun = sys.argv[2]
location = sys.argv[3]
samplingfreq = 10000000.

# takes in a fourier spectrum of data and one of noise, subtracts the noise from the data
# also makes other noise adjustments (low-pass filter, eliminates 0-peak)  

datalocation = parameters.raw_data_location + datarun + '.txt'
noiselocation = parameters.raw_data_location + noiserun + '.txt'

print 'loading data and noise files:'
print datarun
print noiserun

data = np.array(list(open(datalocation, 'r')), dtype = float)
noise = np.array(list(open(noiselocation, 'r')), dtype = float)

book = {datarun: data, noiserun: noise}
# runs fourier analysis on positional data

fftdata = {}

def fourier(run):
    print 'running fourier analysis...'
    freq = np.fft.fftfreq(book[run].size, 1/samplingfreq)
    fft = np.fft.fft(book[run])
    fftdata[run] = [freq, fft]
    
# input where you want the fourier data to end up
def exportfft(location_, run):
    print 'exporting fft to file...'
    if location_[-1] is not '/':
        location_.append('/')
    filename = location + run + '_fft.txt'
    with open(filename, 'w') as newfile:
        for i in range(len(fftdata[run][0])):
            newfile.write(str(fftdata[run][0][i]) + ' ' + str(fftdata[run][1][i].real) + ' ' + str(fftdata[run][1][i].imag))
            newfile.write('\n')

exportfft(location, datarun)
exportfft(location, noiserun)

# does the subtraction
def subtract(data_, noise_):
    print
    print 'subtracting noise from data fft...'
    freq = fftdata[noiserun][0]
    fft_noise = fftdata[noiserun][1]
    fft_data = fftdata[datarun][1]

    subtracted = fft_data - fft_noise
    
    for i, val in enumerate(freq):
        # get rid of everything above a certain frequency (10^5) / get rid of everything above a certain fft value (10^3)
        if abs(val) > 10**5 or val == 0:
            subtracted[i] = 0

    return subtracted

# inverse fourier transforms the noise reduced fourier spectrum

def position(data_, noise_):
    newdata = np.fft.ifft(subtract(data_, noise_))
    return newdata

# exports noise-reduced positional data

def exportdata(data_, noise_):
    print 'exporting noise reduced data'
    with open(parameters.subtracted_data_location + data_ + '_sub.txt', 'w') as newfile:
        for val in position(data_, noise_):
            newfile.write(str(val.real))
            newfile.write('\n')
            
exportdata(datarun, noiserun)
 
    

