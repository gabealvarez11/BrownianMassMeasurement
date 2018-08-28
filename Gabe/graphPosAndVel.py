# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 09:24:13 2018

@author: alvar
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams.update({'font.size': 45}) #45
"""
def velocity(pos,resolution, sampling):   
    timeStep = int(np.ceil(resolution*sampling))
    
    velocity = []
    time = []
    for i in np.arange(timeStep,len(pos)-(timeStep),1):      
        firstHalf = np.average(pos[i-timeStep:i])
        secondHalf = np.average(pos[i:i+timeStep])
        
        velocityVal = (secondHalf - firstHalf)/resolution
        velocity.append(velocityVal)
        time.append(i)
    return time,velocity

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

def avgPos(pos,resolution,sampling):
    timeStep = int(np.ceil(resolution*sampling))

    time = []
    avg = []
    for i in np.arange(timeStep/2,len(pos)-(timeStep/2),timeStep):
        time.append(i)
        avg.append(np.average(pos[i-timeStep/2:i+timeStep/2]))
        
    time = time
    return time,avg
        
def velocity(pos,resolution,sampling):
    shortTime, averagedPos = avgPos(pos,resolution,sampling)
    velocity = []
    for counter,value in enumerate(averagedPos):
        if not(counter+1 >=len(averagedPos)):
            velocityVal = (averagedPos[counter+1]-averagedPos[counter])/resolution
            velocity.append(velocityVal)
    return shortTime[:-1], velocity

fileName = "../Data/filtered/2018_08_17_13_fil.txt"
#fileName = "../Data/rawdata/2018_08_17_13.txt"
calibrationFactor = 4.0e-7 #1.94
sampling = 1e7
length = 200000
width = 20000
start = 160000
#res = 5*10**(-6)

#resolvedTime = np.linspace(0,width-2*int(width/(sampling*res)),int(width/(sampling*res)))

#print resolvedTime
t=range(0,width)

input_file = open(fileName,"r")
sample = []
for lines in range(length):
    sample.append(float(input_file.readline()[:-1]))
input_file.close()

slicedSample = sample[start:start+width]


f, ax = plt.subplots(4,1,figsize=(20,40),sharex=True)
f.subplots_adjust(hspace= 0.1)
f.suptitle("Result of numerical derivative on a 6.1um bead",y=0.94)
ax[0].plot(np.dot(1e-4,t),np.dot(np.dot(calibrationFactor,slicedSample),1e9),marker =",")
#ax[0].plot(np.dot(1e-4,posTime),np.dot(averagedPos,1e9),marker = "o",color="r")
f.subplots_adjust(hspace= 0.17)

ax[0].set_ylabel("Position (nm)")
ax[0].set_title("Positional data")
avglength=[0.2,0.5,1,2,3,4,5,10]
avglength = [0.2,1,5]
for i in range(3):
    res = avglength[i]
    vTime, vel = velocity(np.dot(calibrationFactor,slicedSample),res*10**(-6),sampling)
    #posTime,averagedPos = avgPos(np.dot(calibrationFactor,slicedSample),res,sampling)
    ax[i+1].plot(np.dot(1e-4,vTime),np.dot(1e3,vel),marker=".",color="r")
    ax[i+1].set_ylabel("Velocity (mm/s)")
    ax[i+1].set_title("Averaging time: " + str(res) + "us")
    
ax[3].set_xlabel("Time (ms)")
ax[3].xaxis.set_ticks(np.arange(0,2.1, 1))

f.savefig("posAndVel.png")