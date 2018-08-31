#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 13:59:42 2018

@author: juliaorenstein
"""

### Compile and run in spyder
### input data and noise files
### do not create fft files but graph ffts
### return noise cancelled data (maybe in a predetermined “subtracted” folder as you had before)
### graph raw voltage data vs noise cancelled data


import numpy as np
import matplotlib.pyplot as plt
import parameters
import glob

calibration_fac = 4*10**(-7)
locs = glob.glob('../Data/rawdata/2018_08_22*')
runs = []

for i in locs:
    runs.append(i[16:-4])


## run is in the form 'yyyy_mm_dd_#' with '_n' if applicable
## location is a path, MUST have a slash at the end

default_run = '2018_08_22_11' #w'yyyy_mm_dd'
default_noiserun = '2018_08_17_27_n'#'yyyy_mm_dd(_n)'
samplingfreq = 10000000.

datalocation = parameters.raw_data_location + default_run + '.txt'

#if you're gabe and this isn't working, go into my parameters.py file and change the locations so they work on your computer

print 'loading file: ' + default_run

data = np.array(list(open(datalocation, 'r')), dtype = float)

#########################################################
### USE plot_fft() TO PLOT A SINGLE FOURIER TRANSFORM ###
#########################################################

# runs fourier analysis on positional data
def fourier(run = default_run):
    
    if run != default_run:
        data = np.array(list(open('../Data/rawdata/2018_08_17_27_n.txt', 'r')), dtype = float)
    else:
        global data
    
    print 'running fourier analysis...'
    freq = np.fft.fftfreq(data.size, 1/samplingfreq)
    fft = np.fft.fft(data)
    return freq, fft

# plots it
def plot_fft(run = default_run, plot = True, window = None):
    filters = [(229000, 236000),(65400, 65500),(3.3*10**6, 3.35*10**6),(3.45*10**6, 3.5*10**6),(4.9*10**6, 5*10**6)]
    freq, fft = fourier(run)
    power = abs(fft)**2
    
    testffts = []
    
    for i, val in enumerate(fft):
        if abs(freq[i]) > 10**5:
            testffts.append(abs(val))
            
    l_bound = freq[testffts.index(max(testffts))]-150000
    u_bound = freq[testffts.index(max(testffts))]+500000
    
    filters.append((l_bound, u_bound))
    
    if plot == True:
                 
        plt.axvspan(l_bound, u_bound, alpha=0.25, color='red')
        for i in filters:
            plt.axvspan(i[0], i[1], alpha=0.25, color = 'red')
        
        plt.title('power spectrum: ' + run)
        plt.xlabel('frequency (Hz)')
        plt.xscale('log')
        plt.yscale('log')
        if window != None:         
            plt.xlim(window[0], window[1])
        plt.plot(freq, power, ',')
        plt.show()
    
    return filters
    
##################################################################################
### USE THIS TO COMPARE FFTS BEFORE AND AFTER NOISE CANCELING ####################
### TO MODIFY FILTERS, CHANGE VALUES IN THE filters VARIABLE #####################
##################################################################################
    
def filter_noise(run = default_run, noise = default_noiserun, plot = True):
    
    filters = plot_fft(run, plot = False) # ranges that will be filtered
    use_average = False # make this true if you're setting filtered values to some average instead of 0
    
    freq, fft = fourier(run)
    power = abs(fft)**2
    fftnew = np.array(fft)
    
    fft_noise = fourier(noise)[1]
    power_noise = abs(fft_noise)**2

    # average = TK
    print 'applying filters...'
    for i, val in enumerate(freq):
        # apply filters
        for pair in filters:
            if abs(val) > pair[0] and abs(val) < pair[1]:
                fftnew[i] = 0  
        if val == 0:
            fftnew[i] = 0
            #fftnew[i] = average #if we decide filters should use average value instead of 0
    #powernew = abs(fftnew)**2
     
    if plot:
        plt.figure(figsize = (10,10))
        plt.suptitle('Power spectra and positional data, before and after noise filtering', fontsize = 20)
    
        plt.subplot(221)
        plt.xlabel('Frequency (Hz)')
        plt.xscale('log')
        plt.yscale('log')
        plt.title('After')
        plt.plot(freq, power_noise, ',') 
        
        
        plt.subplot(222)
        for pair in filters:
            plt.axvspan(pair[0], pair[1], alpha=0.25, color='red')
        plt.xlabel('Frequency (Hz)')
        plt.xscale('log')
        plt.yscale('log')
        plt.ylabel('Power spectrum')
        plt.title('Before')
        plt.plot(freq, power, ',')
        
        window = 500
        t = np.arange(window)/samplingfreq
        fftnew = filter_noise(run, False)[0] #UH OH FIX THAT
        newdata = calibration_fac*np.fft.ifft(fftnew)
        
        plt.subplot(223)
        plt.xlabel('Time (s)')
        plt.ylabel('Positional data')
        plt.plot(t, data[1000:window+1000], lw = 1)
        
        plt.subplot(224)
        plt.xlabel('Time (s)')
        plt.plot(t, newdata[1000:window+1000], lw = 1)
        
        plt.show()
        
    return fftnew, filters, use_average

############################################################################
### USE THIS TO COMPARE POSITIONAL DATA BEFORE AND AFTER NOISE CANCELING ###
############################################################################

#change window size to view different zoom levels        
def compare_position(run = default_run, window = 10000):
    global data
    if run != default_run:
        data = np.array(list(open(parameters.raw_data_location + run + '.txt', 'r')), dtype = float) 
    
    fftnew = filter_noise(run, False)[0]
    
    print 'converting filtered fft data back to positional data...'
    t = np.arange(window)/samplingfreq
    newdata = np.fft.ifft(fftnew).real
    
    plt.title('comparing positional data before/after noise canceling: ' + run)
    plt.xlabel('time (s)')
    plt.ylabel('voltage (V)')
    plt.plot(t, data[:window], lw = 1)
    plt.plot(t, newdata[:window], lw =1)


###################################################################
### THIS WILL EXPORT THE FILTERED DATA TO THE FOLDER 'FILTERED' ###
### ALSO CUTS OFF FIRST AND LAST 200 POINTS (you can edit the #)###
### IT ALSO WRITES TO A NOTE 'filter_note.txt' WITH INFO ABOUT ####
### WHAT FFT VALUES WERE FILTERED OUT #############################
###################################################################
    
def export_filtered_data(run = default_run, border = 200):
    fftnew, filters, use_average = filter_noise(run, False)
    position = np.fft.ifft(fftnew).real[border: -border]
    filename = run + '_fil.txt'
    
    print 'writing the new filtered file...'
    
    with open(parameters.filtered_data_location + filename, 'w') as newfile:
        for i in position:
            newfile.write(str(i))
            newfile.write('\n')
    
    print 'updating note'
    
    with open(parameters.filtered_data_location + 'filter_note.txt', 'a') as note:
        note.write(run + ': ')
        if use_average:
            note.write('average')
        else: 
             note.write('zero')
        note.write('\n')
        note.write('border = ' + str(border))
        note.write('\n')
        for pair in filters:
            note.write(str(pair[0]) + ' - ' + str(pair[1]))
            note.write('\n')
        note.write('\n')
    
    
#####################################################################################################################
### THIS IS OUR OLD METHOD OF SUBTRACTED NOISE FILES FROM DATA FILES. PROBABLY WON'T NEED IT BUT JUST IN CASE #######
### INPUT DATARUN, NOISERUN, AND IF YOU WANT TO PLOT THE DIFFERENCE BETWEEN THE TWO AND SEE THE SUBTRACTED RESULT ###
### THEN SET PLOT = TRUE ############################################################################################
#####################################################################################################################

def subtract(datarun = default_run, noiserun = default_noiserun, plot = True):
    print 'subtracting noise from data fft.'
    freq, fft_data = fourier(datarun)
    fft_noise = fourier(noiserun)[1]

    subtracted = fft_data - fft_noise
     
    for i, val in enumerate(freq):
        # get rid of everything above a certain frequency (10^5) / get rid of everything above a certain fft value (10^3)
        if abs(val) > 10**5 or val == 0:
            subtracted[i] = 0

    if plot:
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

filter_noise()
