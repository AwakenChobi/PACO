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
    s_candidates = np.where(Y > threshold)[0]

    print("print s_candidates =", s_candidates)

    def center_value(arr):
        n = len(arr)
        return arr[n // 2 - 1] if n % 2 == 0 else arr[n // 2]
    
    saturated_peaks_indices = []
    store_cons_points = []

    for idx, val in enumerate(s_candidates):
        if idx == 0 or val == s_candidates[idx - 1] + 1:
            store_cons_points.append(val)
        else:
            saturated_peaks_indices.append(center_value(store_cons_points))
            store_cons_points = [val]
    if store_cons_points:
        saturated_peaks_indices.append(center_value(store_cons_points))

    #The X values corresponding to the saturated peaks
    saturated_peaks = X[saturated_peaks_indices]

    return saturated_peaks