from pathlib import Path
from typing import Dict, List, Optional, Union
from loguru import logger

# Idea for part 1:
# - set up a 2-dimensional array which is always extended with the infinite value
# - the infinite value is defined by the algorithm values 0 and 511 (all darg or all light)
# - then the enhancement algorithm is applied as described, take dark and light pixel in 3x3 grid, transform it into
#   binary and take the value from the algorithm
# Idea for part 2:
# - same as part 1, but with 50 steps


class Image:
    def __init__(self):
        self.map: List[List[str]] = []
        self.algorithm: List[str] = []
        self.infinite_value = "."

    def set_algorithm(self, algorithm: str):
        self.algorithm = list(algorithm)

    def init_with_string(self, string_image: List[str]):
        for line in string_image:
            line = line.strip()
            image_line = []
            for pixel in line:
                image_line.append(pixel)
            self.map.append(image_line)
        self._extend_map()

    def enhance_steps(self, steps: int):
        for i in range(steps):
            self.enhance()

    def enhance(self):
        new_map = []
        self._extend_map()
        for i in range(len(self.map)):
            new_line = []
            for j in range(len(self.map[i])):
                if self._is_infinite_value(i, j):
                    self._append_infinite_value(new_line)
                else:
                    self._append_enhanced_value(i, j, new_line)
            new_map.append(new_line)
        self._set_infinite_value_and_map(new_map)

    def _is_infinite_value(self, i, j):
        return i == 0 or j == 0 or i == len(self.map) - 1 or j == len(self.map[0]) - 1

    def _set_infinite_value_and_map(self, new_map):
        if self.infinite_value == ".":
            self.infinite_value = self.algorithm[0]
        elif self.infinite_value == "#":
            self.infinite_value = self.algorithm[511]
        self.map = new_map

    def _append_enhanced_value(self, i, j, new_line):
        pixel_string = "".join(
            self.map[i - 1][j - 1:j + 2] + self.map[i][j - 1:j + 2] + self.map[i + 1][j - 1:j + 2])
        selector = int(pixel_string.replace(".", "0").replace("#", "1"), 2)
        new_line.append(self.algorithm[selector])

    def _append_infinite_value(self, new_line):
        if self.infinite_value == ".":
            new_line.append(self.algorithm[0])
        elif self.infinite_value == "#":
            new_line.append(self.algorithm[511])

    def _extend_map(self):
        for line in self.map:
            line.insert(0, self.infinite_value)
            line.append(self.infinite_value)
        self.map.insert(0, [self.infinite_value] * (len(self.map[0])))
        self.map.append([self.infinite_value] * (len(self.map[0])))

    def print(self):
        for line in self.map:
            for pixel in line:
                print(pixel, end="")
            print()
        print()

    def get_light_pixels(self):
        light_pixel_sum = 0
        for line in self.map:
            light_pixel_sum += len([x for x in line if x == '#'])
        return light_pixel_sum


def setup_image(input_lines):
    image = Image()
    algorithm = ""
    i = 0
    while True:
        if input_lines[i].strip() == "":
            i += 1
            break
        else:
            algorithm += input_lines[i].strip()
            i += 1
        image.set_algorithm(algorithm)
    image.init_with_string(input_lines[i:])
    return image


def part_one(input_file: Path):
    input_lines = read_input(input_file)
    image = setup_image(input_lines)
    image.enhance_steps(2)
    light_pixel_sum = image.get_light_pixels()
    print("Result 1:", light_pixel_sum)


def part_two(input_file: Path):
    input_lines = read_input(input_file)
    image = setup_image(input_lines)
    image.enhance_steps(50)
    light_pixel_sum = image.get_light_pixels()
    print("Result 2:", light_pixel_sum)


def read_input(input_file: Path):
    with input_file.open("r") as file_handle:
        input_lines = file_handle.readlines()
        return input_lines


@logger.catch()
def main():
    part_one(Path("input.txt"))
    part_two(Path("input.txt"))


main()
