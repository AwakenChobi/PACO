import numpy as np

# Function to compute the average and standard deviation of three datasets with offsets
def compute_stats(datasets, offsets, ax, canvas):

    # Adjust x values with offsets
    adjusted_data = [
        ([xi + offsets[i] for xi in x], y) for i, (x, y) in enumerate(datasets)
    ]

    # Interpolate to align x values
    num_points = len(adjusted_data[0][0])  # Use the number of points in the first dataset
    common_x = np.linspace(
        min(min(x for x, _ in adjusted_data)), max(max(x for x, _ in adjusted_data)), num_points
    )
    interpolated_y = [
        np.interp(common_x, [xi + offsets[i] for xi in x], y)
        for i, (x, y) in enumerate(adjusted_data)
    ]
    avg_y = np.mean(interpolated_y, axis=0)
    std_y = np.std(interpolated_y, axis=0)

    # Plot the average and standard deviation
    ax.clear()
    for i, (x, y) in enumerate(adjusted_data):
        ax.scatter(x, y, label=f"Dataset {i+1}")
    ax.plot(common_x, avg_y, color="black", label="Average")
    ax.fill_between(
        common_x, avg_y - std_y, avg_y + std_y, color="gray", alpha=0.3, label="Std Dev"
    )
    ax.set_xlabel("X Axis")
    ax.set_ylabel("Y Axis")
    ax.set_title("Average and Standard Deviation")
    ax.legend()
    ax.grid(True)
    canvas.draw()

#Hay que aumentar el número de inputs jeje