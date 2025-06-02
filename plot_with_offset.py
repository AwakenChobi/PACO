from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import ttk
from compute_stats import compute_stats
from save_normalized_spectra import save_normalized_spectra
from normalize_spectra import normalize_spectra
from saturated_lines_searcher import saturated_lines_searcher
from scipy.signal import find_peaks
from save_peaks import save_normalized_peaks
import tkinter as tk
import tkinter.simpledialog as simpledialog
import matplotlib.pyplot as plt

def plot_with_offset(datasets):

    offsets = [0]*len(datasets) # Start with an initial offset of 0 for the first dataset

    # Create the main window
    # Create a Tkinter window
    # Set the title of the window
    root = tk.Tk()
    root.title("Plot with X-Axis Offset Adjustment")

    #Atomic lines detected in Atm press Argon plasmas in TIAGO 
    # REF: NIST atomic spectra database:
    Ar_lines=[430.0, 560.6, 696.5, 706.72175,720.6980, 727.2936, 731.1716, 731.6005, 737.2118, 738.3980]
    C_lines=[247.85612, 296.72240, 426.90197, 538.03308]
    N_lines=[740.612, 740.624, 742.364, 744.229, 821.6]
    H_lines=[486.1, 656.279]
    O_lines=[725.415, 725.445, 725.453, 777.2]

    #Molecular head bands detected in Atm press Argon plasmas in TIAGO:
    # REF: Spectroscopic characterization of atmospheric pressure argon plasmas sustained with the Torche à Injection Axiale sur Guide d'Ondes 
    #      R. Rincón, J. Muñoz ⁎, M. Sáez, M.D. Calzada, 2013
    N2_head_bands=[315.8, 357.7, 405.9, 420.05]
    CN_head_bands=[386.2, 387.1, 388.3,460.4, 460.7]
    OH_head_bands=[306.4, 308.9]
    NO_head_bands=[237.0, 247.9, 259.6]
    N2_head_bands=[315.8, 357.7, 391, 405.9, 420.05]
    CO_head_bands=[297.7]
    # REF: The Identification of Molecular Spectra, 2nd Edition, 1976, Pearse and Gaydon
    C2_head_bands=[516.2, 563.5]

    #Dictionary of references
    reference_lines_dict = {
        "Ar lines": Ar_lines,
        "C lines": C_lines,
        "N lines": N_lines,
        "H lines": H_lines,
        "O lines": O_lines,
        "N2 head bands": N2_head_bands,
        "CN head bands": CN_head_bands,
        "OH head bands": OH_head_bands,
        "NO head bands": NO_head_bands,
        "CO head bands": CO_head_bands,
        "C2 head bands": C2_head_bands,
    }

    reference_lines_colors = {
        "Ar lines": "purple",
        "C lines": "black",
        "N lines": "orange",
        "H lines": "blue",
        "O lines": "green",
        "N2 head bands": "red",
        "CN head bands": "magenta",
        "OH head bands": "cyan",
        "NO head bands": "brown",
        "CO head bands": "gray",
        "C2 head bands": "olive",
    }

    #Automatically store the normalized spectra (and substracted) for further calculations
    [common_x, normalized_avg_y, std_dev_y]=normalize_spectra(datasets, offsets)

    # Create a Matplotlib figure
    # Create a figure and axis for the plot
    # Set the size of the figure
    #fig, ax = plt.subplots(nrows, ncols, figsize=(width, height))
    fig, ax = plt.subplots()
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_title("Plot with Offset Adjustment")
    ax.grid(True)

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

    def toggle_saturated_lines():
        show_saturated_lines[0] = not show_saturated_lines[0]
        # Remove old lines
        for artist in saturated_lines_artists:
            artist.remove()
        saturated_lines_artists.clear()
        if show_saturated_lines[0]:
            # Get all saturated x positions from all datasets
            for i, (x, y) in enumerate(datasets):
                saturated_x = saturated_lines_searcher(x+offsets[i], y)
                for sx in saturated_x:
                    line = ax.axvline(sx, color='red', linestyle='--', linewidth=1.5)
                    saturated_lines_artists.append(line)
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

    #State for toggling and storing artists
    show_ref_lines = [False]
    ref_lines_artists = []

    show_saturated_lines = [False]
    saturated_lines_artists = []

    # Add controls for each dataset for offset adjustment
    control_frame = ttk.Frame(root)
    control_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

    #Add dropdown for reference lines selection
    selected_ref_lines = tk.StringVar()
    selected_ref_lines.set("Ar lines")  # Default selection
    ref_dropdown = ttk.OptionMenu(control_frame, selected_ref_lines,"Ar lines", *reference_lines_dict.keys())
    ref_dropdown.pack(side=tk.LEFT, padx=5)


    # Dropdown menu to select the dataset
    # Dropdown menu to select the dataset
    selected_dataset = tk.StringVar()
    if datasets:
        selected_dataset.set("Dataset 1")  # Default to the first dataset
    else:
        selected_dataset.set("Select Dataset")  # Default if no datasets are available

    dataset_options = [f"Dataset {i+1}" for i in range(len(datasets))]
    selected_dataset = tk.StringVar(value=dataset_options[0] if dataset_options else "Select Dataset")

    dataset_dropdown = ttk.OptionMenu(
        control_frame,
        selected_dataset,
        dataset_options[0] if dataset_options else "Select Dataset",
        *dataset_options
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

    # State variable for plot mode: 0 = datasets, 1 = normalized
    plot_mode = [0]  # Use a list for mutability in nested functions

    def update_plot_mode():
        ax.clear()
        if plot_mode[0] == 0:
            # Plot all datasets with offsets
            for i, (x, y) in enumerate(datasets):
                adjusted_x = [xi + offsets[i] for xi in x]
                ax.plot(adjusted_x, y, label=f"Dataset {i+1}")
            ax.set_title("Plot with Offset Adjustment")
        else:
            # Plot normalized averaged spectrum
            nonlocal common_x, normalized_avg_y, std_dev_y
            [common_x, normalized_avg_y, std_dev_y]=normalize_spectra(datasets, offsets)
            ax.plot(common_x, normalized_avg_y, label="Normalized Averaged Spectrum", color="black")
            ax.set_title("Normalized Averaged Spectrum")
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.legend()
        ax.grid(True)
        canvas.draw()

    peaks_artist = [None]

    def plot_peaks_on_normalized():
        # Ask the user for the minimum threshold
        min_height = simpledialog.askfloat(
            "Peak Threshold",
            "Enter minimum height for peaks:",
            initialvalue=0.00075,
            minvalue=0.0
        )
        if min_height is None:
            min_height = 0.00075  # Default if user cancels

        # Clear previous peaks if any
        if peaks_artist[0] is not None:
            peaks_artist[0].remove()
            peaks_artist[0] = None

        # Compute peaks
        peaks, _ = find_peaks(normalized_avg_y, height=min_height)
        # Plot the peaks as red 'x' markers
        peaks_artist[0] = ax.scatter(common_x[peaks], normalized_avg_y[peaks], color='red', marker='x', label='Peaks')
        ax.legend()
        canvas.draw()


    def toggle_plot_mode():
        plot_mode[0] = 1 - plot_mode[0]  # Toggle between 0 and 1
        update_plot_mode()

    # Replace calls to update_plot() with update_plot_mode()
    update_plot_mode()  # Initial plot

    # Add buttons for file loading and statistics computation
    button_frame = ttk.Frame(root)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    ttk.Button(button_frame, text="Compute Stats", command=lambda: compute_stats(datasets, offsets, ax, canvas)).pack(side=tk.RIGHT, padx=5)
    ttk.Button(button_frame, text="Save Normalized Spectra", command=lambda: save_normalized_spectra(datasets, offsets)).pack(side=tk.RIGHT, padx=5)
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    ttk.Button(button_frame, text="Save Normalized Peaks", command=lambda: save_normalized_peaks(common_x, normalized_avg_y, std_dev_y)).pack(side=tk.RIGHT, padx=5)
    ttk.Button(button_frame, text="Toggle Plot Mode", command=toggle_plot_mode).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Compute & Plot Peaks", command=plot_peaks_on_normalized).pack(side=tk.LEFT, padx=5)

    ##############################################################
    ##############################################################
    ##############################################################
    temperature=0

    show_saturated_lines = [False]
    saturated_lines_artists = []

    def toggle_saturated_lines():
        show_saturated_lines[0] = not show_saturated_lines[0]
        for artist in saturated_lines_artists:
            artist.remove()
        saturated_lines_artists.clear()
        if show_saturated_lines[0]:
            for i, (x, y) in enumerate(datasets):
                saturated_x = saturated_lines_searcher(x, y)
                for sx in saturated_x:
                    line = ax.axvline(sx, color='red', linestyle='--', linewidth=1.5)
                    saturated_lines_artists.append(line)
        canvas.draw()

    ttk.Button(button_frame, text="Toggle Saturated Lines", command=toggle_saturated_lines).pack(side=tk.RIGHT, padx=5)

    # Function automatically update the reference lines when the dropdown changes
    def on_ref_dropdown_change(*args):
        if show_ref_lines[0]:
            # Remove old lines
            for artist in ref_lines_artists:
                artist.remove()
            ref_lines_artists.clear()
            ref_name = selected_ref_lines.get()
            ref_xs = reference_lines_dict[ref_name]
            color = reference_lines_colors.get(ref_name, "orange")
            for x in ref_xs:
                line = ax.axvline(x, color=color, linestyle=':', linewidth=1.5)
                ref_lines_artists.append(line)
            canvas.draw()

    selected_ref_lines.trace_add("write", on_ref_dropdown_change)

    # Function to toggle reference lines (without on_ref_dropdown_change, it won't automatically update but it still works)
    def toggle_reference_lines():
        show_ref_lines[0] = not show_ref_lines[0]
        # Remove old lines
        for artist in ref_lines_artists:
            if hasattr(artist, "remove"):
                try:
                    artist.remove()
                except NotImplementedError:
                    pass  # Ignore artists that cannot be removed
        ref_lines_artists.clear()
        if show_ref_lines[0]:
            ref_name = selected_ref_lines.get()
            ref_xs = reference_lines_dict[ref_name]
            color = reference_lines_colors.get(ref_name, "orange")  # Default to orange if not found
            for x in ref_xs:
                line = ax.axvline(x, color=color, linestyle=':', linewidth=1.5)
                ref_lines_artists.append(line)
        canvas.draw()

    # Add the toggle button for reference lines/bands
    ttk.Button(control_frame, text="Toggle Reference Lines", command=toggle_reference_lines).pack(side=tk.LEFT, padx=5)

    # Add a label to display the temperature
    temperature_label = tk.Label(root, text=f"Gas Temperature: {temperature}°C", font=("Arial", 12))
    temperature_label.pack(side=tk.BOTTOM, pady=10)

    # Run the Tkinter event loop
    root.mainloop()

    #Queda meter las ecuaciones de la temperatura y meter cosillas para calcular densidad electronica 