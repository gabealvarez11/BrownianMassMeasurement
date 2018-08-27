# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 11:52:08 2018

@author: alvar
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 12:29:51 2018

@author: alvar
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import optimize

matplotlib.rcParams.update({'errorbar.capsize': 5})
matplotlib.rcParams.update({'font.size': 12})

#must first calibrate detector with calibration.py
calibrationFactor = 1.90e-7

#manually controls data input
length = 2000000
avglength=[0.2,0.5,1,2,3,4,5,10]
binning = 50
resolution = "x"
#dataName: [label,sampling rate (Hz), number of data points, diameter (um), desired temporal resolution (s), desired bin count]
dataList = {}

dataList.update({"../Data/rawdata/2018_08_17_27_n.txt":[13,10**7,length,0,resolution,binning,"raw noise"]})
dataList.update({"../Data/filtered/2018_08_17_27_n_fil.txt":[14,10**7,length,0,resolution,binning,"filtered noise"]})
dataList.update({"../Data/filtered/2018_08_17_13_fil.txt":[15,10**7,length,6.1,resolution,binning,"filtered data"]})
dataList.update({"../Data/rawdata/2018_08_17_13.txt":[16,10**7,length,6.1,resolution,binning,"raw data"]})

#expected mass (kg) of microsphere of associated diameter (m)
def expectedMass(diameter):
    density = 2000 #kg/m^3
    return density*4./3*np.pi*np.power(diameter / 2, 3)

#defines boltzmann's constant
k = 1.38064852*10**(-23)

#returns product kT, assumes room temperature of 295.25K
def getkT():
    return k * 295.25

def getRMSvel(mass):
    return np.sqrt(getkT()/mass)

#calculates instantaneous velocity (m/s) from calibrated position data (m) as a function of time (intervals of 1/sampling s)
#returns velocity (m/s) as a function of time (intervals of resolution)
"""
def velocity(pos,resolution, sampling):   
    timeStep = int(np.ceil(resolution*sampling))
    
    velocity = []
    for i in np.arange(timeStep,len(pos)-(timeStep),1):      
        firstHalf = np.average(pos[i-timeStep:i])
        secondHalf = np.average(pos[i:i+timeStep])
        
        velocityVal = (secondHalf - firstHalf)/resolution
        velocity.append(velocityVal)
    return velocity
"""

def avgPos(pos,resolution,sampling):
    timeStep = int(np.ceil(resolution*sampling))
    avg = []
    for i in np.arange(timeStep,len(pos)-(timeStep),timeStep):
        avg.append(np.average(pos[i-timeStep/2:i+timeStep/2]))
    return avg
        
def velocity(pos,resolution,sampling):
    averagedPos = avgPos(pos,resolution,sampling)
    velocity = []
    for counter,value in enumerate(averagedPos):
        if not(counter+1 >=len(averagedPos)):
            velocityVal = (averagedPos[counter+1]-averagedPos[counter])/resolution
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
def getMass(calibrationFactor_,voltData_,sampling_,resolution_,binCount_,ax=[], label_=-1,counter=0,locs=[],name="" ):
    
    #convert between voltage and position
    posData = calib(calibrationFactor_,voltData_)
   
    vel = velocity(posData,resolution_,sampling_)
    
    vProb, vBins, vBinWidth = distribution(vel, binCount_)
    
    params, cov = optimize.curve_fit(mbDist,vBins,vProb/vBinWidth,p0=(float(0.237e-4)))
    measuredMass = params[0]*10**(-12)
    
    if(label_>-1):
        fineBins = np.linspace(vBins[0],vBins[len(vBins)-1],100*len(vBins))
        colorOptions = ["b","c","r","y","m","g","k"]
        lineStyle = colorOptions[label_-13] + "-"
        dotStyle = colorOptions[label_-13] + "."
        ax[locs[counter][0],locs[counter][1]].plot(np.dot(1e3,vBins),vProb,dotStyle)
        ax[locs[counter][0],locs[counter][1]].set_ylim((1e-4,10**np.max(vProb)))

        label_ = name
        #label_ = "Trial " + str (label_ - 12) + ": " + str(np.round(measuredMass,decimals=16)) + " kg"
        ax[locs[counter][0],locs[counter][1]].plot(np.dot(1e3,fineBins),vBinWidth*mbDist(fineBins,*params),lineStyle, label=label_)
    return measuredMass    

