import numpy as np
from scipy.stats import linregress

def rot_temperature_C2(x, y):
    x = np.array(x)
    y = np.array(y)
    peaks=[]
    wavelength_subpeaks = { "P25" : 516.18, "P26" : 516.11, "P27" : 516.03, "P28" : 515.95,
                            "P29" : 515.86, "P30" : 515.77, "P31" : 515.66, "P32" : 515.56,
                            "P33" : 515.44, "P34" : 515.32, "P35" : 515.19, "P36" : 515.07,
                            "P37" : 514.92, "P38" : 514.78, "P39" : 514.62, "P40" : 514.47,
                            "P41" : 513.30, "P42" : 514.13, "P43" : 513.95, "P44" : 513.77,
                            "P45" : 513.57
                            }
    
    crosssection_subpeaks= {"P25" : 24.96, "P26" : 25.961538, "P27" : 26.962963, "P28" : 27.964286, 
                            "P29" : 28.965517, "P30" : 29.966667, "P31" : 30.967742, "P32" : 31.96875,
                            "P33" : 32.969697, "P34" : 33.970588, "P35" : 34.971429, "P36" : 35.972222,
                            "P37" : 36.972222, "P38" : 37.973684, "P39" : 38.974359, "P40" : 39.975,
                            "P41" : 40.97561, "P42" : 41.97619, "P43" : 42.976744, "P44" : 43.977273,
                            "P45" : 44.977778
                            }

    energy_subpeaks = [(i**2)-i for i in range(25, 46)]
    
    background = 0
    backgroundlist = []

    maskb = (x >= 517.8) & (x <= 518.0)
    for yi in y[maskb]:
        backgroundlist.append(yi)
    
    background = np.mean(backgroundlist)
        
    print(f"Background value: {background}")

    tolerance = 0.055
    for key in [f"P{i}" for i in range(25, 46)]:
        center = wavelength_subpeaks[key]
        mask = (x >= center - tolerance) & (x <= center + tolerance)
        if np.any(mask):
            peaks.append(np.max(y[mask]-background))
        else:
            print(f"Warning: No x values found for {key} in interval [{center-tolerance}, {center+tolerance}]")  # or handle missing data as you prefer
            peaks.append(np.nan)
        
        print(f"Peak for {key}: {peaks[-1]}") # Print the last added peak value

    log_i_A = [np.log10(peaks[i]/crosssection_subpeaks[f"P{i+25}"]) for i in range(len(peaks))]
    
    for aaa in log_i_A:
        print(f"log I/A for peak P :{aaa}")

    slope, intercept, r_value, p_value, std_err = linregress(energy_subpeaks, log_i_A)

    print(f"Slope: {slope}, Intercept: {intercept}, R-squared: {r_value**2}, P-value: {p_value}, Standard Error: {std_err}")
    #-1.09 is the factor used to convert the slope to temperature in Kelvin
    temperature = -1.09 / slope
    print(f"Temperature: {temperature} K")
    error = (std_err * 1.09) / (slope * slope)  # Error of the slope 
    return temperature, error, r_value, p_value, intercept

########################################################################################################################################################################
########################################################################################################################################################################

def rot_temperature_OH(x, y):
    x = np.array(x)
    y = np.array(y)
    peaks=[]
    
    wavelength_subpeaks = { "Q4" : 308.3, "Q5" : 308.5, "Q6" : 308.7, "Q8" : 309.2, "Q9" : 309.5, "Q10" : 309.8}

    crosssection_subpeaks= {"Q4" : 3.37e16, "Q5" : 4.22e19, "Q6" : 5.06e19, "Q8" : 6.75e19, "Q9" : 7.58e19, "Q10" : 8.41e19}

    energy_subpeaks = [32779, 32948, 33150, 33652, 33952, 34283]
    
    background = 0
    backgroundlist = []

    maskb = (x >= 306.0) & (x <= 306.25)
    for yi in y[maskb]:
        backgroundlist.append(yi)
    background = np.mean(backgroundlist)

    tolerance = 0.08
    for key in [f"Q{i}" for i in range(4, 11)]:
        center = wavelength_subpeaks[key]
        mask = (x >= center - tolerance) & (x <= center + tolerance)
        if np.any(mask):
            peaks.append(np.max(y[mask]-background))
        else:
            print(f"Warning: No x values found for {key} in interval [{center-tolerance}, {center+tolerance}]")  # or handle missing data as you prefer
            peaks.append(np.nan)

    log_i_A = [np.log10(peaks[i]/crosssection_subpeaks[f"Q{i+4}"]) for i in range(len(peaks))]


    slope, intercept, r_value, p_value, std_err = linregress(energy_subpeaks, log_i_A)

    #-0.625 is the factor used to convert the slope to temperature in Kelvin
    temperature = -0.625 / slope  
    error = (std_err * 0.625) / (slope * slope)  # Error of the slope 
    return temperature, error, r_value, p_value, intercept


########################################################################################################################################################################
########################################################################################################################################################################

def rot_temperature_N2_plus(x, y):
    x = np.array(x)
    y = np.array(y)
    
    peaks=[]

    wavelength_subpeaks = { "L1" : 390.41, "L2" : 390.6, "L3" : 390.76, "L4" : 390.91, "L5" : 391.04, "L6" : 391.15, "L7" : 391.25}

    crosssection_subpeaks= { "L1" : 68, "L2" : 64, "L3" : 60, "L4" : 56, "L5" : 52, "L6" : 48, "L7" : 44}

    energy_subpeaks = [1122, 992, 870, 756, 650, 552, 462]
    
    background = 0
    backgroundlist = []

    maskb = (x >= 392.0) & (x <= 392.5)
    for yi in y[maskb]:
        backgroundlist.append(yi)
    background = np.mean(backgroundlist)

    tolerance = 0.08
    for key in [f"L{i}" for i in range(1, 8)]:
        center = wavelength_subpeaks[key]
        mask = (x >= center - tolerance) & (x <= center + tolerance)
        if np.any(mask):
            peaks.append(np.max(y[mask]- background))
        else:
            print(f"Warning: No x values found for {key} in interval [{center-tolerance}, {center+tolerance}]")  # or handle missing data as you prefer
            peaks.append(np.nan)

    log_i_A = [np.log10(peaks[i]/crosssection_subpeaks[f"L{i+1}"]) for i in range(len(peaks))]

    slope, intercept, r_value, p_value, std_err = linregress(energy_subpeaks, log_i_A)

    #-1.296 is the factor used to convert the slope to temperature in Kelvin
    temperature = -1.296 / slope
    error = (std_err * 1.296) / (slope * slope)  # Error of the slope
    return temperature, error, r_value, p_value, intercept