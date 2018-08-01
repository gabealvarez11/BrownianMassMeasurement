# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 11:59:10 2018

@author: alvar
"""
from __future__ import division

import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def gaussian(x, mu, sig): 
    return np.power(sig*np.power(2.*np.pi,0.5),-1.)*np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

plt.figure()
x = np.arange(-500,500,1)
y = gaussian(x,0,200)
for i in range(len(y)):
    y[i] += 0.0001*np.random.rand()
    
plt.plot(x,y)

params,cov = curve_fit(gaussian,x,y)
plt.plot(x,gaussian(x,*params))