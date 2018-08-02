# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 14:52:33 2018

@author: alvar
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

#must first calibrate detector with calibration.py
calibrationFactor = 5.35e-7

#manually controls data input
length = 400000
binning = 30

#dataName: [label,sampling rate (Hz), number of data points, diameter (um), desired temporal resolution (s), desired bin count]
dataList = {}

"""
dataList.update({"../../data/rawdata/2018_06_06_1.txt":[1,10.**7,length,6.1,5*10**(-6),binning]}) #2000128
dataList.update({"../../data/subtracted/2018_06_06_1_sub.txt":[2,10.**7,length,6.1,5*10**(-6),binning]}) #2000128
dataList.update({"../../data/rawdata/2018_07_17_3.txt":[3,10.**7,length,3.17,5*10**(-6),binning]}) #4000128
dataList.update({"../../data/rawdata/2018_06_18_1.txt":[4,10.**7,length,3.01,5*10**(-6),binning]}) #4000128
dataList.update({"../../data/rawdata/2018_07_11_1.txt":[5,10.**7,length,5.09,5*10**(-6),binning]}) #4000128


for i in range(1):
    name = "../../Data/rawdata/2018_07_30_" + str(16+i) + ".txt"
    print name
    dataList.update({name:[i,10**7,length,4.74,5*10**(-6),binning]})
"""

dataList.update({"../../data/rawdata/2018_07_31_13.txt":[1,10.**7,length,5.07,5*10**(-6),binning]})

#expected mass (kg) of microsphere of associated diameter (m)
def expectedMass(diameter):
    density = 2000 #kg/m^3
    return density*4./3*np.pi*np.power(diameter / 2, 3)

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
def getMass(calibrationFactor_,voltData_,sampling_,resolution_,binCount_,label_=0):
    
    #convert between voltage and position
    posData = calib(calibrationFactor_,voltData_)
   
    vel = velocity(posData,resolution_,sampling_)
    
    vProb, vBins, vBinWidth = distribution(vel, binCount_)
    
    params, cov = optimize.curve_fit(mbDist,vBins,vProb/vBinWidth,p0=(float(0.237)),bounds=(5e-3,10))
    measuredMass = params[0]*10**(-12)
    
    if(label_>-1):
        fineBins = np.linspace(vBins[0],vBins[len(vBins)-1],10*len(vBins))
        title = "Velocity Distribution for Dataset "+ str(label_)
        plt.figure()
        plt.title(title)
        plt.xlim(1.1*(np.min(vBins)),1.1*np.max(vBins))
        plt.ylim((-0.005,np.max(vProb)+0.01))
        plt.xlabel("Velocity (m/s)")
        plt.ylabel("Probability")
        plt.plot(vBins,vProb,".")
        plt.plot(fineBins,vBinWidth*mbDist(fineBins,*params))
    return measuredMass    

#convert between voltage and position
def calib(calibrationFactor_,voltData_):
    posData = [x * calibrationFactor_ for x in voltData_]
    return posData

#controls data processing
def processData(data,calibrationFactor_):
    for i in data:
        label = data[i][0]
        sampling = data[i][1]
        numDataPoints = data[i][2]
        diameter = data[i][3] * 10 **(-6)
        resolution = data[i][4]
        binCount = data[i][5]
        
        input_file = open(i,"r")
        voltData = []
        for lines in range(numDataPoints):
            voltData.append(float(input_file.readline()[:-1]))
        input_file.close()
        
        expMass = expectedMass(diameter)
        measuredMass = getMass(calibrationFactor_,voltData,sampling,resolution,binCount,label)
        
        print "label: ", label
        print "diameter: ", diameter
        print "expected mass: ", expMass
        print "measured mass: ", measuredMass
        print "ratio: ", expMass / measuredMass
        print

processData(dataList,calibrationFactor)