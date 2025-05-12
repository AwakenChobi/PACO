from tkinter import filedialog
import tkinter as tk
import numpy as np

def save_normalized_spectra(datasets, offsets):
    if len(datasets) < 1:
        tk.messagebox.showerror("Error", "You need at least 1 dataset to save the normalized-averaged spectra.")
        return

    # Adjust x values with offsets
    adjusted_data = [
        ([xi + offsets[i] for xi in x], y) for i, (x, y) in enumerate(datasets)
    ]

    # Interpolate to align x values
    num_points = len(adjusted_data[0][0])  # Use the number of points in the first dataset
    common_x = np.linspace(
        min(min(x for x, _ in adjusted_data)), max(max(x for x, _ in adjusted_data)), num_points
    )
    # Interpolate y values for each dataset to the common x values
    # np.interp(x, xp, fp):
    # x: The x-coordinates at which to evaluate the interpolated values.
    # xp: The x-coordinates of the data points. These are the x values of the datasets.
    # fp: The y-coordinates of the data points. These are the y values of the datasets.
    interpolated_y = [
        np.interp(common_x, [xi + offsets[i] for xi in x], y)
        for i, (x, y) in enumerate(adjusted_data)
    ]
    avg_y = np.mean(interpolated_y, axis=0)

    # Compute the standard deviation for each x value
    std_dev_y = np.std(interpolated_y, axis=0)

    # Normalize the averaged spectra
    normalized_avg_y = avg_y / np.max(avg_y)


    print("Maximum value of avg_y before normalization:", np.max(avg_y))
    print("Maximum value of avg_y after normalization (should be 1):", np.max(normalized_avg_y))


    # Ask the user where to save the file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")],
        title="Save Normalized-Averaged Spectra"
    )
    if not file_path:
        return  # User canceled the save dialog

    # Save the data to the file
    try:
        np.savetxt(
            file_path,
            np.column_stack((common_x, normalized_avg_y, std_dev_y)),
            header="X Normalized_Averaged_Y Std_Dev_Y",
            fmt="%.9f"  # Use fixed-point notation with 9 decimal places
        ) 
        tk.messagebox.showinfo("Success", f"File saved successfully at {file_path}")
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to save file: {e}")