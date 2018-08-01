# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 15:44:10 2018

@author: alvar
"""
import numpy as np
import matplotlib.pyplot as plt

#defines boltzmann's constant
k = 1.38064852*10**(-23)

#assumes room temperature of 298K
def getkT():
    return k * 298


"""investigate behavior of mbDist, try to fix overflow"""

#maxwell boltzmann velocity distribution in one dimension, takes mass in nanograms
def mbDist(v,m):
    kT = getkT()
    scaledM = float(np.dot(m,np.power(10.,-12)))
    """print "1: ", np.divide(np.sqrt(np.abs(scaledM)),np.sqrt(2*np.pi*kT))
    print "2: ", np.dot(scaledM,-1)
    print "3: ", np.power(v,2)
    print "4: ", (2*kT)
    print"""
    dist = np.dot(np.divide(np.sqrt(np.abs(scaledM)),np.sqrt(2*np.pi*kT)),np.exp(np.dot(np.dot(scaledM,-1),np.power(v,2)/(2*kT))))
    return dist

x = np.linspace(-0.001,0.001,50)
y=[]
for i in x:
    #print i
    y.append(mbDist(i,.2))
#print y
plt.plot(x,np.dot(0.0001,y))