# This script creates a scatter plot using Matplotlib and allows the user to adjust the x-axis offset using a slider in a Tkinter GUI.
# Import necessary libraries
import sys
from tkinter import filedialog
from plot_with_offset import plot_with_offset
import tkinter as tk
import numpy as np

def main():
    try:
        file_paths = filedialog.askopenfilenames(
            title="Select Data Files",
            filetypes=[("Text Files", "*.txt")]
        )
            
        if not file_paths:
            tk.messagebox.showinfo("Info", "No files selected.")
            return

        datasets = []
        for file_path in file_paths:
            data = np.loadtxt(file_path)
            x, y = data[:, 0], data[:, 1]
            datasets.append((x, y))

        plot_with_offset(datasets)
        
    except KeyboardInterrupt:
        print("Interrupted by user.")
        sys.exit(0)
    except Exception as e:
        tk.messagebox.showerror("Error", f"Failed to load files: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()