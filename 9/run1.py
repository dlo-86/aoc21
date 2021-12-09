from pathlib import Path
from loguru import logger


@logger.catch()
def main():
    file_input = Path("input.txt")
    with file_input.open("r") as file_handle:
        input_lines = file_handle.readlines()
    heatmap = []
    for line in input_lines:
        heatmap.append([int(x) for x in line.strip()])
    risk_level = 0
    line_length = len(heatmap[0])
    for i in range(0, len(heatmap)):
        for j in range(0,line_length):
            current_value = heatmap[i][j]
            if j > 0 and not heatmap[i][j - 1] > current_value:
                continue
            if j < line_length - 1 and not heatmap[i][j + 1] > current_value:
                continue
            if i > 0 and not heatmap[i - 1][j] > current_value:
                continue
            if i < len(heatmap) - 1 and not heatmap[i + 1][j] > current_value:
                continue
            risk_level += current_value + 1
    print(risk_level)


main()
