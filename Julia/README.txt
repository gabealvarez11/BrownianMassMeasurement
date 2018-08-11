#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 15:51:40 2018

@author: juliaorenstein
"""

TO USE THE filter.py FILE:

SETUP

* set default_run to the run you'd like to inspect/filter/etc
* default_noise_run is not needed unless you're using the subtraction method instead of the filtering method
    * the only reason you'd need to do this is if you're trying to compare the methods
* edit (or make your own) parameters.py file with paths that correspond to your computer
    (although the current once should work if you're not making any fft files)


LOOK AT FFT

* call plot_fft() to look at a single fft, along with highlighted sections over noise peaks
* you can edit the values on plt.axvspan to experiment with different filters


FILTER THE NOISE

* edit the filters list to appropriate values
* right now (as of 08 11 2018) the filtered values get set to zero
    * if one of us eventually writes some sort of averaging code to set the values to a non-zero value,
      then we should set use_average = True
    * this will be marked in a note file for later


COMPARE POSITIONAL DATA BEFORE AND AFTER FILTERING

* call compare_position() to look at position data before and after filtering
* add kwarg 'window = ____' to adjust how much of the data you're viewing. default = 10000


TO EXPORT

* once you're happy with the noise-filtered data, run export_filtered_data() to send new positional
  data to a file in the filtered folder
* the note will be updated with information on how the filtering was done
* if you run this on the same data more than once, the filtered data will be overwritten, SO
    * if there are multiple instances of the same run in the note, then the last one is correct
    * if we want to compare different filtering methods on the same file we should come up with a new naming convention
