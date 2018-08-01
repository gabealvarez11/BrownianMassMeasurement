# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 15:15:59 2018

@author: alvar
"""

import numpy as np
import matplotlib.pyplot as plt

#load data
noiseData = np.loadtxt("../data/2018_06_05_3.txt")
trapData = np.loadtxt("../data/2018_06_06_1.txt")
dataLen = len(noiseData)
timeRange = np.arange(dataLen)

#plots input data
def plotData():
    plt.plot(timeRange[:1000], noiseData[:1000])
    plt.xlabel("time (100ns)") # 10^-7 s
    plt.ylabel("amplitude")
    plt.title("Noise")
    
    plt.figure()
    plt.plot(timeRange[:1000],trapData[:1000])
    plt.xlabel("time (100ns)")
    plt.ylabel("amplitude")
    plt.title("Signal")

#fourier tranforms
def fourierTransform(inputData):
    f = np.fft.fft(inputData)
    fourierFreq = np.fft.fftfreq(inputData.size, 1./10000000)
    return {"f": f, "freq":fourierFreq}
    
#finds power spectrum of data
def powerSpectrum(inputData, plot = True, label = "Power Spectrum"):
    fourier = fourierTransform(inputData)['f']
    fourierFreq = fourierTransform(inputData)['freq']
    powerSpec = np.abs(fourier)**2
    
    if (plot == True):
        plt.figure()
        plt.plot(fourierFreq,powerSpec, ",")
        plt.xscale("log")
        plt.yscale("log")
        plt.title(label)
        plt.xlabel("Frequency (Hz)")
        plt.ylabel("Fourier Transform")
    return powerSpec

#removes noise from signal
def noiseCancel(data, noise):
    average = np.average()
    
#finds calibration factor position/voltage
def calibrationFactor():
    return 1

#converts voltage to position (m)
def calibrate(inputData,calibrationFactor):
    return calibrationFactor * inputData

#calculates instantaneous velocity from position data
def velocity(pos,resolution):
    velocity = []
    for i in np.arange(resolution,dataLen-(resolution+1),resolution):
        velocity.append((pos[i+100]-pos[i])*100000)
    
    return velocity

#histogram of velocities
def velDistribution(velocities):
    return 0

#run things
   
print trapData[:100]
plotData()

#powerSpectrum(noiseData, True, "Noise Power Spectrum")
#powerSpectrum(trapData, True, "Signal Power Spectrum")
velocities = velocity(trapData,10)

plt.figure()
plt.plot(timeRange[:1000],velocities[:1000],"-")
