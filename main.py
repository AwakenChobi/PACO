import time
import sys
import os
import numpy as np
from read_xy_file import read_xy_file

print("PACO Data Analyzer")
print("=" * 50)
startup_time = time.time()

def lazy_import_and_setup():
    print("Loading libraries...")
    
    import numpy as np
    print("  ✓ NumPy loaded")
    
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    print("  ✓ Tkinter loaded")
    
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    print("  ✓ Matplotlib loaded")
    
    from scipy.signal import find_peaks
    print("  ✓ Scipy loaded")
    
    return {
        'np': np,
        'tk': tk,
        'filedialog': filedialog,
        'messagebox': messagebox,
        'ttk': ttk,
        'plt': plt,
        'FigureCanvasTkAgg': FigureCanvasTkAgg,
        'NavigationToolbar2Tk': NavigationToolbar2Tk,
        'find_peaks': find_peaks
    }

def show_startup_progress():
    try:
        import tkinter as tk
        from tkinter import ttk
        import numpy as np
        
        root = tk.Tk()
        root.title("PACO - Starting Up")
        root.geometry("350x100")
        root.resizable(False, False)
        
        # Add close handler for progress window
        def on_progress_close():
            print("Startup cancelled by user.")
            try:
                root.quit()
                root.destroy()
            except:
                pass
            finally:
                sys.exit(0)
        
        root.protocol("WM_DELETE_WINDOW", on_progress_close)
        
        # Center window
        root.geometry("+{}+{}".format(
            int(root.winfo_screenwidth()/2 - 175),
            int(root.winfo_screenheight()/2 - 50)
        ))
        
        tk.Label(root, text="Loading PACO Data Analyzer...", 
                font=("Arial", 11, "bold")).pack(pady=15)
        
        progress = ttk.Progressbar(root, mode='indeterminate', length=250)
        progress.pack(pady=5)
        progress.start(15)
        
        status = tk.Label(root, text="Initializing...", fg="blue")
        status.pack(pady=5)
        
        root.update()
        return root, status
        
    except Exception:
        # If GUI fails the program continues
        return None, None

def load_data_optimized(file_paths, progress_callback=None):
    """Optimized data loading with progress feedback"""
    datasets = []
    x_offsets = []
    total_points = 0
    
    for i, file_path in enumerate(file_paths):
        if progress_callback:
            progress_callback(f"Loading file {i+1}/{len(file_paths)}: {os.path.basename(file_path)}")
        
        try:
            start = time.time()
            x, y, x_offset = read_xy_file(file_path, return_offset=True)
            x = np.array(x, dtype=np.float64)
            y = np.array(y, dtype=np.float64)

            if x.size == 0 or y.size == 0:
                raise Exception("No valid XY numeric data found in file")

            datasets.append((x, y))
            x_offsets.append(x_offset)
            
            load_time = time.time() - start
            points = len(x)
            total_points += points
            
            print(f"  Loaded {os.path.basename(file_path)}: {points:,} points ({load_time:.2f}s), x_offset={x_offset:.6g}")
            
        except Exception as e:
            raise Exception(f"Failed to load {os.path.basename(file_path)}: {str(e)}")
    
    print(f"Total data points loaded: {total_points:,}")
    return datasets, x_offsets

def create_gui_with_close_handler(datasets, x_offsets):
    try:
        from plot_with_offset import plot_with_offset
        plot_with_offset(datasets, initial_offsets=x_offsets) 
        print("GUI closed.")
        
    except SystemExit:
        print("GUI window was closed - exiting program.")
        sys.exit(0)
    except KeyboardInterrupt:
        print("GUI interrupted - exiting program.")
        sys.exit(0)
    except Exception as e:
        print(f"GUI error: {e}")
        sys.exit(1)

def main():
    startup_begin = time.time()
    progress_root, status_label = show_startup_progress()
    
    def update_status(text):
        if status_label:
            status_label.config(text=text)
            progress_root.update()
        print(f"Status: {text}")
    
    try:
        update_status("Loading libraries...")
        libs = lazy_import_and_setup()
        
        import_time = time.time() - startup_begin
        print(f"All libraries loaded in {import_time:.2f} seconds")
        
        update_status("Opening file dialog...")
        if progress_root:
            progress_root.withdraw() # Hide progress window during file dialog
        
        temp_root = libs['tk'].Tk()
        temp_root.withdraw()
        
        file_paths = libs['filedialog'].askopenfilenames(
            title="Select Data Files (.txt)",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            parent=temp_root
        )
        
        temp_root.destroy()
        
        if not file_paths:
            print("No files selected. Exiting.")
            if progress_root:
                progress_root.destroy()
            return
        
        print(f"\nSelected {len(file_paths)} files:")
        for i, fp in enumerate(file_paths, 1):
            print(f"  {i}. {os.path.basename(fp)}")
        
        # Show progress window again
        if progress_root:
            progress_root.deiconify()
        
        update_status("Loading data files...")
        
        def progress_callback(msg):
            update_status(msg)
        
        load_start = time.time()
        datasets, x_offsets = load_data_optimized(file_paths, progress_callback)
        load_time = time.time() - load_start
        
        print(f"Data loading completed in {load_time:.2f} seconds")
        
        if progress_root:
            progress_root.destroy()
        
        print("Starting analysis interface...")
        gui_start = time.time()
        
        create_gui_with_close_handler(datasets, x_offsets)
        
        total_time = time.time() - startup_begin
        print(f"Total startup time: {total_time:.2f} seconds")
        print("=" * 50)
        
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
        if progress_root:
            progress_root.destroy()
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        if progress_root:
            progress_root.destroy()
        
        try:
            libs['messagebox'].showerror("Error", f"Failed to start PACO:\n{str(e)}")
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()