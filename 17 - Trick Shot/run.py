import re
from pathlib import Path
from typing import Dict, List
from loguru import logger
import copy

# Idea for part 1:
# - start with y = min_y and increase it till 100 (gut feeling)
# - we increase x until the line ends behind the target area without coming under the target and then store the
#   highest y
# Idea for part 2:
# - we don't stop on the first hit, but when we overshoot
# - we add some misses (x_max - x_min) because ending behind the target area does not mean we did miss the target line,
#   only no step did hit the target area


def simulate(x_min, x_max, y_min, y_max, x_velocity, y_velocity):
    x_point = 0
    y_point = 0
    y_highest = 0
    while True:
        x_point += x_velocity
        y_point += y_velocity
        if y_highest < y_point:
            y_highest = y_point
        if x_velocity > 0:
            x_velocity -= 1
        y_velocity -= 1
        if x_min <= x_point <= x_max and y_min <= y_point <= y_max:
            return y_highest, False
        if y_point < y_min:
            return None, False
        if x_point > x_max:
            return None, True


def part_one(input_file: Path):
    input_lines = read_input(input_file)
    x_max, x_min, y_max, y_min = extract_target_area(input_lines)
    y_highest = calculate_highest_y(x_max, x_min, y_max, y_min)
    print("Result 1:", y_highest)


def calculate_highest_y(x_max, x_min, y_max, y_min):
    y_highest = 0
    for y in range(y_min, 100):
        x = 1
        while True:
            y_highest_new, overshoot = simulate(x_min, x_max, y_min, y_max, x, y)
            if y_highest_new:
                if y_highest_new > y_highest:
                    y_highest = y_highest_new
                    break
            if overshoot:
                break
            x += 1
    return y_highest


def calculate_all_velocities(x_max, x_min, y_max, y_min):
    count = 0

    for y in range(y_min, 100):
        miss_counter = (x_max - x_min) * 2
        x = 1
        while True:
            hit, overshoot = simulate(x_min, x_max, y_min, y_max, x, y)
            if hit is not None:
                count += 1
            if overshoot:
                if miss_counter == 0:
                    break
                else:
                    miss_counter -= 1
            x += 1
    return count


def extract_target_area(input_lines):
    m_target_area = re.search(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)", input_lines[0])
    x_min = int(m_target_area.group(1))
    x_max = int(m_target_area.group(2))
    y_min = int(m_target_area.group(3))
    y_max = int(m_target_area.group(4))
    return x_max, x_min, y_max, y_min


def part_two(input_file: Path):
    input_lines = read_input(input_file)
    x_max, x_min, y_max, y_min = extract_target_area(input_lines)
    count = calculate_all_velocities(x_max, x_min, y_max, y_min)
    print("Result 2:", count)


def read_input(input_file: Path):
    with input_file.open("r") as file_handle:
        input_lines = file_handle.readlines()

        return input_lines


@logger.catch()
def main():
    part_one(Path("input.txt"))
    part_two(Path("input.txt"))


main()
