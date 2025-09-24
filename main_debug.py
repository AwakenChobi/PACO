# Debug version of main.py to identify bottlenecks
import time

def print_timing(message, start_time):
    elapsed = time.time() - start_time
    print(f"[{elapsed:.2f}s] {message}")
    return time.time()

print("PACO Debug Version - Tracking execution time")
print("=" * 60)

overall_start = time.time()
step_start = time.time()

print("Step 1: Importing libraries...")
step_start = print_timing("Starting imports", step_start)

from tkinter import filedialog
step_start = print_timing("  ✓ tkinter.filedialog imported", step_start)

import tkinter as tk
step_start = print_timing("  ✓ tkinter imported", step_start)

import numpy as np
step_start = print_timing("  ✓ numpy imported", step_start)

from plot_with_offset import plot_with_offset
step_start = print_timing("  ✓ plot_with_offset imported (this may be slow!)", step_start)

print("\nStep 2: Opening file selection dialog...")
file_paths = filedialog.askopenfilenames(
    title="Select Data Files",
    filetypes=[("Text Files", "*.txt")]
)
step_start = print_timing("  ✓ File dialog completed", step_start)

if not file_paths:
    print("No files selected. Exiting.")
    exit()

print(f"Selected {len(file_paths)} files:")
for i, fp in enumerate(file_paths, 1):
    print(f"  {i}. {fp.split('/')[-1] if '/' in fp else fp.split('\\')[-1]}")

print(f"\nStep 3: Loading {len(file_paths)} data files...")
datasets = []
try:
    for i, file_path in enumerate(file_paths):
        file_start = time.time()
        data = np.loadtxt(file_path)
        x, y = data[:, 0], data[:, 1]
        datasets.append((x, y))
        file_time = time.time() - file_start
        print(f"  ✓ File {i+1}: {len(x):,} points loaded in {file_time:.2f}s")
        
except Exception as e:
    tk.messagebox.showerror("Error", f"Failed to load files: {e}")
    exit()

step_start = print_timing("  ✓ All data files loaded", step_start)

print("\nStep 4: Starting GUI...")
plot_with_offset(datasets)
step_start = print_timing("  ✓ GUI started", step_start)

total_time = time.time() - overall_start
print(f"\n" + "=" * 60)
print(f"TOTAL EXECUTION TIME: {total_time:.2f} seconds")
print("=" * 60)