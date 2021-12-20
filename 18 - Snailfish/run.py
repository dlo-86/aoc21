import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Union
from loguru import logger
import copy

# Idea for part 1:
# - each pair is an object with left, right and depth
# - on addition a new pair is created with the two added pairs as left and right and the depths are increased of both
#   arguments
# - explosion: search for first element with depth > 4, replace it with 0 and add the two digits the next left and right
#   digit
# - split: create a new pair with the half and left digit rounded down and right digit rounded up
# - after addition and reduction of all numbers, return the magnitude with the given formula by recursively traversing
#   through the pairs
# Idea for part 2:
# - same as part 1 but add all numbers with each other and search for the biggest magnitude


class Pair:
    def __init__(self):
        self.left: Optional[Union[Pair, int]] = None
        self.right: Optional[Union[Pair, int]] = None
        self.depth: Optional[int] = None

    @property
    def left_is_digit(self):
        return type(self.left) == int

    @property
    def right_is_digit(self):
        return type(self.right) == int

    @property
    def is_leaf(self):
        return self.left_is_digit and self.right_is_digit

    def add_to_left(self, number: int):
        if self.left_is_digit:
            self.left += number
        else:
            self.left.add_to_left(number)

    def add_to_right(self, number: int):
        if self.right_is_digit:
            self.right += number
        else:
            self.right.add_to_right(number)

    def increase_depth(self):
        self.depth += 1
        if not self.left_is_digit:
            self.left.increase_depth()
        if not self.right_is_digit:
            self.right.increase_depth()

    def init_with_string(self, number: str, i: int, depth: int):
        self.depth = depth
        if number[i + 1] == '[':
            self.left = Pair()
            i = self.left.init_with_string(number, i + 1, depth + 1)
        else:
            m_number = re.search(r"^(\d+),.*", number[i + 1:])
            self.left = int(m_number.group(1))
            i += len(m_number.group(1)) + 1
        assert number[i] == ','
        if number[i + 1] == '[':
            self.right = Pair()
            i = self.right.init_with_string(number, i + 1, depth + 1)
        else:
            m_number = re.search(r"^(\d+)].*", number[i + 1:])
            self.right = int(m_number.group(1))
            i += len(m_number.group(1)) + 1
        assert number[i] == ']'
        return i + 1

    def init_with_pairs(self, left, right, depth=0):
        self.left = left
        self.right = right
        self.depth = depth
        self.increase_depth()

    def split(self):
        did_split = False
        if self.left_is_digit:
            if self.left > 9:
                pair = Pair()
                pair.init_with_pairs(int(self.left / 2), int(self.left / 2 + 0.5), self.depth)
                self.left = pair
                return True
        else:
            did_split |= self.left.split()
            if did_split:
                return True
        if self.right_is_digit:
            if self.right > 9:
                pair = Pair()
                pair.init_with_pairs(int(self.right / 2), int(self.right / 2 + 0.5), self.depth)
                self.right = pair
                return True
        else:
            did_split |= self.right.split()
            if did_split:
                return True
        return False

    def explode(self):
        did_reduce = False
        if self.left_is_digit and self.right_is_digit:
            if self.depth > 4:
                return True, True, self.left, self.right
        else:
            if not self.left_is_digit:
                did_reduce, reduce_necessary, left, right = self.left.explode()
                if reduce_necessary:
                    if right is not None:
                        if left is not None and right is not None:
                            self.left = 0
                        if self.right_is_digit:
                            self.right += right
                        else:
                            self.right.add_to_left(right)
                    return did_reduce, True, left, None
            if not self.right_is_digit and not did_reduce:
                did_reduce, reduce_necessary, left, right = self.right.explode()
                if reduce_necessary:
                    if left is not None:
                        if left is not None and right is not None:
                            self.right = 0
                        if self.left_is_digit:
                            self.left += left
                        else:
                            self.left.add_to_right(left)
                    return did_reduce, True, None, right
        return did_reduce, False, None, None

    def get_magnitude(self):
        magnitude = 0
        if self.left_is_digit:
            magnitude += 3 * self.left
        else:
            magnitude += 3 * self.left.get_magnitude()
        if self.right_is_digit:
            magnitude += 2 * self.right
        else:
            magnitude += 2 * self.right.get_magnitude()
        return magnitude

    def print(self, first=False):
        print("[", end="")
        if self.left_is_digit:
            print(self.left, end="")
        else:
            self.left.print()
        print(",", end="")
        if self.right_is_digit:
            print(self.right, end="")
        else:
            self.right.print()
        print("]", end="")
        if first:
            print()


def reduce_number(result):
    while True:
        while True:
            did_explode_or_split = result.explode()[0]
            if not did_explode_or_split:
                break
        did_explode_or_split |= result.split()
        if not did_explode_or_split:
            break


def get_numbers(input_lines):
    numbers = []
    for line in input_lines:
        pair = Pair()
        pair.init_with_string(line, 0, 1)
        numbers.append(pair)
    return numbers


def part_one(input_file: Path):
    input_lines = read_input(input_file)
    numbers = get_numbers(input_lines)
    result = numbers[0]
    for i in range(1, len(numbers)):
        new_pair = Pair()
        new_pair.init_with_pairs(result, numbers[i])
        result = new_pair
        reduce_number(result)
    print("Result 1:", result.get_magnitude())


def part_two(input_file: Path):
    input_lines = read_input(input_file)
    numbers = get_numbers(input_lines)
    max_magnitude = 0
    for i in range(0, len(numbers)):
        for j in range(0, len(numbers)):
            if i == j:
                continue
            working_copy = copy.deepcopy(numbers)
            pair = Pair()
            pair.init_with_pairs(working_copy[i], working_copy[j])
            reduce_number(pair)
            if max_magnitude < pair.get_magnitude():
                max_magnitude = pair.get_magnitude()
    print("Result 2:", max_magnitude)


def read_input(input_file: Path):
    with input_file.open("r") as file_handle:
        input_lines = file_handle.readlines()
        return input_lines


@logger.catch()
def main():
    part_one(Path("input.txt"))
    part_two(Path("input.txt"))


main()
