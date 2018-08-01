# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 11:02:07 2018

@author: alvar
"""

import numpy as np
import matplotlib.pyplot as plt

length = 2000000
resolution = 50
sampling = 10e6 #10 MHz

input_file = open("../data/2018_06_06_1.txt","r") #harry data
posData = []
for lines in range(length):
    posData.append(float(input_file.readline()[:-1]))
input_file.close()

posData = np.arange(0,2000000)
#maxwell boltzmann distribution
def mbDist(v,m,k,T):
    return np.power(m/(2*np.pi*k*T),0.5)*np.exp(-1*m*np.power(v,2)/(2*k*T))


#calculates instantaneous velocity (m/s) from calibrated position data (m) as a function of time (intervals of 1/sampling s)
#returns velocity (m/s) as a function of time (intervals of resolution/sampling s)
def velocity(pos,resolution, sampling):   
    velocity = []
    for i in np.arange(resolution,len(pos)-(resolution-1),resolution):
        firstHalf = np.average(pos[i-resolution:i])
        secondHalf = np.average(pos[i-1:i+resolution-1])
        velocityVal = (secondHalf - firstHalf)/resolution*sampling
        velocity.append(velocityVal)
        
    return velocity

#histogram of velocities
def velDistribution(velocities):
    """histo = np.histogram(velocities,bins=75)
    plt.plot(histo["hist"])
    """
    plt.figure()
    plt.title("vel dist")
    histo = plt.hist(velocities,bins=75)
    plt.show()
    #print histo[:100]
    
    return 0





vel = velocity(posData,resolution,sampling)
velTime = np.arange(resolution,len(posData)-(resolution-1),resolution)

abbrevPos = []
for j in velTime:
    abbrevPos.append(posData[j])

plt.plot(velTime,abbrevPos)
plt.title("pos")
plt.figure()

plt.plot(velTime,vel)
plt.title("velocity")


dist = velDistribution(vel)