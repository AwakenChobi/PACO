# This script reads a file containing two columns of numeric data (x and y values)
# Function to read the file and extract x and y data

def read_xy_file(file_path):
    x_data = []
    y_data = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                x, y = map(float, line.split())
                x_data.append(x)
                y_data.append(y)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except ValueError:
        print("Error: Ensure the file contains two numeric columns separated by spaces.")
    
    print("Data read successfully from the file.")
    return x_data, y_data
