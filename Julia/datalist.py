#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 15:30:25 2018

@author: juliaorenstein
"""

import numpy as np
import parameters


class DataList(object):
    def __init__(self, label_):
        self.label = label_
        self.sampling = 10**7
        self.current = None
        self.diameter = None
        self.tempres = None
        with open('../Data/Note.txt') as note:
            for line in note:
                if self.label + ',' in line:
                    self.current = line[line.index('A')-3:line.index('A')]
                    self.diameter = line[line.index('um')-3:line.index('um')]
                    self.resolution = 5*10**(-7)
        
    def get_rawdata(self):
        rawdata_loc = parameters.raw_data_location + self.label + '.txt'
        with open(rawdata_loc) as data:
            self.rawdata = data.read().splitlines()
            
        for i in range(len(self.rawdata)):
            self.rawdata[i] = float(self.rawdata[i])

    def get_fft(self):
        try: self.rawdata
        except AttributeError:
            self.get_rawdata()
        self.fft = np.fft.fft(self.rawdata)
        
    def get_filtered_fft(self):
        try: self.fft
        except AttributeError:
            self.get_fft()
        self.filtered_fft = self.get_fft() #CHANGE THIS
        
    def get_clean_data(self):
        try: self.filtered_fft
        except AttributeError:
            self.get_filtered_fft()
        self.clean_data = np.fft.ifft(self.filtered_fft)
        
        
        
x = DataList('2018_08_22_1')
print x.current
print x.get_rawdata()
