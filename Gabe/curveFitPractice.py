# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 09:30:40 2018

@author: alvar
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

x = range(50)
y = range(50)

for i in range(len(y)):
    y[i] += 5*np.random.rand()
    
plt.plot(x,y)

def linearFit(x,m,b):
    return m*x + b

params, cov = curve_fit(linearFit,x,y)

fittedY = []
for j in x:
    fittedY.append(linearFit(j,*params))
    
plt.plot(x,fittedY,"-")

print params[0]