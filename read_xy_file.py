# This script reads a file containing two columns of numeric data (x and y values)
# Function to read the file and extract x and y data
def read_xy_file(file_path):
    x_data = []
    y_data = []
    # Attempt to open the file and read its contents
    # Handle potential errors with file reading
    # and data conversion
    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Split the line into x and y values
                x, y = map(float, line.split())
                x_data.append(x)
                y_data.append(y)
    #If the file is not found, print an error message
    # If the data cannot be converted to float, print an error message
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except ValueError:
        print("Error: Ensure the file contains two numeric columns separated by spaces.")
    return x_data, y_data