#convert between voltage and position
def calib(calibrationFactor_,voltData_):
    posData = [x * calibrationFactor_ for x in voltData_]
    return posData

#controls data processing
def processData(avglength_,data,calibrationFactor_):
    counter = 0
    deviations = []
    estimates = []
    
    locs = [[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3]]
    f, ax = plt.subplots(2,4, figsize=(30,20),sharex=False, sharey=False)
    f.subplots_adjust(wspace = 0.15, hspace= 0.15)

    f.suptitle("Signal to Noise Ratios for Various Averaging Lengths (All at Total Sample Length 2ms)",fontsize=20,y=0.95)
    ax[0,0].set_ylabel("Probability")
    ax[1,0].set_ylabel("Probability")
    
    for l in avglength_:
        print
        print "AVG LENGTH: ", l, "us"
        print
        
        
        title_ = str(l) + " us"
        ax[locs[counter][0],locs[counter][1]].set_title(title_)
        #if(counter > 4):
        ax[locs[counter][0],locs[counter][1]].set_xlabel("Velocity (mm/s)")
        ax[locs[counter][0],locs[counter][1]].set_yscale("log")
        #ax[locs[counter][0],locs[counter][1]].set_xlim((-0.6,0.6))

        masses = []
        rms = {}
        
        for i in data:
            label = data[i][0]
            sampling = data[i][1]
            numDataPoints = data[i][2]
            diameter = data[i][3] * 10 **(-6)
            resolution = np.dot(l,10**(-6))
            binCount = data[i][5]
            name = data[i][6]
            
            input_file = open(i,"r")
            voltData = []
            for lines in range(numDataPoints):
                voltData.append(float(input_file.readline()[:-1]))
            input_file.close()
            
            slicedData = voltData[200:-200]
        
            expMass = expectedMass(diameter)
            measuredMass = getMass(calibrationFactor_,slicedData,sampling,resolution,binCount,ax, label,counter,locs,name)
            masses.append(measuredMass)
            rms.update({name:getRMSvel(measuredMass)})
            print name
            print "diameter: ", diameter
            print "expected mass: ", np.round(expMass,decimals=16)
            print "measured mass: ", np.round(measuredMass,decimals=16)
            print "ratio: ", np.round(expMass / measuredMass,decimals=3)
            print
        
        deviations.append(np.std(masses))
        estimates.append(np.mean(masses))
        legendLabel = "raw S/N: " + str(np.round(np.power(rms["raw data"]/rms["raw noise"],2),decimals=2)) + ", filtered S/N: " + str(np.round(np.power(rms["filtered data"]/rms["filtered noise"],2),decimals=2))
        #legendLabel = "Std. Dev. of Mass: " + str(np.round(np.std(masses),decimals=16)) + " kg"
        ax[locs[counter][0],locs[counter][1]].legend(title=legendLabel,loc = 'upper center')
        counter = counter + 1

    plt.savefig("avgfittings.png")
    return deviations,estimates

stdDev,massEstimates = processData(avglength,dataList,calibrationFactor)
normalizedMass = massEstimates/expectedMass(6.10*10**(-6))
normStdDev = stdDev/expectedMass(6.10*10**(-6))
print massEstimates
"""
f, ax = plt.subplots(2,1,figsize=(8,10))
f.subplots_adjust(hspace= 0.3)

ax[0].set_title("Mass Estimates")
ax[0].set_ylabel("Normalized Mass")
#ax[0].set_xlabel("Length of Data Sample (ms)")
ax[0].set_xscale("log")
ax[0].errorbar(length,normalizedMass,yerr=normStdDev,fmt="o")
#ax[0].axhline(y=1,linestyle="dashed")
#ax[0].set_ylim(0.6,1.2)

ax[1].set_title("Standard Deviation of Mass Estimates")
ax[1].set_ylabel("Error of Normalized Mass")
ax[1].set_xlabel("Length of Data Sample (ms)")
ax[1].set_xscale("log")
ax[1].set_yscale("log")
ax[1].plot(length, normStdDev)

f.savefig("avgerrors.png")
"""