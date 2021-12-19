from pathlib import Path
from typing import Dict, List
from loguru import logger

# Idea for part 1:
# - search for evey point the shortest path from top left
# - create a map where every point has a very high value (risk value from top left)
# - we let particles start from top left and go in all directions, if their risk value is lower
# - if a particle does not find any lower point, it dies
# - we simulate as long as particles live
# - after all particles died, we take the value from bottom right
# Idea for part 2:
# - create extended map and use algorithm from part 1


def calc_shortest_path(risk_map: List[List[int]]):
    positions = {(0, 0): 0}
    lowest_risk_values = {}
    for i in range(len(risk_map)):
        for j in range(len(next(iter(risk_map)))):
            lowest_risk_values[(i, j)] = 1e100
    while True:
        new_positions = {}
        for key, value in positions.items():
            i = key[0]
            j = key[1]
            calc_new_position(i + 1, j, lowest_risk_values, new_positions, risk_map, value)
            calc_new_position(i - 1, j, lowest_risk_values, new_positions, risk_map, value)
            calc_new_position(i, j + 1, lowest_risk_values, new_positions, risk_map, value)
            calc_new_position(i, j - 1, lowest_risk_values, new_positions, risk_map, value)
        positions = new_positions
        if len(positions) == 0:
            break
    return lowest_risk_values[(len(risk_map) - 1, len(risk_map[0]) - 1)]


def calc_new_position(i, j, lowest_risk_values, new_positions, risk_map, value):
    if 0 <= i < len(risk_map) and 0 <= j < len(risk_map[0]):
        if risk_map[i][j] + value < lowest_risk_values[(i, j)]:
            new_positions[(i, j)] = risk_map[i][j] + value
            lowest_risk_values[(i, j)] = risk_map[i][j] + value


def get_map(input_lines: List[str]):
    risk_map: List[List[int]] = []
    for line in input_lines:
        risk_line = []
        for field in line.strip():
            risk_line.append(int(field))
        risk_map.append(risk_line)
    return risk_map


def get_extended_risk_map(risk_map):
    extended_map: List[List[int]] = []
    for i in range(5):
        for i_map in range(len(risk_map)):
            risk_line = []
            for j in range(5):
                for j_map in range(len(next(iter(risk_map)))):
                    value = risk_map[i_map][j_map]
                    value += i + j
                    if value > 9:
                        value -= 9
                    risk_line.append(value)
            extended_map.append(risk_line)
    return extended_map


def part_one(input_file: Path):
    input_lines = read_input(input_file)
    risk_map = get_map(input_lines)
    shortest_path = calc_shortest_path(risk_map)
    print("Result 1:", shortest_path)


def part_two(input_file: Path):
    input_lines = read_input(input_file)
    risk_map = get_map(input_lines)
    extended_risk_map = get_extended_risk_map(risk_map)
    shortest_path = calc_shortest_path(extended_risk_map)
    print("Result 2:", shortest_path)


def read_input(input_file: Path):
    with input_file.open("r") as file_handle:
        input_lines = file_handle.readlines()

        return input_lines


@logger.catch()
def main():
    part_one(Path("input.txt"))
    part_two(Path("input.txt"))


main()
