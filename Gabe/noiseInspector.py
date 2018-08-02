# -*- coding: utf-8 -*-
"""
Created on Wed Aug 01 14:46:49 2018

@author: alvar
"""

import matplotlib.pyplot as plt

length = 100

files = {}
option = "split"
#option = "intensity"
#option = "split, near PD blocked"
#option = "split, far PD blocked"
#option = "vacuum?"

if (option == "split"):
    files.update({"pure laser, split onto both PDs":"../data/rawdata/2018_08_01_1_n.txt"})
    files.update({"through back AOM, split onto both PDs":"../data/rawdata/2018_08_01_8_n.txt"})
    files.update({"through front AOM, split onto both PDs":"../data/rawdata/2018_08_01_14_n.txt"})
    files.update({"through AOM and trap, split onto both PDs":"../data/rawdata/2018_07_31_12_n.txt"})
    files.update({"around AOM but through trap, split onto both PDs":"../data/rawdata/2018_08_02_4_n.txt"})
    
if (option == "intensity"):
    files.update({"pure laser fully incident on back PD":"../data/rawdata/2018_08_01_4_n.txt"})
    files.update({"through back AOM fully incident on back PD":"../data/rawdata/2018_08_01_10_n.txt"})
    files.update({"through front AOM fully incident on back PD":"../data/rawdata/2018_08_01_16_n.txt"})
    files.update({"through trap fully incident on back PD":"../data/rawdata/2018_07_31_8_n.txt"})

if (option == "split, near PD blocked"):
    files.update({"pure laser, split, near PD blocked":"../data/rawdata/2018_08_01_6_n.txt"})
    files.update({"through back AOM, split, near PD blocked":"../data/rawdata/2018_08_01_12_n.txt"})
    files.update({"through front AOM, split, near PD blocked":"../data/rawdata/2018_08_01_18_n.txt"})
    files.update({"through trap, split, near PD blocked":"../data/rawdata/2018_07_31_10_n.txt"})

if (option == "split, far PD blocked"):
    files.update({"pure laser, split, far PD blocked":"../data/rawdata/2018_08_01_7_n.txt"})
    files.update({"through back AOM, split, far PD blocked":"../data/rawdata/2018_08_01_13_n.txt"})
    files.update({"through front AOM, split, far PD blocked":"../data/rawdata/2018_08_01_19_n.txt"})
    files.update({"through trap, split, far PD blocked":"../data/rawdata/2018_07_31_11_n.txt"})

if (option == "vacuum?"):
    files.update({"with vacuum":"../data/rawdata/2018_08_02_2_n.txt"})
    files.update({"without vacuum":"../data/rawdata/2018_08_02_3_n.txt"})

#files.update({"beam blocked":"../data/rawdata/2018_07_31_9_n.txt"})

print length, "points, sampled from", option

t = range(0,length)
for i in files:
    input_file = open(files[i],"r")
    sample = []
    for lines in range(length):
        sample.append(float(input_file.readline()[:-1]))
    input_file.close()
    
    plt.figure()
    plt.plot(t,sample)
    plt.title(i)