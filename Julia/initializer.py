#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 13:55:47 2018

@author: juliaorenstein
"""

import numpy as np
import glob
import parameters

datalocs = glob.glob(parameters.raw_data_location + '*.txt')
fouriers = glob.glob(parameters.fft_data_location + '*.txt')

runs = []
for i in datalocs:
    runs.append(i[66:-4])

noises = []
window = 10000
samplingfreq = 10000000.

################################
##### PREPARE ALL THE DATA #####
################################

## create a dictionary 'rawdata' that stores all the data. ##
## keys are of the form 'yyyy_mm_dd_#', with # indicating the run. ##
## all functions will call for 'run' which will be dictionary keys ##

try: rawdatadict
except NameError: 
    print 'creating raw data dictionary'
    rawdatadict = {}
finally:
    for run in runs:
        if run not in rawdatadict.keys():
            datalocation = parameters.raw_data_location + run + '.txt'
            print 'new entry: ' + run
            tmpdata = np.array(list(open(datalocation, 'r')), dtype = float)
            rawdatadict[run] = np.array(tmpdata)
        
    print 'done!'

## create a dictionary 'fftdata' that stores all ffts. ##
## same key format as rawdatadict dictionary, format key: [freq, fft]


try: fftdata
except NameError: 
    fftdata = {}
finally:
    
    ## runs fft on positional data
    
    def fourier(run):
        position = rawdatadict[run]
        freq = np.fft.fftfreq(position.size, 1/parameters.sampling_freq)
        fft = np.fft.fft(position)
        fftdata[run] = [freq,fft]
    
    ## grabs dictionary entry and outputs a file with the form:
    ## frequency real_fft imaginary_fft    
    
    def exportfft(run):
        print 'exporting fft to file...'
        filename = parameters.fft_data_location + run + '_fft.txt'
        with open(filename, 'w') as newfile:
            for i in range(len(fftdata[run][0])):
                newfile.write(str(fftdata[run][0][i]) + ' ' + str(fftdata[run][1][i].real) + ' ' + str(fftdata[run][1][i].imag))
                newfile.write('\n')
    
    ## reads fourier file and puts it into dictionary
                
    def readfile(run):
        print 'reading file into dictionary...'
        freqtmp = []
        fftrealtmp = []
        fftimagtmp = []
        with open(parameters.fft_data_location + run + '_fft.txt') as ffttext:
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
        print
        print run + ':'
        filename = parameters.fft_data_location + run + '_fft.txt'
        if filename in fouriers:
            readfile(run)
            print
                         
        else:
            fourier(run)
            print 'fft done'
            exportfft(run)
            print 'file created'
        

