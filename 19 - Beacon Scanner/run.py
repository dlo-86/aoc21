import itertools
from pathlib import Path
from typing import Dict, List
from loguru import logger


def part_one(input_file: Path):
    with input_file.open("r") as file_handle:
        scanner_inputs = file_handle.read().split("\n\n")
        scanner_list = []
        for scanner_input in scanner_inputs:
            scanner_list.append([[int(y) for y in x.split(",")] for x in scanner_input.split("\n")[1:]])
            print(scanner_list[-1])
        relative_absolute_distances1 = []
        for point1 in scanner_list[0]:
            for point2 in scanner_list[0]:
                if point1 == point2:
                    continue
                x_abs = abs(point1[0] - point2[0])
                y_abs = abs(point1[1] - point2[1])
                z_abs = abs(point1[2] - point2[2])
                relative_absolute_distances1.append([x_abs, y_abs, z_abs])
        relative_absolute_distances2 = []
        for point1 in scanner_list[1]:
            for point2 in scanner_list[1]:
                if point1 == point2:
                    continue
                x_abs = abs(point1[0] - point2[0])
                y_abs = abs(point1[1] - point2[1])
                z_abs = abs(point1[2] - point2[2])
                relative_absolute_distances2.append([x_abs, y_abs, z_abs])
        for distance1 in relative_absolute_distances1:
            for distance2 in relative_absolute_distances2:
                if distance1[0] in distance2 and distance1[1] in distance2 and distance1[2] in distance2:
                    print(distance1)
                    print(distance2)


    print("Result 1:")


def part_two(input_file: Path):
    input_lines = read_input(input_file)
    print("Result 2:")


def read_input(input_file: Path):
    with input_file.open("r") as file_handle:
        input_lines = file_handle.readlines()

        return input_lines


@logger.catch()
def main():
    part_one(Path("test_input.txt"))
    part_two(Path("input.txt"))


main()
