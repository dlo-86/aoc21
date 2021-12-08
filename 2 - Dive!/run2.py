from pathlib import Path

position = 0
depth = 0
aim = 0
file_input = Path("input.txt")
with file_input.open("r") as file_handle:
    for line in file_handle:
        if line.startswith("f"):
            value = int(line.split()[1])
            position += int(line.split()[1])
            depth += value * aim
        elif line.startswith("u"):
            aim -= int(line.split()[1])
        elif line.startswith("d"):
            aim += int(line.split()[1])
print(position * depth)