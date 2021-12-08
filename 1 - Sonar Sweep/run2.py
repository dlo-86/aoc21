from pathlib import Path

increases = 0
decreases = 0
last_number = None
file_input = Path("input.txt")
sliding_window = {}
pos = 1

with file_input.open("r") as file_handle:
    for line in file_handle:
        number = int(line)
        sliding_window[pos] = number
        if len(sliding_window) == 3:
            summed_values = sum(sliding_window.values())
            if not last_number:
                last_number = summed_values
            if summed_values > last_number:
                increases += 1
            if summed_values < last_number:
                decreases -= 1
            last_number = summed_values
        pos += 1
        if pos > 3:
            pos = 1
print(increases)
