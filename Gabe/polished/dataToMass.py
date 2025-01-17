# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 14:52:33 2018

@author: alvar
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

#must first calibrate detector with calibration.py
calibrationFactor = 4.0e-7

#manually controls data input
length = 38000 #how many points you want to read in
binning = 100 #how many bins used in histogram
resolution = 5*10**(-6) #length of averaging for velocity calculation, in seconds

print "LENGTH OF SAMPLES: ", length, " POINTS"
print

#dataName: [label,sampling rate (Hz), number of data points, diameter (um), desired temporal resolution (s), desired bin count]
dataList = {}

#input whatever data you want here
for i in range(1):
    if(i+13 != 17):
        name = "../../Data/filtered/2018_08_17_" + str(i+13) + "_fil.txt"
        dataList.update({name:[i+13,10**7,length,6.01,resolution,binning]})
dataList.update({"../../Data/rawdata/2018_08_17_27_n.txt":["filtered noise",10**7,length,0,resolution,binning]})
dataList.update({"../../Data/filtered/2018_08_17_27_n_fil.txt":["noise",10**7,length,0,resolution,binning]})

#expected mass (kg) of microsphere of associated diameter (m)
def expectedMass(diameter):
    density = 2000 #kg/m^3
    return density*4./3*np.pi*np.power(diameter / 2, 3)

#defines boltzmann's constant
k = 1.38064852*10**(-23)

#returns product kT, assumes room temperature of 295.25K
def getkT():
    return k * 295.25

#calculates instantaneous velocity (m/s) from calibrated position data (m) as a function of time (intervals of 1/sampling s)
#returns velocity (m/s) as a function of time (intervals of resolution)
def velocity(pos,resolution,sampling):
    averagedPos = avgPos(pos,resolution,sampling)
    velocity = []
    for counter,value in enumerate(averagedPos):
        if not(counter+1 >=len(averagedPos)):
            velocityVal = (averagedPos[counter+1]-averagedPos[counter])/resolution
            velocity.append(velocityVal)
    return velocity

#helper method for velocity, averages positional values
def avgPos(pos,resolution,sampling):
    timeStep = int(np.ceil(resolution*sampling))
    avg = []
    for i in np.arange(timeStep/2,len(pos)-(timeStep/2),timeStep):
        avg.append(np.average(pos[i-timeStep/2:i+timeStep/2]))
    return avg
        
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
def getMass(calibrationFactor_,voltData_,sampling_,resolution_,binCount_,label_=""):
    
    #convert between voltage and position
    posData = calib(calibrationFactor_,voltData_)
   
    vel = velocity(posData,resolution_,sampling_)
    
    vProb, vBins, vBinWidth = distribution(vel, binCount_)
    
    params, cov = optimize.curve_fit(mbDist,vBins,vProb/vBinWidth,p0=(float(0.237e-3)))
    measuredMass = params[0]*10**(-12)
    
    if not(label_ == ""):
        fineBins = np.linspace(vBins[0],vBins[len(vBins)-1],100*len(vBins))
        title = "Velocity distributions with corresponding MB fittings"
        plt.title(title)
        plt.xlabel("Velocity (mm/s)")
        plt.ylabel("Normalized counts")
        dist = np.dot(vBinWidth,mbDist(fineBins,*params))

        plt.plot(np.dot(1e3,vBins),np.divide(vProb,np.max(dist)),".")
        plt.plot(np.dot(1e3,fineBins),np.divide(dist,np.max(dist)),label=label_)
        plt.ylim((1e-5,1.1))
        plt.legend()
                
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