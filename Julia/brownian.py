#!/usr/bin/env python2
# -*- coding: utf-8 -*- 
"""
Created on Wed Jun 13 14:02:36 2018

@author: juliaorenstein
"""

import numpy as np
import matplotlib.pyplot as plt

data1 = np.loadtxt("../Data/2018_06_05_3.txt")
data2 = np.loadtxt("../Data/2018_06_06_1.txt")
todaydata1 = np.loadtxt("../Data/2018_07_17_2.txt")
todaydata2 = np.loadtxt("../Data/2018_07_17_3.txt")

# create a timescale for data
sample = np.arange(2000128)
t = sample/10000000.

# plot trajectory
def traj(data):    
    plt.title("Position")
    plt.xlabel("Time (s)")
    plt.ylabel("Voltage difference (V)")
    plt.plot(t[:100000], data[:100000], linewidth = .5)
   

# create power spectrum
def power(data):
    
    #fourier y and x values, respectively
    fft = np.fft.fft(data)
    fftfreq = np.fft.fftfreq(data.size, 1/10000000.)
    
    # power spectrum equals fourier squared
    power = []
    for val in fft:
        power.append(abs(val)**2)
    
    #plot    
    plt.title("Power Spectrum")
    plt.xlabel("frequency (Hz)")
    plt.yscale("log")
    plt.xscale("log")
    ########    
    #plt.xlim(3.2*10**3,3.4*10**3)
    ########
    plt.plot(fftfreq, power, ',')
    
# get rid of noise
def noisecancel(data):
    
    fft = np.fft.fft(data)
    fftfreq = np.fft.fftfreq(data.size, 1/10000000.)

    # eliminates all frequences above 10^5
    for i,freq in enumerate(fftfreq):
        if abs(freq) > 10**5:
            fft[i] = 0
                    
        ##########
        if abs(freq) > 1.9*10**3 and abs(freq) < 2.1*10**3:
            fft[i] = 0
            
        if abs(freq) > 3.2*10**3 and abs(freq) < 3.4*10**3:
            fft[i] = 0
        ##########
        
    # eliminates all power spectrum values above 10^8 (all fft values about 10^4)
    for i,val in enumerate(fft):
        if abs(val) > 10**3.5:
            fft[i] = 0
    
    # plot new fourier tranforms before inverse-back
    
    #plt.plot(fftfreq, fft.real, ',')
    
    
    #inverse fourier transform to get back to original data minus noise
    newdata = np.fft.ifft(fft)
    
    return newdata

def calcvelocity(data):
    velocity = []
    position = abs(noisecancel(data))
    for i in (range(np.size(position)-1)):
        velocity.append((position[i+1]-position[i])*10000000)
        
    plt.plot(t[:10000], velocity[:10000], ',')
    print velocity[:10]
    print position[:10]        


def plotit():

    plt.figure(1, figsize = (15,10))
    
    # plot before noise cancellation (blue)
    plt.subplot(221)
    traj(data1)
    plt.subplot(223)
    traj(data2)    
    plt.subplot(222)
    power(data1)
    plt.subplot(224)
    power(data2)
    
    # plot after noise cancellation (orange)
    plt.subplot(221)
    traj(noisecancel(data1))
    plt.subplot(223)
    traj(noisecancel(data2))   
    plt.subplot(222)
    power(noisecancel(data1))
    plt.ylim(10**(-10),10**9)
    plt.subplot(224)
    power(noisecancel(data2))
    plt.ylim(10**(-10),10**9)
    plt.show()

