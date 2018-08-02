#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 14:27:37 2018

@author: juliaorenstein
"""

import numpy as np
import matplotlib.pyplot as plt
import parameters
import glob

datalocs = glob.glob(parameters.raw_data_location + '*.txt')
runs = []
for i in datalocs:
    runs.append(i[67:-4])
    
noiseruns = []
for i in runs:
    if '_n' in i:
        noiseruns.append(i)

options =  ['intensity', 'split', 'split, near PD blocked', 'split, far PD blocked']    
files = {}
option = "split"
#option = "intensity"
#option = "split, near PD blocked"
#option = "split, far PD blocked"

if (option == "split"):
    files.update({"pure laser, split onto both PDs":parameters.fft_data_location + "2018_08_01_1_n_fft.txt"})
    files.update({"through back AOM, split onto both PDs":parameters.fft_data_location + "2018_08_01_8_n_fft.txt"})
    files.update({"through front AOM, split onto both PDs":parameters.fft_data_location + "2018_08_01_14_n_fft.txt"})
    files.update({"through trap, split onto both PDs":parameters.fft_data_location + "2018_07_31_12_n_fft.txt"})
    
if (option == "intensity"):
    files.update({"pure laser fully incident on back PD":parameters.fft_data_location + "2018_08_01_4_n_fft.txt"})
    files.update({"through back AOM fully incident on back PD":parameters.fft_data_location + "2018_08_01_10_n_fft.txt"})
    files.update({"through front AOM fully incident on back PD":parameters.fft_data_location + "2018_08_01_16_n_fft.txt"})
    files.update({"through trap fully incident on back PD":parameters.fft_data_location + "2018_07_31_8_n_fft.txt"})

if (option == "split, near PD blocked"):
    files.update({"pure laser, split, near PD blocked":parameters.fft_data_location + "2018_08_01_6_n_fft.txt"})
    files.update({"through back AOM, split, near PD blocked":parameters.fft_data_location + "2018_08_01_12_n_fft.txt"})
    files.update({"through front AOM, split, near PD blocked":parameters.fft_data_location + "2018_08_01_18_n_fft.txt"})
    files.update({"through trap, split, near PD blocked":parameters.fft_data_location + "2018_07_31_10_n_fft.txt"})

if (option == "split, far PD blocked"):
    files.update({"pure laser, split, far PD blocked":parameters.fft_data_location + "2018_08_01_7_n_fft.txt"})
    files.update({"through back AOM, split, far PD blocked":parameters.fft_data_location + "2018_08_01_13_n_fft.txt"})
    files.update({"through front AOM, split, far PD blocked":parameters.fft_data_location + "2018_08_01_19_n_fft.txt"})
    files.update({"through trap, split, far PD blocked":parameters.fft_data_location + "2018_07_31_11_n_fft.txt"})

#files.update({"beam blocked":parameters.fft_data_location + "2018_07_31_9_n_fft.txt"})    

## reads fft files, plots them 
def initializedictionary():
    fftdata = {}
    return fftdata

def readfiles():  
    
    for k in options:
    
        for j in files:
            freqtmp = []
            fftrealtmp = []
            fftimagtmp = []
            with open(files[j]) as ffttext:
                for line in ffttext:
                    freqtmp.append(float(line.split()[0]))
                    fftrealtmp.append(float(line.split()[1]))
                    fftimagtmp.append(float(line.split()[2]))
            
            fftcomplex = [complex(fftrealtmp[i], fftimagtmp[i]) for i in range(len(fftrealtmp))]
            fft = np.array(fftcomplex)
            freq = np.array(freqtmp)
            
            fftdata[j] = [freq,fft]
            
            
    
try: fftdata
except NameError:
    fftdata = initializedictionary()
    readfiles()
    

    
def plot():
    f, ax = plt.subplots(4, 4, figsize = (20,15), sharex='col', sharey='row')
    counter1 = 0
    for k in options:
        counter2 = 0
        for j in fftdata:
            freq,fft = fftdata[j][0], fftdata[j][1]
            ax[counter1, counter2].plot(freq, abs(fft)**2, ',')
            ax[counter1, counter2].set_title(j)
            if counter1 == 3:
                ax[counter1, counter2].set_xlabel('frequency (Hz)')
            ax[counter1, counter2].set_xscale('log')
            ax[counter1, counter2].set_yscale('log')
            
            
            counter2 +=1
        counter1 += 1

'''    
fftdata = {}

def readfile(run):
    print 'reading file into dictionary...'
    freqtmp = []
    fftrealtmp = []
    fftimagtmp = []
    with open(parameters.fft_data_location + run + '_fft.txt') as ffttext:
        for line in ffttext:
            freqtmp.append(float(line.split()[0]))
            fftrealtmp.append(float(line.split()[1]))
            fftimagtmp.append(float(line.split()[2]))
    
    fftcomplex = [complex(fftrealtmp[i], fftimagtmp[i]) for i in range(len(fftrealtmp))]
    fft = np.array(fftcomplex)
    freq = np.array(freqtmp)
    
     
    fftdata[run] = [freq, fft]    

## plot
def plotffts(runs):
    for i in runs:
        readfile(i)
    fig, ax = plt.subplots(figsize = (10,5))
    ax.legend(markerscale = 10)  
    for i in runs:
        freq = fftdata[i][0].tolist()
        fft = fftdata[i][1]
        power = (abs(fft)**2).tolist()
        ax.plot(freq, power, ',', label = i)
        print
        print 'peaks in ' + i + ':'
        j = max(power[1:-1])
        print str(freq[power.index(j)]) + 'Hz, ' + str(j)            
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('frequency (Hz)')
'''