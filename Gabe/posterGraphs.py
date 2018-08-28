# -*- coding: utf-8 -*-
"""
Created on Tue Aug 28 14:05:56 2018

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
matplotlib.rcParams.update({'font.size': 40})

#must first calibrate detector with calibration.py
calibrationFactor = 4.0e-7

#manually controls data input
length0="x"
length = [300,50,5] # x 1e4
#length = [10,9,8,7,6,5,4,3,2,1]
#length= [10,5,1]
binning = 100
RESOLUTION=5e-6
#dataName: [label,sampling rate (Hz), number of data points, diameter (um), desired temporal resolution (s), desired bin count]
dataList = {}

for i in range(5):
    if(i+13 != 17):
        name = "../Data/rawdata/2018_08_17_" + str(i+13) + ".txt"
        dataList.update({name:[i+13,10**7,length0,6.10,RESOLUTION,binning,"data"]})

dataList.update({"../Data/filtered/2018_08_17_27_n_fil.txt":[19,10**7,length,0,RESOLUTION,binning,"noise"]})
#dataList.update({"../Data/rawdata/2018_08_17_27_n.txt":[19,10**7,length,0,0.5*10**(-6),binning]})
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
def getMass(calibrationFactor_,voltData_,sampling_,resolution_,binCount_,ax=[], label_=-1,counter=0,locs=[],name=""):
    
    #convert between voltage and position
    posData = calib(calibrationFactor_,voltData_)
   
    vel = velocity(posData,resolution_,sampling_)
    
    vProb, vBins, vBinWidth = distribution(vel, binCount_)
    
    params, cov = optimize.curve_fit(mbDist,vBins,vProb/vBinWidth,p0=(float(0.237e-3)))
    measuredMass = params[0]*10**(-12)
    
    if(label_>-1):
        fineBins = np.linspace(vBins[0],vBins[len(vBins)-1],100*len(vBins))
        colorOptions = ["b","g","r","c","m","y","k"]
        numOptions = ["2","4","1","3"]
        lineStyle = colorOptions[label_-13] + "-"
        dotStyle = colorOptions[label_-13] + "o"
        dist = np.dot(vBinWidth,mbDist(fineBins,*params))
        ax[counter].plot(np.dot(1e3,vBins),np.divide(vProb,np.max(dist)),dotStyle)
        if not (name == "noise"):
            label_ = "Trial " + numOptions[label_ - 13] + ": " + str(np.round(measuredMass,decimals=16)) + " kg"
        else:
            label_ = "Noise"
        ax[counter].plot(np.dot(1e3,fineBins),np.divide(dist,np.max(dist)),lineStyle, label=label_,linewidth=5)
    return measuredMass    

#convert between voltage and position
def calib(calibrationFactor_,voltData_):
    posData = [x * calibrationFactor_ for x in voltData_]
    return posData

#controls data processing
def processData(length_,data,calibrationFactor_):
    counter = 0
    deviations = []
    estimates = []
    locs = [0,1,2]
    f, ax = plt.subplots(1,3, figsize=(50,20), sharey=True)
    f.subplots_adjust(wspace = 0.1, hspace= 0.05)

    f.suptitle("Velocity distribution of a trapped 6.1um bead vs. length of data sample (" + str(binning) + " bins, " + str(np.dot(1e6,RESOLUTION)) + "us averaging time)",fontsize=55,y=0.96)
    ax[0].set_ylabel("Normalized counts",fontsize=55)
    #ax[1,0].set_ylabel("Normalized Counts",fontsize=55)
    
    noiseLevel = []

    for l in length_:
        print
        print "LENGTH: ", l, "ms"
        print
        
        numDataPoints = int(l * 1e4)
        
        title_ = str(l) + " ms"
        ax[counter].set_title(title_,fontsize=55)
        #if(counter > 4):
        ax[counter].set_xlabel("Velocity (mm/s)",fontsize=55)
        ax[counter].set_ylim((1e-4,1.6)) #0.08
        #ax[locs[counter][0],locs[counter][1]].set_yscale("log")
        ax[counter].set_xlim((-0.5,0.5))

        masses = []
        for i in data:
            label = data[i][0]
            sampling = data[i][1]
            diameter = data[i][3] * 10 **(-6)
            resolution = data[i][4]
            binCount = data[i][5]
            name = data[i][6]
            input_file = open(i,"r")
            voltData = []
            for lines in range(numDataPoints):
                voltData.append(float(input_file.readline()[:-1]))
            input_file.close()
            
            #slicedData = voltData[200:-200]
        
            expMass = expectedMass(diameter)
            measuredMass = getMass(calibrationFactor_,voltData,sampling,resolution,binCount,ax, label,counter,locs,name)
            if not (name == "noise"):
                masses.append(measuredMass)
            else:
                noiseMass = measuredMass
                
            print "label: ", label
            print "diameter: ", diameter
            print "expected mass: ", np.round(expMass,decimals=16)
            print "measured mass: ", np.round(measuredMass,decimals=16)
            print "ratio: ", np.round(expMass / measuredMass,decimals=3)
            print
        
        deviations.append(np.std(masses))
        estimates.append(np.mean(masses))
        noiseLevel.append(getRMSvel(noiseMass))
        #legendLabel = "Std. Dev. of Mass: " + str(np.round(np.std(masses),decimals=16)) + " kg \n S/N: " + str(np.round(np.power(getRMSvel(np.mean(masses))/getRMSvel(noiseMass),2),decimals=2))
        legendLabel = "Precision of fit: " + str(np.round(100*np.std(masses)/np.mean(masses),decimals=1)) + "%"
        leg = ax[counter].legend(loc = 'upper center',fontsize=40)
        leg.set_title(legendLabel, prop = {'size':40})

        counter = counter + 1

    plt.savefig("posterfittings.png")
    print noiseLevel
    print np.mean(noiseLevel)
    return deviations,estimates

stdDev,massEstimates = processData(length,dataList,calibrationFactor)
normalizedMass = massEstimates/expectedMass(6.10*10**(-6))
normStdDev = stdDev/expectedMass(6.10*10**(-6))
print massEstimates

f, ax = plt.subplots(2,1,figsize=(15,20))
f.subplots_adjust(hspace= 0.3)

ax[0].set_title("Mass estimates",fontsize=55)
ax[0].set_ylabel("Normalized mass",fontsize=55)
#ax[0].set_xlabel("Length of Data Sample (ms)")
ax[0].set_xscale("log")
ax[0].errorbar(length,normalizedMass,yerr=normStdDev,fmt="o")
#ax[0].axhline(y=1,linestyle="dashed")
#ax[0].set_ylim(0.6,1.2)

ax[1].set_title("Standard deviation of mass estimates",fontsize=45)
ax[1].set_ylabel("Error of normalized mass",fontsize=45)
ax[1].set_xlabel("Length of data sample (ms)",fontsize=45)
ax[1].set_xscale("log")
ax[1].set_yscale("log")
ax[1].plot(length, normStdDev)

f.savefig("postererrors.png")