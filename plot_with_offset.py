from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from tkinter import ttk, messagebox
from compute_stats import compute_stats
from save_normalized_spectra import save_normalized_spectra
from normalize_spectra import normalize_spectra
from saturated_lines_searcher import saturated_lines_searcher
from read_xy_file import read_xy_file
from scipy.signal import find_peaks
from save_peaks import save_normalized_peaks
from rot_temperature import rot_temperature_C2, rot_temperature_OH, rot_temperature_N2_plus
import tkinter as tk
import tkinter.simpledialog as simpledialog
import tkinter.filedialog as filedialog
import matplotlib.pyplot as plt
import numpy as np

def plot_with_offset(datasets):
    
    adjusted_datasets = []
    for idx, (x, y) in enumerate(datasets):
        x = np.array(x)
        y = np.array(y)
        mask = (x >= 104) & (x <= 105)
        if np.any(mask):
            background = np.mean(y[mask])
        else:
            background = 0  #### edit backgroud manually

        # If background is above 30, warn and allow manual input
        if background > 30:
            msg = (f"Dataset {idx+1}: The computed background value is {background:.2f}, "
                "which is above 30.\nIt is possible that the background is not well computed.\n"
                "Would you like to input the background value manually?")
            if messagebox.askyesno("Background Warning", msg):
                manual_bg = simpledialog.askfloat(
                    "Manual Background Input",
                    f"Enter background value for Dataset {idx+1}:",
                    initialvalue=background
                )
                if manual_bg is not None:
                    background = manual_bg

        y_adjusted = y - background
        adjusted_datasets.append((x, y_adjusted))
    datasets = adjusted_datasets

    offsets = [0]*len(datasets) # Variable to store offsets for each dataset

    root = tk.Tk()
    root.title("Plot with X-Axis Offset Adjustment")
    
    # Add proper window closing handler
    def on_closing():
        """Handle window closing properly"""
        try:
            root.quit()  # Stop the mainloop
            root.destroy()  # Destroy the window
        except:
            pass
        finally:
            import sys
            sys.exit(0)  # Ensure the program exits
    
    root.protocol("WM_DELETE_WINDOW", on_closing)

    #Atomic lines detected in Atm press Argon plasmas in TIAGO 
    # REF: NIST atomic spectra database:
    Ar_lines=[430.0, 560.6, 696.5, 706.72175,720.6980, 727.2936, 731.1716, 731.6005, 737.2118, 738.3980]
    C_lines=[247.85612, 258.289728, 296.72240, 426.90197, 538.03308]
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
    C2_head_bands=[516.5, 563.5]
    C2_molecular_bands=[516.5, 563.5]
    
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
    [common_x, avg_y, std_dev_y, normalized_avg_y, normalized_std_dev_y]=normalize_spectra(datasets, offsets)

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

    def open_new_files():
        nonlocal datasets, offsets, show_dataset_vars, checkbox_frame, common_x, avg_y, std_dev_y, normalized_avg_y, normalized_std_dev_y

        filepaths = filedialog.askopenfilenames(
            title="Open Data Files",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not filepaths:
            return  # User cancelled

        # Read new datasets
        new_datasets = []
        for fp in filepaths:
            try:
                x, y = read_xy_file(fp)
                new_datasets.append((np.array(x), np.array(y)))
            except Exception as e:
                messagebox.showerror("File Error", f"Could not read {fp}:\n{e}")
                return

        # Adjust background for each new dataset (reuse your background subtraction logic)
        adjusted_datasets = []
        for idx, (x, y) in enumerate(new_datasets):
            mask = (x >= 104) & (x <= 105)
            background = np.mean(y[mask]) if np.any(mask) else 0
            if background > 30:
                msg = (f"Dataset {idx+1}: The computed background value is {background:.2f}, "
                       "which is above 30.\nIt is possible that the background is not well computed.\n"
                       "Would you like to input the background value manually?")
                if messagebox.askyesno("Background Warning", msg):
                    manual_bg = simpledialog.askfloat(
                        "Manual Background Input",
                        f"Enter background value for Dataset {idx+1}:",
                        initialvalue=background
                    )
                    if manual_bg is not None:
                        background = manual_bg
            y_adjusted = y - background
            adjusted_datasets.append((x, y_adjusted))

        # Replace datasets and reset offsets and checkboxes
        datasets = adjusted_datasets
        offsets[:] = [0] * len(datasets)
        show_dataset_vars[:] = [tk.BooleanVar(value=True) for _ in datasets]

        # Remove old checkboxes and add new ones
        for widget in checkbox_frame.winfo_children():
            widget.destroy()
        for i in range(len(datasets)):
            cb = ttk.Checkbutton(
                checkbox_frame,
                text=f"Show Dataset {i+1}",
                variable=show_dataset_vars[i],
                command=update_plot_mode
            )
            cb.pack(side=tk.LEFT)

        # Update normalized spectra and plot
        [common_x, avg_y, std_dev_y, normalized_avg_y, normalized_std_dev_y] = normalize_spectra(datasets, offsets)
        update_plot_mode()

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
    plot_mode = [0]

    show_dataset_vars = [tk.BooleanVar(value=True) for _ in datasets]

    # This list will hold the colors for each dataset. It would be a problem if there are more datasets than colors (10).
    # If that happens, the colors will repeat.
    dataset_colors = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "olive", "cyan"]

    def update_plot_mode():
        ax.clear()
        if plot_mode[0] == 0:
            # Plot all datasets with offsets, only those checked
            for i, (x, y) in enumerate(datasets):
                if show_dataset_vars[i].get():
                    adjusted_x = [xi + offsets[i] for xi in x]
                    color = dataset_colors[i % len(dataset_colors)]
                    ax.plot(adjusted_x, y, label=f"Dataset {i+1}", color=color)
            ax.set_title("Plot with Offset Adjustment")
        else:
            # Plot
            nonlocal common_x, avg_y, std_dev_y, normalized_avg_y, normalized_std_dev_y
            [common_x, avg_y, std_dev_y, normalized_avg_y, normalized_std_dev_y] = normalize_spectra(datasets, offsets)
            ax.plot(common_x, normalized_avg_y, label="Normalized Averaged Spectrum", color="black")
            ax.set_title("Normalized Averaged Spectrum")
        ax.set_xlabel("X Axis")
        ax.set_ylabel("Y Axis")
        ax.legend()
        ax.grid(True)
        canvas.draw()

    update_plot_mode()

    peaks_artist = [None]

    def plot_peaks_on_normalized():
        # Ask the user for the minimum threshold, useful when the ground noise is irregular
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

        # Compute peaks and plot them as x
        peaks, _ = find_peaks(normalized_avg_y, height=min_height)
        peaks_artist[0] = ax.scatter(common_x[peaks], normalized_avg_y[peaks], color='red', marker='x', label='Peaks')
        ax.legend()
        canvas.draw()


    def toggle_plot_mode():
        plot_mode[0] = 1 - plot_mode[0]
        update_plot_mode()

    update_plot_mode()

    # Buttons for file loading and statistics computation
    button_frame = ttk.Frame(root)

    button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    ttk.Button(button_frame, text="Compute Stats", command=lambda: compute_stats(datasets, offsets, ax, canvas)).pack(side=tk.RIGHT, padx=5)
    ttk.Button(button_frame, text="Save Normalized Spectra", command=lambda: save_normalized_spectra(datasets, offsets)).pack(side=tk.RIGHT, padx=5)
    #root = tk.Tk()
    #root.withdraw()  # Hide the main window
    ttk.Button(button_frame, text="Save Normalized Peaks", command=lambda: save_normalized_peaks(common_x, avg_y, std_dev_y, normalized_avg_y, normalized_std_dev_y)).pack(side=tk.RIGHT, padx=5)
    ttk.Button(button_frame, text="Toggle Plot Mode", command=toggle_plot_mode).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Compute & Plot Peaks", command=plot_peaks_on_normalized).pack(side=tk.LEFT, padx=5)

    #Temperature computation
    temperature=0

    # Add dropdown for temperature computation method
    temp_methods = ["C2 (averaged)", "N2+ (averaged)", "OH (averaged)", "C2 (1 by 1)", "N2+ (1 by 1)", "OH (1 by 1)"]
    selected_temp_method = tk.StringVar()
    selected_temp_method.set(temp_methods[0])
    temp_method_dropdown = ttk.OptionMenu(control_frame, selected_temp_method, temp_methods[0], *temp_methods)
    temp_method_dropdown.pack(side=tk.LEFT, padx=5)

    # Function to compute and display temperature
    def compute_temperature():
        method = selected_temp_method.get()
        if "averaged" in method:
            if "C2" in method:
                temperature, error, *_ = rot_temperature_C2(common_x, normalized_avg_y)
            elif "N2+" in method:
                temperature, error, *_ = rot_temperature_N2_plus(common_x, normalized_avg_y)
            elif "OH" in method:
                temperature, error, *_ = rot_temperature_OH(common_x, normalized_avg_y)
            else:
                temperature, error = None, None
        elif "1 by 1" in method:
            temps = []
            errs = []
            for i, (x, y) in enumerate(datasets):
                x_offset = [xi + offsets[i] for xi in x]
                if "C2" in method:
                    t, e, *_ = rot_temperature_C2(x_offset, y)
                elif "N2+" in method:
                    t, e, *_ = rot_temperature_N2_plus(x_offset, y)
                elif "OH" in method:
                    t, e, *_ = rot_temperature_OH(x_offset, y)
                else:
                    t, e = None, None
                if t is not None:
                    temps.append(t)
                    errs.append(e)
            if temps:
                temperature = np.mean(temps)
                error = np.sqrt(np.sum(np.array(errs)**2)) / len(errs)  # combine errors
            else:
                temperature, error = None, None
        else:
            temperature, error = None, None

        if temperature is not None:
            temperature_label.config(text=f"Gas Temperature: {temperature:.1f} K ± {error:.1f} K")
        else:
            temperature_label.config(text="Temperature calculation failed.")

    # Add button to compute temperature
    ttk.Button(control_frame, text="Compute Temperature", command=compute_temperature).pack(side=tk.LEFT, padx=5)


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
            color = reference_lines_colors.get(ref_name, "orange")
            for x in ref_xs:
                line = ax.axvline(x, color=color, linestyle=':', linewidth=1.5)
                ref_lines_artists.append(line)
        canvas.draw()

    # Add the toggle button for reference lines/bands
    ttk.Button(control_frame, text="Toggle Reference Lines", command=toggle_reference_lines).pack(side=tk.LEFT, padx=5)

    # Add a label to display the temperature
    temperature_label = tk.Label(root, text=f"Gas Temperature: {temperature}°C", font=("Arial", 12))
    temperature_label.pack(side=tk.BOTTOM, pady=10)

    # Add a menu bar with an "Open" and "Exit" option
    menubar = tk.Menu(root)
    filemenu = tk.Menu(menubar, tearoff=0)
    filemenu.add_command(label="Open New Files", command=open_new_files)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)

    # Add checkboxes for each dataset
    checkbox_frame = ttk.Frame(control_frame)
    checkbox_frame.pack(side=tk.LEFT, padx=5)
    for i in range(len(datasets)):
        cb = ttk.Checkbutton(
            checkbox_frame,
            text=f"Show Dataset {i+1}",
            variable=show_dataset_vars[i],
            command=update_plot_mode
        )
        cb.pack(side=tk.LEFT)

    root.mainloop()