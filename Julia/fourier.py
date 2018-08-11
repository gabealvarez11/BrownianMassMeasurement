#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 11:07:26 2018

@author: juliaorenstein
"""

import numpy as np
import parameters
import sys

## run is in the form 'yyyy_mm_dd_#' with '_n' if applicable
## location is a path, MUST have a slash at the end

run = sys.argv[1]
location = sys.argv[2]
samplingfreq = 10000000.


# takes in a fourier spectrum of data and one of noise, subtracts the noise from the data
# also makes other noise adjustments (low-pass filter, eliminates 0-peak)  

datalocation = parameters.raw_data_location + run + '.txt'

print 'loading file:'
print run

data = np.array(list(open(datalocation, 'r')), dtype = float)

# runs fourier analysis on positional data

def fourier(run):
    print 'running fourier analysis...'
    freq = np.fft.fftfreq(data.size, 1/samplingfreq)
    fft = np.fft.fft(data)
    return [freq, fft]

# input where you want the fourier data to end up
def exportfft(location_, run):
    freq = fourier(run)[0]
    fft = fourier(run)[1]
    print 'exporting fft to file...'
    filename = location + run + '_fft.txt'
    with open(filename, 'w') as newfile:
        for i in range(len(freq)):
            newfile.write(str(freq[i]) + ' ' + str(fft[i].real) + ' ' + str(fft[i].imag))
            newfile.write('\n')

exportfft(location, run)