from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import ttk, filedialog
from compute_stats import compute_stats
from save_normalized_spectra import save_normalized_spectra
from normalize_spectra import normalize_spectra
from find_peaks import find_peaks
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt

def plot_with_offset(datasets):

    offsets = [0]*len(datasets) # Start with an initial offset of 0 for the first dataset

    # Create the main window
    # Create a Tkinter window
    # Set the title of the window
    root = tk.Tk()
    root.title("Plot with X-Axis Offset Adjustment")

    # Create a Matplotlib figure
    # Create a figure and axis for the plot
    # Set the size of the figure
    #fig, ax = plt.subplots(nrows, ncols, figsize=(width, height))
    fig, ax = plt.subplots()
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_title("Plot with Offset Adjustment")
    ax.grid(True)

    # Function to open a new file and add its data
    #def open_file():
    #    if len(datasets) >= 3:
    #        tk.messagebox.showerror("Error", "You can only load up to 3 datasets.")
    #        return
    #    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        # if not file_path:
        #     return
        # try:
        #     # Load the data from the selected file
        #     # Unpack the data into x and y variables
        #     x, y = np.loadtxt(file_path, unpack=True)
        #     # datasets: A list to store the datasets (x, y pairs).
        #     # It has the structure [(x1, y1), (x2, y2), ...]
        #     # offsets: A list to store the offsets for each dataset.
        #     datasets.append((x, y))
        #     update_offset(len(datasets) - 1, 0)
        # except Exception as e:
        #     tk.messagebox.showerror("Error", f"Failed to load file: {e}")

    # Embed the Matplotlib figure in the Tkinter window
    # FigureCanvasTkAgg: This is a Matplotlib backend that allows a Matplotlib figure to be rendered inside a Tkinter GUI.
    # fig: The Matplotlib figure object that you want to display.
    # master=root: Specifies the parent widget (in this case, the Tkinter window root) where the figure will be embedded.
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # Add the Matplotlib navigation toolbar for zoom and pan functionality
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()
    toolbar.pack(side=tk.TOP, fill=tk.X)

    # Function to update the plot with offsets
    def update_plot():
        ax.clear()
        for i, (x, y) in enumerate(datasets):
            adjusted_x = [xi + offsets[i] for xi in x]
            ax.plot(adjusted_x, y, label=f"Dataset {i+1}")
        ax.legend()
        ax.grid(True)
        canvas.draw()

    update_plot()  # Initial plot with offsets at zero

    # Function to update the plot when the offset slider changes
    # Added the variable index to the function signature to identify which dataset is being adjusted
    # The function takes an index and an offset value as arguments
    def update_offset(index, offset):
        offsets[index] = float(offset)
        ax.clear()
        for i, (x, y) in enumerate(datasets):
            adjusted_x = [xi + offsets[i] for xi in x]
            ax.plot(adjusted_x, y, label=f"Dataset {i+1}")
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.set_title("Plot with Offset Adjustment")
        ax.legend()
        ax.grid(True)
        canvas.draw()

    # Add controls for each dataset for offset adjustment
    control_frame = ttk.Frame(root)
    control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    # Dropdown menu to select the dataset
    # Dropdown menu to select the dataset
    selected_dataset = tk.StringVar()
    if datasets:
        selected_dataset.set("Dataset 1")  # Default to the first dataset
    else:
        selected_dataset.set("Select Dataset")  # Default if no datasets are available

    dataset_dropdown = ttk.OptionMenu(
        control_frame,
        selected_dataset,
        *[f"Dataset {i+1}" for i in range(len(datasets))]
    )
    dataset_dropdown.pack(side=tk.LEFT, padx=5)

    # Entry for manual offset adjustment
    offset_entry = ttk.Entry(control_frame, width=10)
    offset_entry.pack(side=tk.LEFT, padx=5)
    offset_entry.insert(0, "0.0")  # Default value

    # Button to apply the offset from the entry
    def apply_offset():
        try:
            # Validate the selected dataset
            selected_value = selected_dataset.get()
            if not selected_value.startswith("Dataset"):
                raise ValueError("Invalid dataset selected.")

            # Extract the dataset index from the dropdown menu
            dataset_index = int(selected_value.split()[-1]) - 1  # Extract dataset index from dropdown
            if dataset_index < 0 or dataset_index >= len(datasets):
                raise IndexError("Dataset index out of range.")

            # Validate the offset input
            offset = float(offset_entry.get())  # Get the offset value from the entry
            update_offset(dataset_index, offset)  # Update the offset for the selected dataset
        except ValueError:
            tk.messagebox.showerror("Error", "Please select a valid dataset and enter a valid number.")
        except IndexError:
            tk.messagebox.showerror("Error", "Selected dataset is out of range.")
    
    ttk.Button(control_frame, text="Apply Offset", command=apply_offset).pack()

    #Automatically store the normalized spectra for further calculations
    [common_x, normalized_avg_y, std_dev_y]=normalize_spectra(datasets, offsets)

    # Add buttons for file loading and statistics computation
    button_frame = ttk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    ttk.Button(button_frame, text="Compute Stats", command=lambda: compute_stats(datasets, offsets, ax, canvas)).pack(side=tk.RIGHT, padx=5)
    ttk.Button(button_frame, text="Save Normalized Spectra", command=lambda: save_normalized_spectra(datasets, offsets)).pack(side=tk.RIGHT, padx=5)

    ##############################################################
    ##############################################################
    ##############################################################
    temperature=0

    # Add a label to display the temperature
    temperature_label = tk.Label(root, text=f"Gas Temperature: {temperature}°C", font=("Arial", 12))
    temperature_label.pack(side=tk.BOTTOM, pady=10)

    # Run the Tkinter event loop
    root.mainloop()

    #Queda meter las ecuaciones de la temperatura y meter cosillas para calcular densidad electronica 