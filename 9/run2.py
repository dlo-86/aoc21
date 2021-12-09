from pathlib import Path
from typing import List

from loguru import logger


class BasinFinder:
    def __init__(self, height_map: List[List[int]]):
        self.height_map = height_map
        self.line_length = len(height_map[0])

    def find_basin(self, i, j):
        found_points = []
        self._find_next_points(i,j, found_points)
        return len(found_points)

    def _find_next_points(self,i, j, found_points):
        if (i, j) in found_points:
            return
        found_points.append((i, j))
        current_value = self.height_map[i][j]
        if j > 0 and self.height_map[i][j - 1] > current_value and self.height_map[i][j - 1] != 9:
            self._find_next_points(i, j - 1, found_points)
        if j < self.line_length - 1 and self.height_map[i][j + 1] > current_value and self.height_map[i][j + 1] != 9:
            self._find_next_points(i, j + 1, found_points)
        if i > 0 and self.height_map[i - 1][j] > current_value and self.height_map[i - 1][j] != 9:
            self._find_next_points(i - 1, j, found_points)
        if i < len(self.height_map) - 1 and self.height_map[i + 1][j] > current_value and self.height_map[i + 1][j] != 9:
            self._find_next_points(i + 1, j, found_points)


@logger.catch()
def main():
    file_input = Path("input.txt")
    with file_input.open("r") as file_handle:
        input_lines = file_handle.readlines()
    height_map = []
    for line in input_lines:
        height_map.append([int(x) for x in line.strip()])
    risk_level = 0
    line_length = len(height_map[0])
    basins = []
    for i in range(0, len(height_map)):
        for j in range(0,line_length):
            current_value = height_map[i][j]
            if j > 0 and not height_map[i][j - 1] > current_value:
                continue
            if j < line_length - 1 and not height_map[i][j + 1] > current_value:
                continue
            if i > 0 and not height_map[i - 1][j] > current_value:
                continue
            if i < len(height_map) - 1 and not height_map[i + 1][j] > current_value:
                continue
            basin_finder = BasinFinder(height_map)
            basins.append(basin_finder.find_basin(i, j))
    basins.sort(reverse=True)
    result = 1
    for i in range(3):
        result *= basins[i]
    print(result)



main()
