# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 12:29:51 2018

@author: alvar
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

#must first calibrate detector with calibration.py
calibrationFactor = 1.9e-7

#manually controls data input
length = 4000128
binning = 100

#dataName: [label,sampling rate (Hz), number of data points, diameter (um), desired temporal resolution (s), desired bin count]
dataList = {}

for i in range(5):
    if(i+13 != 17):
        name = "../Data/filtered/2018_08_17_" + str(i+13) + "_fil.txt"
        dataList.update({name:[i+13,10**7,length,6.10,5*10**(-7),binning]})

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
def getMass(calibrationFactor_,voltData_,sampling_,resolution_,binCount_,label_=-1):
    
    #convert between voltage and position
    posData = calib(calibrationFactor_,voltData_)
   
    vel = velocity(posData,resolution_,sampling_)
    
    vProb, vBins, vBinWidth = distribution(vel, binCount_)
    
    params, cov = optimize.curve_fit(mbDist,vBins,vProb/vBinWidth,p0=(float(0.237)),bounds=(5e-5,10))
    measuredMass = params[0]*10**(-12)
    
    if(label_>-1):
        fineBins = np.linspace(vBins[0],vBins[len(vBins)-1],10*len(vBins))
        #title = "Velocity Distribution for Dataset "+ str(label_)
        #plt.figure()
        #plt.title(title)
        #plt.xlim(1.1*(np.min(vBins)),1.1*np.max(vBins))
        #plt.ylim((-0.005,np.max(vProb)+0.01))
        
        #plt.xlabel("Velocity (m/s)")
        #plt.ylabel("Probability")
        colorOptions = ["b","g","r","c","m","y","k"]
        lineStyle = colorOptions[label_-13] + "-"
        dotStyle = colorOptions[label_-13] + "."
        plt.plot(vBins,vProb,dotStyle)
        label_ = "Trial " + str (label_ - 12) + ": " + str(np.round(measuredMass,decimals=16)) + " kg"
        plt.plot(fineBins,vBinWidth*mbDist(fineBins,*params),lineStyle, label=label_)
        plt.legend(title="Masses Extracted From Fittings")
    return measuredMass    

#convert between voltage and position
def calib(calibrationFactor_,voltData_):
    posData = [x * calibrationFactor_ for x in voltData_]
    return posData

#controls data processing
def processData(data,calibrationFactor_):
    
    plt.figure(figsize=(10,10))
    plt.xlabel("Velocity (m/s)")
    plt.ylabel("Probability")
    plt.xlim((-0.0005,0.0005))
    plt.ylim((0,0.05))
    plt.title("Maxwell-Boltzmann Velocity Distributions for a 6.1um Bead")
    
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
        
        slicedData = voltData[200:-200]
    
        expMass = expectedMass(diameter)
        measuredMass = getMass(calibrationFactor_,slicedData,sampling,resolution,binCount,label)
        
        print "label: ", label
        print "diameter: ", diameter
        print "expected mass: ", np.round(expMass,decimals=16)
        print "measured mass: ", np.round(measuredMass,decimals=16)
        print "ratio: ", np.round(expMass / measuredMass,decimals=3)
        print
    
    plt.savefig("fittings.png")

processData(dataList,calibrationFactor)