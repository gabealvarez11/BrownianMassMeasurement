# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 10:06:17 2018

@author: alvar
"""

from scipy import optimize

def func(x):
    return x**3+x**2-x+1

print optimize.minimize_scalar(func,method="Golden")