#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 10:53:42 2018

@author: juliaorenstein
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import os.path
import glob
import datalist

#must first calibrate detector with calibration.py
calibrationFactor = 1.94e-7

#manually controls data input
current = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0] # in Amps
binning = 100

f,ax = plt.subplots(2,5, figsize=(15,10))

data = glob.glob('../Data/filtered/2018_08_22*')
for loc in data:
    if '2018_08_22_12' in loc or '2018_08_22_23' in loc:
        data.remove(loc)

#expected mass (kg) of microsphere of associated diameter (m)
def expectedMass(diameter):
    density = 2000 #kg/m^3
    return density*4./3*np.pi*np.power(float(diameter) / 2, 3)

#defines boltzmann's constant
k = 1.38064852*10**(-23)

#returns product kT, assumes room temperature of 298K
def getkT():
    return k * 298

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

#maxwell boltzmann velocity distribution in one dimension, takes mass in nanograms
def mbDist(v,m):    
    kT = getkT()
    scaledM = float(np.dot(m,np.power(10.,-12)))
    dist = np.dot(np.divide(np.sqrt(np.abs(scaledM)),np.sqrt(2*np.pi*kT)),np.exp(np.dot(np.dot(scaledM,-1),np.power(v,2)/(2*kT))))
    return dist

#create histogram, returns centers of bin and associated probabilities
def distribution(velocities, binCount_):
    n, bins, patches = plt.hist(velocities,bins=binCount_,visible=False)
    
    binCenters = []
    prob = []
    numData = len(velocities)
    for j in range(len(bins)-1):
        binCenters.append((bins[j]+bins[j+1])/2)
        prob.append(n[j]/numData)
    
    binWidth_ = binCenters[1]-binCenters[0]
    return prob, binCenters, binWidth_

#extracts mass (kg) from data
def getMass(calibrationFactor_,voltData_,sampling_,resolution_,binCount_,ax,label_,current_):
    
    #convert between voltage and position
    posData = calib(calibrationFactor_,voltData_)
   
    vel = velocity(posData,resolution_,sampling_)
    
    vProb, vBins, vBinWidth = distribution(vel, binCount_)
    
    params, cov = optimize.curve_fit(mbDist,vBins,vProb/vBinWidth,p0=(float(0.237)),bounds=(5e-5,10))
    measuredMass = params[0]*10**(-12)

    fineBins = np.linspace(vBins[0],vBins[len(vBins)-1],10*len(vBins))
    dist = np.dot(vBinWidth,mbDist(fineBins,*params))
    
    colorOptions = ["b","g","r","c","m","y","k","b","g","r"]
    colorChoice = colorOptions[int(current_[-1])]
    print x.label + ': ' + str(current_)
    
    lineStyle = colorChoice + "-"
    dotStyle = colorChoice + ","
    plt.subplot(2, 5, 1+int(current_[-1]))
    plt.title('I = ' + str(current_))
    plt.ylim(0,.04)
    plt.plot(np.dot(1e3,vBins),vProb,dotStyle)
    plt.plot(np.dot(1e3,fineBins),vBinWidth*mbDist(fineBins,*params),lineStyle, label=label_)
    
    label_ = str(np.round(measuredMass,decimals=16)) + " kg"
    plt.plot(np.dot(1e3,fineBins),np.divide(dist,np.max(dist)),lineStyle, label=label_)
   
    return measuredMass    

#convert between voltage and position
def calib(calibrationFactor_,voltData_):
    posData = [x * calibrationFactor_ for x in voltData_]
    return posData

def execute(calibrationFactor_):
    
    numDataPoints = int(1 * 1e4) 
    with open(loc,"r") as input_file:
        voltData = []
        for line in range(numDataPoints):
            voltData.append(float(input_file.readline()[:-1]))
    
    #ax.set_ylabel('Probability')
    getMass(calibrationFactor_, voltData, x.sampling, x.resolution, x.binCount, ax, x.label, x.current)

for loc in data:
    x = DataList(loc)            
    execute(calibrationFactor)    
plt.show()
   
'''
    def process(calibrationFactor_):
    
        deviations = []
        estimates = []
        f, ax = plt.subplots(2,5, figsize=(15,10))
        f.subplots_adjust(wspace = 0.1, hspace= 0.05)
    
        f.suptitle("Velocity Distribution of a Trapped 6.1um Bead vs. current of Data Sample",fontsize=20,y=0.92)
        plt.ylabel("Probability")
        
        for loc in data:
            
            x = DataList(loc)
            numDataPoints = int(1 * 1e4)
            
            #title_ = x.current + "A"
    
            masses = []
            
            with open(loc,"r") as input_file:
                voltData = []
                for lines in range(numDataPoints):
                    voltData.append(float(input_file.readline()[:-1]))
    
        
            expMass = expectedMass(x.diameter)
            measuredMass = getMass(calibrationFactor_,voltData,x.sampling,x.resolution,x.binCount,ax,x.label,x.current)
            masses.append(measuredMass)
            print "label: ", x.label
            print "diameter: ", x.diameter
            print "expected mass: ", np.round(expMass,decimals=16)
            print "measured mass: ", np.round(measuredMass,decimals=16)
            print "ratio: ", np.round(expMass / measuredMass,decimals=3)
            print
            
            deviations.append(np.std(masses))
            estimates.append(np.mean(masses))
            #legendLabel = "Std. Dev. of Mass: " + str(np.round(np.std(masses),decimals=16)) + " kg"
            #ax.legend(title=legendLabel,loc = 'upper center')
    
        #plt.savefig("fittings.png")
        return deviations,estimates
    
    stdDev,massEstimates = process(calibrationFactor)
    normalizedMass = massEstimates/expectedMass(6.10*10**(-6))
    normStdDev = stdDev/expectedMass(6.10*10**(-6))
    print massEstimates
    
    f, ax = plt.subplots(2,1,figsize=(8,10))
    f.subplots_adjust(hspace= 0.3)
'''
    
    
'''
    ax.set_title("Mass Estimates")
    ax.set_ylabel("Normalized Mass")
    ax.set_xlabel("Length of Data Sample (ms)")
    ax.set_xscale("log")
    ax.errorbar(length,normalizedMass,yerr=normStdDev)
    #ax[0].axhline(y=1,linestyle="dashed")
    #ax[0].set_ylim(0.6,1.2)
    
    ax.set_title("Standard Deviation of Mass Estimates")
    ax.set_ylabel("Error of Normalized Mass")
    ax.set_xlabel("Length of Data Sample (ms)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.plot(length, normStdDev)
'''
    
            