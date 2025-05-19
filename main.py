# This script creates a scatter plot using Matplotlib and allows the user to adjust the x-axis offset using a slider in a Tkinter GUI.
# Import necessary libraries
from tkinter import filedialog
from plot_with_offset import plot_with_offset
import tkinter as tk
import numpy as np

# Ask the user to select a file

# Open a file dialog to select multiple .txt files
file_paths = filedialog.askopenfilenames(
    title="Select Data Files",
    filetypes=[("Text Files", "*.txt")]
)
    
if not file_paths:
    tk.messagebox.showinfo("Info", "No files selected.")
    exit()

datasets = []
try:
    for file_path in file_paths:
        # Load data from each file (assuming two columns: x and y)
        data = np.loadtxt(file_path)
        x, y = data[:, 0], data[:, 1]
        datasets.append((x, y))
except Exception as e:
    tk.messagebox.showerror("Error", f"Failed to load files: {e}")
    exit()

# Initialize the Tkinter window
plot_with_offset(datasets)