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

datalocs = glob.glob('../Data/rawdata/*.txt')
todaydata = glob.glob('../Data/rawdata/2018_07_30_*.txt')
noiselocs = glob.glob('../Data/rawdata/*_n.txt')
fouriers = glob.glob('../Data/ffts/*.txt')

runs = []
for i in datalocs:
    runs.append(i[16:-4])
    
noiseruns = []
for i in noiselocs:
    noiseruns.append(i[16:-4])

todayruns = []
for i in todaydata:
    todayruns.append(i[16:-4])
    
todaynoise = '2018_07_30_26_n'


noises = []
for i in noiselocs:
    noises.append(i[6:-4])
window = 10000
samplingfreq = 10000000.



################################
##### PREPARE ALL THE DATA #####
################################

## create a dictionary 'rawdata' that stores all the data. ##
## keys are of the form 'yyyy_mm_dd_#', with # indicating the run. ##
## all functions will call for 'run' which will be dictionary keys ##

def addentries():
    for run in runs:
        datalocation = '../Data/rawdata/' + run + '.txt'
        #noiselocation = '../Data/noise/' + run + '_n.txt'
        print
        print run
        tmpdata = np.array(list(open(datalocation, 'r')), dtype = float)
        rawdatadict[run] = np.array(tmpdata)
    

try: rawdatadict
except NameError:
    print 'creating raw data and noise dictionaries...'
    rawdatadict = {}
    #noisedict = {}
    for run in runs:
        datalocation = '../Data/rawdata/' + run + '.txt'
        #noiselocation = '../Data/noise/' + run + '_n.txt'
        print
        print run
        tmpdata = np.array(list(open(datalocation, 'r')), dtype = float)
        rawdatadict[run] = np.array(tmpdata)
        
        '''try:
            tmpnoise = np.array(list(open(noiselocation, 'r')), dtype = float)
            noisedict[run] = np.array(tmpnoise)  
        except IOError:
            print 'no associated noise file found'
            '''
        
        # address potential issue of forgetting a noise file for a certain data file
        
    print 'done!'

## create a dictionary 'fftdata' that stores all ffts. ##
## same key format as rawdatadict dictionary, format key: [freq, fft]

try: fftdata
except NameError: 
    print
    print 'creating fft data dictionary...'
    fftdata = {}
    ## fourier analysis of raw data, creates a dictionary entry in fftdata
    
    def fourier(run):
        print 'running fourier analysis...'
        data = rawdatadict[run]
        freq = np.fft.fftfreq(data.size, 1/samplingfreq)
        fft = np.fft.fft(data)
        
        fftdata[run] = [freq, fft]
        
    ## grabs dictionary entry and outputs a file with the form:
    ## frequency real_fft imaginary_fft    
    
    def exportfft(run):
        print 'exporting fft to file...'
        filename = '../Data/ffts/' + run + '_fft.txt'
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
        print
        print run + ':'
        filename = '../Data/ffts/' + run + '_fft.txt'
        if filename in fouriers:
            readfile(run)
            print
                         
        else:
            fourier(run)
            print 'ftt done'
            exportfft(run)
            print 'file created'
            
            
        
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

## identifies frequencies of peaks in ffts 
            
def findpeaks(run, plot = False):
    print 
    print 'peaks for ' + run
    
    freq = fftdata[run][0]
    fft = fftdata[run][1]

    power = abs(fft)**2
    
    # create list of running averages to identify when several dots are rising above normal values
    averages = []
    avebin = 20
    for i in range(len(freq)/avebin):
        averages.append(np.mean(power[avebin*i : avebin*(i+1)]))
    
    # corresponding frequencies to averages list    
    newfreqs = []
    for i in range(len(freq)-avebin):
        if i%avebin == 0:
            newfreqs.append(freq[i])
    
    # plot the new fft (should look like old one but less dense)
    if plot == True:
        plt.figure(figsize=(5,3))
        plt.plot(newfreqs, averages, ',')
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('frequency (Hz)')
        plt.title('averaged fft -- ' + run)

    
    # now identify peaks by looking for dots that are a) above 10 and b) 5x greater that dots on either side    
    peaks = []
    peakfreqs = []
    for i, val in enumerate(averages):
        try:
            if val > 10 and val > 10*(averages[i+1]) or val > 10*(averages[i-1]):
                peaks.append(val)
                peakfreqs.append(newfreqs[i])
        except: IndexError
        
    for i in range(len(peaks)):
        print str(peakfreqs[i]) + ': ' + str(peaks[i])
        
        
    # plot the peaks to show what the code has found (should overlay other plots)
    if plot == True:
        plt.plot(peakfreqs, peaks, '.')
        plt.show()
        
def altfindpeaks(run, plot = False):
    
    freq = fftdata[run][0]
    fft = fftdata[run][1]

    power = abs(fft)**2
    
    print
    print 'peaks for ' + run
    
    if plot == True:
        plt.plot(freq, power)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('frequency (Hz)')
        plt.title('peaks for ' + run)
    
    #intialpeaks = []
    #for i

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
    with open('../Data/subtracted/' + datarun + '_sub.txt', 'w') as newfile:
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
    
def plotcheck(run):
    
    position = np.array(list(open('../Data/subtracted/' + run + '_sub.txt', 'r')), dtype = float)
    plt.figure(figsize=(10,5))
    plt.title('positional data -- ' + run)
    plt.plot(np.arange(window)/samplingfreq, rawdatadict[run][:window], ',')
    plt.plot(np.arange(window)/samplingfreq, position[:window], ',')
    plt.xlabel('time (s)')
    plt.ylabel('position')
    
    