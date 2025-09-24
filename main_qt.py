# Super-optimized main.py with lazy imports and better performance
import time
import sys
import os
import numpy as np

# Only import the absolute essentials at startup
print("PACO Data Analyzer v2.0 - Fast Loading")
print("=" * 50)
startup_time = time.time()

def lazy_import_and_setup():
    """Lazy import of heavy libraries with progress feedback"""
    print("Loading libraries...")
    
    import numpy as np
    print("  ✓ NumPy loaded")
    
    import tkinter as tk
    from tkinter import filedialog, messagebox, ttk
    print("  ✓ Tkinter loaded")
    
    print("  ⏳ Loading matplotlib (this may take a moment)...")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
    print("  ✓ Matplotlib loaded")
    
    print("  ⏳ Loading scipy...")
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
    """Show a lightweight startup progress window"""
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
            """Handle progress window close"""
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
        # If GUI fails, continue without progress window
        return None, None

def load_data_optimized(file_paths, progress_callback=None):
    """Optimized data loading with progress feedback"""
    datasets = []
    total_points = 0
    
    for i, file_path in enumerate(file_paths):
        if progress_callback:
            progress_callback(f"Loading file {i+1}/{len(file_paths)}: {os.path.basename(file_path)}")
        
        try:
            # Use optimized loading
            start = time.time()
            data = np.loadtxt(file_path, dtype=np.float32)  # float32 for speed and memory
            x, y = data[:, 0], data[:, 1]
            datasets.append((x, y))
            
            load_time = time.time() - start
            points = len(x)
            total_points += points
            
            print(f"  Loaded {os.path.basename(file_path)}: {points:,} points ({load_time:.2f}s)")
            
        except Exception as e:
            raise Exception(f"Failed to load {os.path.basename(file_path)}: {str(e)}")
    
    print(f"Total data points loaded: {total_points:,}")
    return datasets

def create_gui_with_close_handler(datasets):
    """Create GUI with proper window closing integrated"""
    try:
        # Import the plot function
        from plot_with_offset import plot_with_offset
        
        print("Creating GUI with integrated close handler...")
        
        # This will use the modified plot_with_offset that already has proper closing
        plot_with_offset(datasets)
        
        # If we reach here, the GUI was closed normally
        print("GUI closed normally.")
        
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
    
    # Show progress window early
    progress_root, status_label = show_startup_progress()
    
    # Update status
    def update_status(text):
        if status_label:
            status_label.config(text=text)
            progress_root.update()
        print(f"Status: {text}")
    
    try:
        # Lazy import all the heavy libraries
        update_status("Loading libraries...")
        libs = lazy_import_and_setup()
        
        import_time = time.time() - startup_begin
        print(f"All libraries loaded in {import_time:.2f} seconds")
        
        # File selection
        update_status("Opening file dialog...")
        if progress_root:
            progress_root.withdraw()  # Hide progress window during file dialog
        
        # Create a temporary root for file dialog
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
        
        # Load data files
        update_status("Loading data files...")
        
        def progress_callback(msg):
            update_status(msg)
        
        load_start = time.time()
        datasets = load_data_optimized(file_paths, progress_callback)
        load_time = time.time() - load_start
        
        print(f"Data loading completed in {load_time:.2f} seconds")
        
        # Close progress window
        if progress_root:
            progress_root.destroy()
        
        # Import and call the main plot function
        print("Starting analysis interface...")
        gui_start = time.time()
        
        # Use the integrated GUI with proper close handler
        create_gui_with_close_handler(datasets)
        
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
        
        # Show error dialog if possible
        try:
            libs['messagebox'].showerror("Error", f"Failed to start PACO:\n{str(e)}")
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()