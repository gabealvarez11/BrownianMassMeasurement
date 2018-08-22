# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 12:29:51 2018

@author: alvar
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

#must first calibrate detector with calibration.py
calibrationFactor = 1.94e-7

#manually controls data input
powers = [10, 20, 50, 60] # mW
binning = 100

#dataName: [label,sampling rate (Hz), number of data points, diameter (um), desired temporal resolution (s), desired bin count]
dataList10 = {}
for i in range(4):
    name = "../Data/filtered/2018_08_17_" + str(i+19) + "_fil.txt"
    dataList10.update({name:[i+19,10**7,powers,6.10,5*10**(-7),binning]})
    
dataList20 = {}
for i in range(5):
    name = "../Data/filtered/2018_08_17_" + str(i+13) + "_fil.txt"
    dataList20.update({name:[i+13,10**7,powers,6.10,5*10**(-7),binning]})
    
dataList50 = {}
for i in range(3):
    name = "../Data/filtered/2018_08_17_" + str(i+1) + "_fil.txt"
    dataList50.update({name:[i+1,10**7,powers,6.10,5*10**(-7),binning]})
    
dataList60 = {}
for i in range(4):
    name = "../Data/filtered/2018_08_15_" + str(i+2) + "_fil.txt"
    dataList60.update({name:[i+2,10**7,powers,6.10,5*10**(-7),binning]})

dataLists = {10: dataList10, 20: dataList20, 50: dataList50, 60: dataList60}


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
def getMass(calibrationFactor_,voltData_,sampling_,resolution_,binCount_,ax=[], label_=-1,counter=0,locs=[] ):

    #convert between voltage and position
    posData = calib(calibrationFactor_,voltData_)
   
    vel = velocity(posData,resolution_,sampling_)
    
    vProb, vBins, vBinWidth = distribution(vel, binCount_)
    
    params, cov = optimize.curve_fit(mbDist,vBins,vProb/vBinWidth,p0=(float(0.237)),bounds=(5e-5,10))
    measuredMass = params[0]*10**(-12)
    
    if(label_>-1):
        fineBins = np.linspace(vBins[0],vBins[len(vBins)-1],10*len(vBins))
        colorOptions = ["b","g","r","c","m","y","k"]
        #lineStyle = colorOptions[label_-13] + "-"
        lineStyle = colorOptions[counter] + '-'
        #dotStyle = colorOptions[label_-13] + "."
        dotStyle = colorOptions[counter] + '.'
        ax[locs[counter][0],locs[counter][1]].plot(np.dot(1e3,vBins),vProb,dotStyle)
        #ax[locs[counter][0],locs[counter][1]].plot(np.dot(1e3,vBins),vProb)
        label_ = "Trial " + str (label_ - 12) + ": " + str(np.round(measuredMass,decimals=16)) + " kg"
        ax[locs[counter][0],locs[counter][1]].plot(np.dot(1e3,fineBins),vBinWidth*mbDist(fineBins,*params),lineStyle, label=label_)
        #ax[locs[counter][0],locs[counter][1]].plot(np.dot(1e3,fineBins),vBinWidth*mbDist(fineBins,*params), label=label_)

    return measuredMass    

#convert between voltage and position
def calib(calibrationFactor_,voltData_):
    posData = [x * calibrationFactor_ for x in voltData_]
    return posData

#controls data processing
def processData(powers_,data,calibrationFactor_):
    counter = 0
    deviations = []
    estimates = []
    locs = [[0,0],[0,1],[1,0],[1,1]]
    f, ax = plt.subplots(2,2, figsize=(12,12),sharex=True, sharey=True)
    f.subplots_adjust(wspace = 0.1, hspace= 0.05)

    f.suptitle("Velocity Distribution of a Trapped 6.1um Bead vs. Power of Laser",fontsize=20,y=0.92)
    ax[0,0].set_ylabel("Probability")
    ax[1,0].set_ylabel("Probability")
    
    for power in data.keys():
        print
        print "power: " + str(power) + "mW"
        print
        
        numDataPoints = int(10 * 1e4) ##constant when testing power
        
        title_ = str(power) + "mW"
        ax[locs[counter][0],locs[counter][1]].set_title(title_)
        if(counter > 1):
            ax[locs[counter][0],locs[counter][1]].set_xlabel("Velocity (mm/s)")
        ax[locs[counter][0],locs[counter][1]].set_ylim((0,0.05))
        ax[locs[counter][0],locs[counter][1]].set_xlim((-0.6,0.6))

        masses = []
        
        for i in data[power].keys():
            label = data[power][i][0]
            sampling = data[power][i][1]
            diameter = data[power][i][3] * 10 **(-6)
            resolution = data[power][i][4]
            binCount = data[power][i][5]
            
            input_file = open(i,"r")
            voltData = []
            for lines in range(numDataPoints):
                voltData.append(float(input_file.readline()[:-1]))
            input_file.close()
            
            slicedData = voltData[200:-200]
        
            expMass = expectedMass(diameter)
            measuredMass = getMass(calibrationFactor_,slicedData,sampling,resolution,binCount,ax, label,counter,locs)
            masses.append(measuredMass)
            print "label: ", label
            print "diameter: ", diameter
            print "expected mass: ", np.round(expMass,decimals=16)
            print "measured mass: ", np.round(measuredMass,decimals=16)
            print "ratio: ", np.round(expMass / measuredMass,decimals=3)
            print
        
        deviations.append(np.std(masses))
        estimates.append(np.mean(masses))
        legendLabel = "Std. Dev. of Mass: " + str(np.round(np.std(masses),decimals=16)) + " kg"
        ax[locs[counter][0],locs[counter][1]].legend(title=legendLabel,loc = 'upper center')
        counter = counter + 1

    plt.savefig("fittings.png")
    return deviations,estimates


stdDev,massEstimates = processData(powers, dataLists,calibrationFactor)
normalizedMass = massEstimates/expectedMass(6.10*10**(-6))
normStdDev = stdDev/expectedMass(6.10*10**(-6))
print massEstimates

f, ax = plt.subplots(2,1,figsize=(8,10))
f.subplots_adjust(hspace= 0.3)

ax[0].set_title("Mass Estimates")
ax[0].set_ylabel("Normalized Mass")
ax[0].set_xlabel("Power (mW)")
#ax[0].set_xscale("log")
ax[0].errorbar(powers,normalizedMass,yerr=normStdDev)
#ax[0].axhline(y=1,linestyle="dashed")
#ax[0].set_ylim(0.6,1.2)

ax[1].set_title("Standard Deviation of Mass Estimates")
ax[1].set_ylabel("Error of Normalized Mass")
ax[1].set_xlabel("Power (mW)")
#ax[1].set_xscale("log")
ax[1].set_yscale("log")
ax[1].plot(powers, normStdDev)
    
#    f.savefig("errors.png")
    
    
    
