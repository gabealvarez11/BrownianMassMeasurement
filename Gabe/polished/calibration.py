# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 15:00:35 2018

@author: alvar
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

#dataName: [sampling rate (Hz), number of data points, diameter (um), desired temporal resolution (s), desired bin count]
dataList = {}

#input data
length = 40000
binning= 100

for i in range(5):
    if(i+13 != 17):
        name = "../../Data/filtered/2018_08_17_" + str(i+13) + "_fil.txt"
        dataList.update({name:[10**7,length,6.10,5*10**(-6),binning]})
        
#expected mass (kg) of microsphere of associated diameter (m)
def expectedMass(diameter):
    density = 2000 #kg/m^3
    return density*4./3*np.pi*np.power(diameter / 2, 3)

#defines boltzmann's constant
k = 1.38064852*10**(-23)

#returns product kT, assumes room temperature of 298K
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
    for i in np.arange(timeStep,len(pos)-(timeStep),timeStep):
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
def getMass(calibrationFactor_,voltData_,sampling_,resolution_,binCount_):
    
    #convert between voltage and position
    posData = calib(calibrationFactor_,voltData_)
   
    vel = velocity(posData,resolution_,sampling_)
    
    vProb, vBins, vBinWidth = distribution(vel, binCount_)
    
    params, cov = optimize.curve_fit(mbDist,vBins,vProb/vBinWidth,p0=(float(0.237e-3)))
    measuredMass = params[0]*10**(-12)
    
    return measuredMass    

#convert between voltage and position
def calib(calibrationFactor_,voltData_):
    posData = [x * calibrationFactor_ for x in voltData_]
    return posData

#returns magnitude of difference between calculated mass and expected mass (kg)
def massDeviation(calibrationFactor,voltData_,sampling_,resolution_,binCount_,diameter_):
    return np.abs(getMass(calibrationFactor,voltData_,sampling_,resolution_,binCount_) - expectedMass(diameter_))

#controls calibration
def calibrate(data):
    calibrationFactors = []
    
    for i in data:
        sampling = data[i][0]
        numDataPoints = data[i][1]
        diameter = data[i][2] * 10 **(-6)
        resolution = data[i][3]
        binCount = data[i][4]
        
        input_file = open(i,"r")
        voltData = []
        for lines in range(numDataPoints):
            voltData.append(float(input_file.readline()[:-1]))
        input_file.close()
        
        #old method of optimization
        #result = optimize.brute(massDeviation, ((0.1e-6,0.8e-6),),args=((voltData,sampling,resolution,binCount,diameter)),Ns= 10,full_output = True)
        
        print "calibrating..."
        result = optimize.minimize(massDeviation,3.27e-7,args=((voltData,sampling,resolution,binCount,diameter)),bounds=((1e-7,1e-4),),tol=1e-7)
                
        calibrationFactor = result.x[0]
        
        calibrationFactors.append(calibrationFactor)
        
    return np.average(calibrationFactors)
    
avgCalFactor = calibrate(dataList)
print "average calibration factor: ", avgCalFactor, " m/V"