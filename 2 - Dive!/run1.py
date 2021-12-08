from pathlib import Path

position = 0
depth = 0
file_input = Path("input.txt")
with file_input.open("r") as file_handle:
    for line in file_handle:
        if line.startswith("f"):
            position += int(line.split()[1])
        elif line.startswith("u"):
            depth -= int(line.split()[1])
        elif line.startswith("d"):
            depth += int(line.split()[1])
print(position * depth)