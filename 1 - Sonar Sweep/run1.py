from pathlib import Path

increases = 0
decreases = 0
last_number = None
file_input = Path("input.txt")

with file_input.open("r") as file_handle:
    for line in file_handle:
        number = int(line)
        if not last_number:
            last_number = number
        if number > last_number:
            increases += 1
        if number < last_number:
            decreases += 1
        last_number = number
print(increases)
