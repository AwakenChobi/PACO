import numpy as np

def normalize_spectra(datasets, offsets):

    # Adjust x values with offsets
    adjusted_data = [
        ([xi + offsets[i] for xi in x], y)
        for i, (x, y) in enumerate(datasets)]

    # Calculate the overlapping range
    start = max(min(x) for x, _ in adjusted_data)
    end = min(max(x) for x, _ in adjusted_data)

    print("Start of overlapping range:", start)
    print("End of overlapping range:", end)
    # Find the number of points in each dataset within the range, then take the minimum
    # It should be the same for all datasets though
    points_in_range = [
        np.sum((np.array(x) >= start) & (np.array(x) <= end))
        for x, _ in adjusted_data
    ]
    num_points = min(points_in_range)

    common_x = np.linspace(
        start,  # highest minimum
        end,    # lowest maximum
        num_points
    )
    # Interpolate y values for each dataset to the common x values
    # np.interp(x, xp, fp):
    # x: The x-coordinates at which to evaluate the interpolated values.
    # xp: The x-coordinates of the data points. These are the x values of the datasets.
    # fp: The y-coordinates of the data points. These are the y values of the datasets.
    interpolated_y = [
        np.interp(common_x, x, y)
        for x, y in adjusted_data
    ]

    avg_y = np.mean(interpolated_y, axis=0)

    # Compute the standard deviation for each x value
    # np.std(a, axis=None, dtype=None, out=None, ddof=0, keepdims=False):
    # a: The input array or object that contains the data.
    # axis: The axis or axes along which to compute the standard deviation. If None, the standard deviation is computed over the entire array.
    # dtype: The data type to use for the computation. If None, the data type of the input array is used.
    # out: An alternative output array in which to place the result. It must have the same shape as the expected output.
    # ddof: (0 by default) Delta degrees of freedom. The divisor used in the calculation is N - ddof, where N is the number of elements.
    # keepdims: If True, the reduced axes are left in the result as dimensions with size one. This can be useful for broadcasting.
    #If you divide all the data points in the dataset by the same factor k (like the maximum value), the standard deviation (σ) will also be divided by k.
    # This is because the standard deviation is a measure of spread that scales linearly with linear transformations of the data.
    
    std_dev_y = np.std(interpolated_y, axis=0) /np.max(avg_y)

    # Normalize the averaged spectra
    normalized_avg_y = avg_y / np.max(avg_y)

    print("Maximum value of avg_y before normalization:", np.max(avg_y))
    print("Maximum value of avg_y after normalization (should be 1):", np.max(normalized_avg_y))
    return common_x, normalized_avg_y, std_dev_y