# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 16:28:27 2018

@author: alvar
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

#expected mass (kg) of microsphere of associated diameter (m)
def expectedMass(diameter):
    density = 2000 #kg/m^3
    return density*4./3*np.pi*np.power(diameter / 2, 3)

#sampling rate (Hz)
sampling = 10.**7

#number of desired data points
numDataPoints = 2000000

#desired temporal resolution for velocity data (s)
resolution = 5*10**(-6)

#bin count for velocity distribtion
binCount = 25

#defines boltzmann's constant
k = 1.38064852*10**(-23)

#assumes room temperature of 298K
def getkT():
    return k * 298

#print "numDataPoints: ", numDataPoints
#print "resolution: ", resolution, "s"
#print "binCount: ", binCount


#import data
input_file = open("../data/2018_06_06_1.txt","r") #harry data
#input_file = open("../data/2018_07_17_3.txt","r") #our data
#input_file = open("../data/newdata/2018_06_06_1_nc.txt","r") # nc
voltData = []
for lines in range(numDataPoints):
    voltData.append(float(input_file.readline()[:-1]))
input_file.close()

#time axis in seconds
time = np.linspace(0,numDataPoints/sampling,numDataPoints,endpoint = False)

#time only in steps of resolution
resolvedTime = np.linspace(resolution,numDataPoints/sampling-resolution,int(numDataPoints/(sampling*resolution))-1)

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

#create histogram, returns centers of bin and associated probabilities
def distribution(velocities, binCount_,label):
    titles = [label + " Distribution", label + " (m/s)", "Normalized " + label + " Distribution"]
    #plt.figure()
    #plt.title(titles[0])
    #plt.xlabel(titles[1])
    #plt.ylabel("Number of Counts")
    n, bins, patches = plt.hist(velocities,bins=binCount_,visible=False)
    
    binCenters = []
    prob = []
    numData = len(velocities)
    for j in range(len(bins)-1):
        binCenters.append((bins[j]+bins[j+1])/2)
        prob.append(n[j]/numData)
        
    """
    plt.figure()
    plt.plot(binCenters,prob,".")
    plt.title(titles[2])
    plt.xlabel(titles[1])
    plt.ylabel("Probability")
    """
    
    binWidth_ = binCenters[1]-binCenters[0]
    return prob, binCenters, binWidth_

 #maxwell boltzmann velocity distribution in one dimension, takes mass in nanograms
def mbDist(v,m):
    kT = getkT()
    #binWidth = 0.000114752
    scaledM = float(np.dot(m,np.power(10.,-12)))
    dist = np.dot(np.divide(np.sqrt(np.abs(scaledM)),np.sqrt(2*np.pi*kT)),np.exp(np.dot(np.dot(scaledM,-1),np.power(v,2)/(2*kT))))
    return dist

def getMass(calibrationFactor,voltData_):
    
    #full position data
    #posData = calibrate(voltData,calibrationFactor)
    posData = [x * calibrationFactor for x in voltData]
   
    vel = velocity(posData,resolution,sampling)
      
    vProb, vBins, vBinWidth = distribution(vel, binCount, "Velocity")
    
    params, cov = optimize.curve_fit(mbDist,vBins,vProb/vBinWidth,p0=(float(3e-1)))
    measuredMass = params[0]*10**(-12)
   
    #print "calculated mass: ", measuredMass, "kg"
    #plt.figure(5)
    #plt.plot(vBins,mbDist(vBins,*params)*vBinWidth,"-")
    
    return measuredMass

def massDeviation(calibrationFactor,voltData_):
    return np.abs(getMass(calibrationFactor,voltData_) - expectedMass(6.1*10**(-6)))

guess = 13.5e-6
print "getMass: ", getMass(guess,voltData)
print "expectedMass: ", expectedMass(6.1*10**(-6))

print "deviation: ", massDeviation(guess,voltData)
"""
result = optimize.brute(massDeviation, ((1.1e-5,1.8e-5),),args=((voltData,)),Ns= 8,full_output = True)
print result
"""