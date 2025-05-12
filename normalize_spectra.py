from tkinter import filedialog
import tkinter as tk
import numpy as np

def normalize_spectra(datasets, offsets):

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
    return common_x, normalized_avg_y, std_dev_y