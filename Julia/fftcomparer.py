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

#alt file organization system
    #list of four tuples (name, data )
data = [('split', []), ('intensity', []), ('split, near PD blocked', []), ('split, far PD blocked', [])]



## reads fft files, plots them 

def readfiles(run):  
    
    freqtmp = []
    fftrealtmp = []
    fftimagtmp = []
    with open(parameters.fft_data_location + run) as ffttext:
        for line in ffttext:
            freqtmp.append(float(line.split()[0]))
            fftrealtmp.append(float(line.split()[1]))
            fftimagtmp.append(float(line.split()[2]))
    
    fftcomplex = [complex(fftrealtmp[i], fftimagtmp[i]) for i in range(len(fftrealtmp))]
    fft = np.array(fftcomplex)
    freq = np.array(freqtmp)
    
    return fft,freq
            
data[0][1].append(readfiles('2018_08_01_1_n_fft.txt'))
data[0][1].append(readfiles('2018_08_01_8_n_fft.txt'))
data[0][1].append(readfiles('2018_08_01_14_n_fft.txt'))
data[0][1].append(readfiles('2018_07_31_12_n_fft.txt'))

data[1][1].append(readfiles("2018_08_01_4_n_fft.txt"))
data[1][1].append(readfiles("2018_08_01_10_n_fft.txt"))
data[1][1].append(readfiles("2018_08_01_16_n_fft.txt"))
data[1][1].append(readfiles("2018_07_31_10_n_fft.txt"))

data[2][1].append(readfiles("2018_08_01_6_n_fft.txt"))
data[2][1].append(readfiles("2018_08_01_12_n_fft.txt"))
data[2][1].append(readfiles("2018_08_01_18_n_fft.txt"))
data[2][1].append(readfiles("2018_07_31_10_n_fft.txt"))

data[3][1].append(readfiles("2018_08_01_7_n_fft.txt"))
data[3][1].append(readfiles("2018_08_01_13_n_fft.txt"))
data[3][1].append(readfiles("2018_08_01_19_n_fft.txt"))
data[3][1].append(readfiles("2018_07_31_11_n_fft.txt"))
    
      
def plot():
    f, ax = plt.subplots(4, 4, figsize = (20,15), sharex='col', sharey='row')
    ax[0, 0].set_title('pure laser')
    ax[0, 1].set_title('through back AOM')
    ax[0, 2].set_title('through front AOM')
    ax[0, 3].set_title('through trap')
    
    ax[0, 0].set_ylabel('split onto both PDs')
    ax[1, 0].set_ylabel('fully incident on back PD')
    ax[2, 0].set_ylabel('near PD blocked')
    ax[3, 0].set_ylabel('far PD blocked')
    
    for (m,n), subplot in np.ndenumerate(ax):
        ax[m, n].set_xscale('log')
        ax[m, n].set_yscale('log')
    for i in range(4):
        ax[3, i].set_xlabel('frequency (Hz)')
   

    counter1 = 0
    for tuple_ in data:
        list_ = tuple_[1]
        counter2 = 0
        for fft_ in list_:
            fft, freq = fft_[0], fft_[1]
            ax[counter1, counter2].plot(freq, abs(fft)**2, ',')
            #ax[counter1, counter2].set_title(list_)
          
            counter2 +=1
        counter1 += 1
    
    plt.show()
    
    f, ax = plt.subplots(figsize = (5,3))
    fft, freq = readfiles('2018_07_31_9_n_fft.txt')
    ax.plot(freq, abs(fft)**2), ','
    ax.set_title('blocked beam')
    ax.set_xlabel('frequency (Hz)')
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    plt.show()

