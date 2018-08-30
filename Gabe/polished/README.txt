README for Gabe's programs.


calibration.py

Takes in a series of data files, optimizes mass fittings to expected mass by varying calibration factors.

Change "length" (of data sample) and "binning" to match downstream analysis. The longer the sample, the more accurate...
the result, but the slower the runtime. Binning should be chosen to match rms amplitude of noise...
as of 8/29/2018, this is about 100 bins.

May need to change the temperature--parameter is used in getkT() function.

Prints / returns average calibration factor.




dataToMass.py

Takes in a series of data files, already noise cancelled, and will extract the mass from each of them.

Manually input calibration factor from calibration.py.

Change the "length" parameter to modify how many data points are read in. I recommend testing first at a small length...
and then increasing to the full length of the file.





graphPosAndVel.py

Designed to visualize how averaging affects the actual plot of velocity.

"avglength" array contains the averaging lengths that will be used for the plots. Change at will--the graphs should update accordingly.

Ensure that start + width <= length. Start is the beginning of the window of data that will be displayed (width is the duration of the window).
Length is the amount of data read into the program. Leave length relatively long.




graphFittings.py

Intended to take in data files and plot velocity distributions and fittings to MB-distribution with various lengths of sample.

Choose 10 different lengths of sample in the array "length".

Crucial for characterizing precision of measurement at short time scales--also produces a plot of...
how the mass estimates and the variances depend on the length of sample.