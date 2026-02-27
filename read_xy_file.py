# This script reads a file containing two columns of numeric data (x and y values)
# and optionally an offset metadata line.

import re


OFFSET_PATTERN = re.compile(
    r"^(?:paco_)?x_offset\s*[:=]\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)$",
    re.IGNORECASE,
)


def _parse_offset_line(line):
    stripped = line.strip()
    if not stripped.startswith("#"):
        return None

    content = stripped[1:].strip()
    match = OFFSET_PATTERN.match(content)
    if not match:
        return None

    return float(match.group(1))


def read_xy_file(file_path, return_offset=False):
    x_data = []
    y_data = []
    x_offset = 0.0

    try:
        with open(file_path, 'r') as file:
            for line in file:
                stripped = line.strip()
                if not stripped:
                    continue

                parsed_offset = _parse_offset_line(stripped)
                if parsed_offset is not None:
                    x_offset = parsed_offset
                    continue

                parts = stripped.split()
                if len(parts) < 2:
                    continue

                try:
                    x = float(parts[0])
                    y = float(parts[1])
                except ValueError:
                    continue

                x_data.append(x)
                y_data.append(y)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")

    print("Data read successfully from the file.")
    if return_offset:
        return x_data, y_data, x_offset
    return x_data, y_data
