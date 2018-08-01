# -*- coding: utf-8 -*-
"""
Created on Wed Aug 01 14:46:49 2018

@author: alvar
"""

length = 10000

files = {}
#option = "split"
option = "intensity"

if (option == "split"):
    files.update({"pure laser, split onto both PDs":"../data/rawdata/2018_08_01_1.txt"})
    files.update({"through back AOM, split onto both PDs":"../data/rawdata/2018_08_01_8.txt"})
    files.update({"through front AOM, split onto both PDs":"../data/rawdata/2018_08_01_14.txt"})

if (option == "intensity"):
    files.update({"pure laser fully incident on back PD":"../data/rawdata/2018_08_01_4.txt"})
    files.update({"through back AOM fully incident on back PD":"../data/rawdata/2018_08_01_10.txt"})
    files.update({"through front AOM fully incident on back PD":"../data/rawdata/2018_08_01_16.txt"})


t = range(0,length)
for i in files:
    input_file = open(files[i],"r")
    sample = []
    for lines in range(length):
        sample.append(float(input_file.readline()[:-1]))
    input_file.close()
    
    #print sample
    plt.figure()
    plt.plot(t,sample,)
    plt.title(i)
