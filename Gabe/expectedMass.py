# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 14:44:22 2018

@author: alvar
"""
import numpy as np

def expectedMass(diameter):
    density = 2000 #kg / m^3
    return density* 4./3*np.pi*np.power(diameter / 2, 3)

diam = 2.01*10**(-6) #m

print expectedMass(diam), "kg"