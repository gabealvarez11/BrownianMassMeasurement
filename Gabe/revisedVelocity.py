# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 13:29:00 2018

@author: alvar
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#sampling rate (Hz)
sampling = 10.**7

#number of desired data points
numDataPoints = 2000000

#desired temporal resolution for velocity data (s)
resolution = 5*10**(-6)

#bin count for velocity distribtion
binCount = 50

#defines boltzmann's constant
k = 1.38064852*10**(-23)

#assumes room temperature of 298K
def getkT():
    return k * 298

print "numDataPoints: ", numDataPoints
print "resolution: ", resolution, "s"
print "binCount: ", binCount

"""----------------------NEED TO COMPUTE---------------------------------------"""
#calibration factor obtained from curve fitting
calibrationFactor = 3.07540889088e-07

#import data
#input_file = open("../data/2018_06_06_1.txt","r") #harry data
input_file = open("../data/subtracted/2018_06_06_1_sub.txt","r")
voltData = []
for lines in range(numDataPoints):
    voltData.append(float(input_file.readline()[:-1]))
input_file.close()

#time axis in seconds
time = np.linspace(0,numDataPoints/sampling,numDataPoints,endpoint = False)

#time only in steps of resolution
#resolvedTime = np.linspace(resolution,numDataPoints/sampling-resolution,int(numDataPoints/(sampling*resolution))-1)

#removes first and last parts of time axis to match velocity calculations
velTime = time[int(np.ceil(resolution*sampling)):-(int(np.ceil(resolution*sampling)))] 

#converts voltage to position (m)
def calibrate(inputData,calibrationFactor):
    return np.dot(calibrationFactor,inputData)

#full position data
posData = calibrate(voltData,calibrationFactor)

""" ----------- end to end instead of small steps --------
#calculates instantaneous velocity (m/s) from calibrated position data (m) as a function of time (intervals of 1/sampling s)
#returns velocity (m/s) as a function of time (intervals of resolution)
def velocity(pos,resolution, sampling):   
    timeStep = int(np.ceil(resolution*sampling))
    
    velocity = []
    for i in np.arange(timeStep,len(pos)-(timeStep-1),timeStep):      
        firstHalf = np.average(pos[i-timeStep:i])
        secondHalf = np.average(pos[i:i+timeStep])
        
        velocityVal = (secondHalf - firstHalf)/resolution
        velocity.append(velocityVal)
    return velocity
"""

#calculates instantaneous velocity (m/s) from calibrated position data (m) as a function of time (intervals of 1/sampling s)
#returns velocity (m/s) as a function of time (intervals of resolution)
def velocity(pos,resolution, sampling):   
    timeStep = int(np.ceil(resolution*sampling))
    
    velocity = []
    for i in np.arange(timeStep,len(pos)-(timeStep),1):      
        firstHalf = np.average(pos[i-timeStep:i])
        secondHalf = np.average(pos[i:i+timeStep])
        
        velocityVal = (secondHalf - firstHalf)/resolution
        velocity.append(velocityVal)
    return velocity

vel = velocity(posData,resolution,sampling)

#returns speeds instead of velocities
def speed(pos,resolution,sampling):
    vel = velocity(pos,resolution,sampling)
    return np.absolute(vel)
 
#speed_ = speed(posData,resolution,sampling)

#graphs
plt.figure(1)
plt.title("Position")
plt.plot(time, posData)
plt.xlabel("Time (s)")
plt.ylabel("Displacement (m)")

plt.figure(2)
plt.title("Velocity")
plt.plot(velTime,vel)
plt.xlabel("Time (s)")
plt.ylabel("Instantaneous Velocity (m/s)")

"""
plt.figure(3)
plt.title("Speed")
plt.plot(resolvedTime,speed_)
plt.xlabel("Time (s)")
plt.ylabel("Speed (m/s)")
"""

#create histogram, returns centers of bin and associated probabilities
def distribution(velocities, binCount_,label):
    titles = [label + " Distribution", label + " (m/s)", "Normalized " + label + " Distribution"]
    plt.figure()
    plt.title(titles[0])
    plt.xlabel(titles[1])
    plt.ylabel("Number of Counts")
    n, bins, patches = plt.hist(velocities,bins=binCount_)
    
    binCenters = []
    prob = []
    numData = len(velocities)
    for j in range(len(bins)-1):
        binCenters.append((bins[j]+bins[j+1])/2)
        prob.append(n[j]/numData)
        
    plt.figure()
    plt.plot(binCenters,prob,".")
    plt.title(titles[2])
    plt.xlabel(titles[1])
    plt.ylabel("Probability")
    
    binWidth_ = binCenters[1]-binCenters[0]
    return prob, binCenters, binWidth_

vProb, vBins, vBinWidth = distribution(vel, binCount, "Velocity")
#sProb, sBins, sBinWidth = distribution(speed_,binCount, "Speed")

#gaussian distribution
def gaussian(x, a, mu, sig): 
    return a*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

#maxwell boltzmann velocity distribution in one dimension, takes mass in nanograms
def mbDist(v,m):
    kT = getkT()
    scaledM = float(np.dot(m,np.power(10.,-12)))
    dist = np.dot(np.divide(np.sqrt(scaledM),np.sqrt(2*np.pi*kT)),np.exp(np.dot(np.dot(scaledM,-1),np.power(v,2)/(2*kT))))
    return dist

params, cov = curve_fit(mbDist,vBins,vProb/vBinWidth,p0=(float(0.237)),bounds=(1e-4,10))
measuredMass = params[0]*10**(-12)
print "calculated mass: ", measuredMass, "kg"
    
plt.figure(4)
plt.plot(vBins,vBinWidth*mbDist(vBins,*params))