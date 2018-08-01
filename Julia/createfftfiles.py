#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 13:55:47 2018

@author: juliaorenstein
"""

## crashed spyder and lost code, oops
## i wrote a thing that would add fft data to a dictionary
## would read it from the file if it exists
## would create file if it doesn't already exist

import numpy as np
import matplotlib.pyplot as plt
import glob

datalocs = glob.glob('../Data/201*.txt')
fouriers = glob.glob('../Data/ffts/*.txt')
runs = []
for i in datalocs:
    runs.append(i[8:-4])
window = 50000
samplingfreq = 10000000.


## create a dictionary 'rawdata' that stores all the data. ##
## keys are of the form 'yyyy_mm_dd_#', with # indicating the run. ##
## all functions will call for 'run' which will be dictionary keys ##
try: rawdata
except NameError:
    
    rawdata = {}
    def datadict():
        for location in datalocs:
            tmp = np.array(list(open(location, 'r')), dtype = float)
            rawdata[location[8:-4]] = np.array(tmp)
    
    datadict()

## create a dictionary 'fftdata' that stores all ffts. ##
## same key format as rawdata dictionary, format key: [freq, fft]

fftdata = {}

## fourier analysis of raw data, creates a dictionary entry in fftdata

def fourier(run):
    data = rawdata[run]
    freq = np.fft.fftfreq(data.size, 1/samplingfreq)
    fft = np.fft.fft(data)
    
    fftdata[run] = [freq, fft]
    
## grabs dictionary entry and outputs a file with the form:
## frequency real_fft imaginary_fft    

def exportfft(run):
    
    filename = '../Data/ffts/' + run + '_fft.txt'
    with open(filename, 'w') as newfile:
        for i in range(len(fftdata[run][0])):
            newfile.write(str(fftdata[run][0][i]) + ' ' + str(fftdata[run][1][i].real) + ' ' + str(fftdata[run][1][i].imag))
            newfile.write('\n')

## reads fourier file and puts it into dictionary
            
def readfile(run):
    freqtmp = []
    fftrealtmp = []
    fftimagtmp = []
    with open('../Data/ffts/' + run + '_fft.txt') as ffttext:
        for line in ffttext:
            freqtmp.append(float(line.split()[0]))
            fftrealtmp.append(float(line.split()[1]))
            fftimagtmp.append(float(line.split()[2]))
    
    fftcomplex = [complex(fftrealtmp[i], fftimagtmp[i]) for i in range(len(fftrealtmp))]
    fft = np.array(fftcomplex)
    freq = np.array(freqtmp)
    
     
    fftdata[run] = [freq, fft]   
    
## the following will add entries to the fftdata dictionary
## if the fft file exists already, it reads it out from there
## if it does not exist, it will create it

for run in runs:
    print run + ':'
    filename = '../Data/ffts/' + run + '_fft.txt'
    if filename in fouriers:
        print 'reading file into dictionary'
        readfile(run)
        print
                     
    else:
        print 'creating file...'
        fourier(run)
        print 'ftt done'
        exportfft(run)
        print 'file created'
        print
        
        
## ftt the data, export it to file for later use ##
    


## runs exportfft only if the file does not yet exist ##
'''
for item in datalocs:
    run = item[8:-4]
    if '../Data/ffts/' + run + '_fft.txt' not in fouriers:
        exportfft(run)
        

##
'''