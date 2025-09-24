#!/usr/bin/env python3
"""
Test script to verify window closing behavior
"""
import tkinter as tk
import sys

def test_window_closing():
    """Test if window closing works properly"""
    print("Testing window closing behavior...")
    
    root = tk.Tk()
    root.title("PACO - Window Close Test")
    root.geometry("400x200")
    
    # Add proper window closing handler
    def on_closing():
        """Handle window closing properly"""
        print("Window close button clicked - cleaning up...")
        try:
            root.quit()  # Stop the mainloop
            root.destroy()  # Destroy the window
        except:
            pass
        finally:
            print("Exiting program...")
            sys.exit(0)  # Ensure the program exits
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    # Add some content
    tk.Label(root, text="PACO Window Close Test", 
             font=("Arial", 16, "bold")).pack(pady=20)
    
    tk.Label(root, text="Try closing this window using the X button", 
             font=("Arial", 10)).pack(pady=10)
    
    tk.Label(root, text="The program should exit completely", 
             font=("Arial", 10)).pack(pady=5)
    
    # Add manual close button for testing
    def manual_close():
        print("Manual close button clicked")
        on_closing()
    
    tk.Button(root, text="Close Manually", command=manual_close,
             font=("Arial", 12)).pack(pady=20)
    
    print("Window created. Try closing it with X button or manual button.")
    print("The program should exit completely when closed.")
    
    # Start the main loop
    root.mainloop()
    
    # This should not be reached if closing works properly
    print("WARNING: mainloop ended but program didn't exit!")

if __name__ == "__main__":
    test_window_closing()