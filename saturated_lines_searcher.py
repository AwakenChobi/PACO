import numpy as np

def saturated_lines_searcher(X, Y):
    
    if len(X) != len(Y):
        raise ValueError("X and Y must have the same length")
    #This function finds the saturated peaks in a spectrum Y by assuming that
    #avobe a certain threshold the signal is saturated. It returns the x position of the
    #saturated peaks.

    #If the value of the intensity is higher than a certain threshold, we consider it as a saturated peak
    #You can change the threshold value to suit your needs
    threshold = 19000

    #These candidates are basically all negative slope positions
    #Add one since using 'valid' shrinks the arrays
    s_candidates = np.where(Y > threshold)

    #The X values corresponding to the saturated peaks
    saturated_peaks = X[s_candidates]

    return saturated_peaks