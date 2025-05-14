from tkinter import filedialog
from scipy.signal import find_peaks
import tkinter.simpledialog as simpledialog
import tkinter as tk
import numpy as np
#from find_peaks import find_peaks

def save_normalized_peaks(common_x, normalized_avg_y, std_dev_y):

    #############################################################################################################################################################################################################################################################################################################
    #https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html
    #find_peaks(x, height=None, threshold=None, distance=None, prominence=None, width=None, wlen=None, rel_height=0.5, plateau_size=None)
        #x (sequence): A signal with peaks.
        #height (number or ndarray or sequence, optional): Required height of peaks. Either a number, None, an array matching x or a 2-element sequence of the former. The first element is always interpreted as the minimal and the second, if supplied, as the maximal required height.
        #threshold (number or ndarray or sequence, optional): Required threshold of peaks. Either a number, None, an array matching x or a 2-element sequence of the former. The first element is always interpreted as the minimal and the second, if supplied, as the maximal required threshold.
        #distance (number, optional): Required minimal horizontal distance between neighboring peaks. The distance is measured in number of samples.
        #prominence (number or ndarray or sequence, optional): Required prominence of peaks. Either a number, None, an array matching x or a 2-element sequence of the former. The first element is always interpreted as the minimal and the second, if supplied, as the maximal required prominence.
        #width (number or ndarray or sequence, optional): Required width of peaks. Either a number, None, an array matching x or a 2-element sequence of the former. The first element is always interpreted as the minimal and the second, if supplied, as the maximal required width.
        #wlen (int, optional): Window length used for the computation of the prominence. If None, the window length is set to the size of the input signal.
        #rel_height (float, optional): Used for calculation of the peaks width, thus it is only used if width is given. See argument rel_height in peak_widths for a full description of its effects.
        #plateau_size (number or ndarray or sequence, optional): Required size of the plateau. Either a number, None, an array matching x or a 2-element sequence of the former. The first element is always interpreted as the minimal and the second, if supplied, as the maximal required size.
    #Returns:
        #peaks (ndarray): Indices of the peaks in x. The length of peaks is equal to the number of peaks found.
        #properties (dict): A dictionary of properties of the peaks. The keys are the names of the properties and the values are arrays of the same length as peaks. The properties are:
            #'peak_heights': If height is given, the height of each peak in x.
            #'left_threshold','right_threshold': If threshold is given, these keys contain a peaks vertical distance to its neighbouring samples.
            #'prominences', 'right_bases', 'left_bases': If prominence is given, these keys are accessible. See peak_prominences for a description of their content.
            #'widths', 'width_heights', 'left_ips', 'right_ips': If width is given, these keys are accessible. See peak_widths for a description of their content.
            #'plateau_sizes', 'left_edges', 'right_edges': If plateau_size is given, these keys are accessible and contain the indices of a peak’s edges (edges are still part of the plateau) and the calculated plateau sizes.
    ##############################################################################################################################################################################################################################################################################################################
    
    # Editor's note: The function find_peaks takes a 1D array (e.g. the y data of a spectrum) and returns the INDICES of the peaks in that array

    num_normalized_avg_y = np.array(normalized_avg_y)
    height=0.00075
    # Ask the user for the minimum threshold
    height = simpledialog.askfloat(
        "Peak Threshold",
        "Enter minimum height for peaks:",
        initialvalue=0.00075,
        minvalue=0.0
    )
    peaks, _=find_peaks(num_normalized_avg_y, height)  # Find peaks in the normalized average y data

    # Ask the user where to save the file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        title="Save Normalized-Averaged Peaks"
    )
    if not file_path:
        return  # User canceled the save dialog

    peak_indices = [i for i, x in enumerate(common_x) if i in peaks]
    data_to_save = np.column_stack((
        common_x[peak_indices],
        normalized_avg_y[peak_indices],
        std_dev_y[peak_indices]
    ))

    # Save the data to the file
    try:
        np.savetxt(
            file_path,
            data_to_save,
            header="X Normalized_Averaged_Y Std_Dev_Y",
            fmt="%.9f"  # Use fixed-point notation with 9 decimal places
        ) 
        tk.messagebox.showinfo("Success", f"File saved successfully at {file_path}")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to save file: {e}")