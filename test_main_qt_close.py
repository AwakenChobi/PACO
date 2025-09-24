#!/usr/bin/env python3
"""
Test script for main_qt.py window closing functionality
"""
import subprocess
import sys
import time

def test_main_qt_closing():
    """Test if main_qt.py properly handles window closing"""
    print("=" * 60)
    print("TESTING main_qt.py WINDOW CLOSING FUNCTIONALITY")
    print("=" * 60)
    
    print("\nThis test will:")
    print("1. Start main_qt.py")
    print("2. You should see the startup progress window")
    print("3. You can close the progress window to test early exit")
    print("4. Or continue to file selection and main GUI")
    print("5. Try closing the main analysis window")
    print("6. Verify the program exits completely")
    
    print("\nInstructions:")
    print("- If you close the progress window, the program should exit immediately")
    print("- If you select files and open the main GUI, closing it should exit the program")
    print("- Watch the console for exit messages")
    
    input("\nPress Enter to start the test...")
    
    try:
        # Run main_qt.py
        print("\nStarting main_qt.py...")
        process = subprocess.Popen([sys.executable, "main_qt.py"], 
                                 cwd="d:\\Documentos\\Codes\\PACO")
        
        # Wait for the process to complete
        return_code = process.wait()
        
        print(f"\nmain_qt.py exited with code: {return_code}")
        
        if return_code == 0:
            print("✓ Program exited normally")
        else:
            print(f"⚠ Program exited with error code {return_code}")
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        try:
            process.terminate()
        except:
            pass
    except Exception as e:
        print(f"Error running test: {e}")

def show_manual_test_instructions():
    """Show manual testing instructions"""
    print("\n" + "=" * 60)
    print("MANUAL TESTING INSTRUCTIONS")
    print("=" * 60)
    
    print("\n1. Run: python main_qt.py")
    print("\n2. Test Progress Window Closing:")
    print("   - When the progress window appears, try clicking the X button")
    print("   - The program should exit immediately with 'Startup cancelled by user' message")
    
    print("\n3. Test Main GUI Closing:")
    print("   - Let the progress complete and select some data files")
    print("   - When the main analysis window opens, try clicking the X button")
    print("   - The program should exit completely with cleanup messages")
    
    print("\n4. Expected Console Messages:")
    print("   - 'Window close button clicked - cleaning up...'")
    print("   - 'Exiting program...'")
    print("   - 'GUI window was closed - exiting program.'")
    
    print("\n5. Verification:")
    print("   - Check Task Manager to ensure no Python processes are left running")
    print("   - The console should return to the command prompt")
    
if __name__ == "__main__":
    print("PACO main_qt.py Window Closing Test")
    
    choice = input("\nChoose test method:\n1. Automated test\n2. Manual test instructions\nChoice (1 or 2): ")
    
    if choice == "1":
        test_main_qt_closing()
    else:
        show_manual_test_instructions()
    
    print("\nTest completed.")