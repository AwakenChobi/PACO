from scipy.signal import convolve
import numpy as np
from matplotlib import pyplot as plt

def find_peaks(X, Y):
    #This function finds the peaks in a spectrum Y using a simple derivative method.
    #It returns the indices of the peaks.

    #The kernel is a simple derivative filter
    kernel = [1, 0, -1]

    #Obtaining derivative
    dY = convolve(Y, kernel, 'valid') 

    #Checking for sign-flipping
    S = np.sign(dY)
    ddS = convolve(S, kernel, 'valid')

    #These candidates are basically all negative slope positions
    #Add one since using 'valid' shrinks the arrays
    candidates = np.where(dY < 0)[0] + (len(kernel) - 1)

    #Here they are filtered on actually being the final such position in a run of
    #negative slopes
    peaks = sorted(set(candidates).intersection(np.where(ddS == 2)[0] + 1))

    #If you need a simple filter on peak size you could use:
    alpha = 0.00075
    peaks = np.array(peaks)[Y[peaks] > alpha]

    return peaks