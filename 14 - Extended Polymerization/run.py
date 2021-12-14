from pathlib import Path
from typing import Dict
from loguru import logger
import copy

# Idea for part 1 and 2:
# - use a dict for all pairs and remember the amount of this pair as value and the last element
# - in every step create a copy and for each pair create the new pairs and increase the corresponding dict values by
#   the initial value and decrease the initial value correspondingly
# - the amount of elements can be counted by add up the values of each pair beginning with the value and add 1 if the
#   last value is the same


class Polymer:
    def __init__(self):
        self.pair_insertion: Dict[str, str] = {}
        self.polymer: Dict[str, int] = {}
        self.end_element = ""

    def get_elements(self):
        return set("".join(self.polymer.keys()))

    def add_polymer(self, polymer):
        chunks = list(polymer.strip())
        self.end_element = chunks[-1]
        for i in range(len(chunks) - 1):
            key = chunks[i] + chunks[i + 1]
            if key in self.polymer:
                self.polymer[key] += 1
            else:
                self.polymer[key] = 1

    def add_pair_insertion(self, line: str):
        elements = line.strip().split()
        pair = elements[0]
        insert = elements[2]
        self.pair_insertion[pair] = insert
        if pair not in self.polymer:
            self.polymer[pair] = 0

    def do_step(self, amount: int):
        for i in range(amount):
            self._step()

    def _step(self):
        new_polymer = copy.copy(self.polymer)
        for key, value in self.polymer.items():
            if value == 0:
                continue
            insert = self.pair_insertion[key]
            begin = key[0]
            end = key[1]
            new_polymer[key] -= value
            new_polymer[begin + insert] += value
            new_polymer[insert + end] += value
        self.polymer = new_polymer

    def count(self, element):
        element_sum = 0
        for key, value in self.polymer.items():
            if element == key[0]:
                element_sum += value
        if element == self.end_element:
            element_sum += 1
        return element_sum


def parse_input(input_lines, polymer):
    for line in input_lines:
        if line.strip() == "":
            continue
        elif "->" in line:
            polymer.add_pair_insertion(line)
        else:
            polymer.add_polymer(line)


def get_min_max(polymer):
    min_value = polymer.count(next(iter(polymer.get_elements())))
    max_value = 0
    for element in set("".join(polymer.polymer.keys())):
        if polymer.count(element) < min_value:
            min_value = polymer.count(element)
        if polymer.count(element) > max_value:
            max_value = polymer.count(element)
    return max_value, min_value


def part_one(input_file: Path):
    input_lines = read_input(input_file)
    polymer = Polymer()
    parse_input(input_lines, polymer)
    polymer.do_step(10)
    max_value, min_value = get_min_max(polymer)
    print("Result 1:", max_value - min_value)


def part_two(input_file: Path):
    input_lines = read_input(input_file)
    polymer = Polymer()
    parse_input(input_lines, polymer)
    polymer.do_step(40)
    max_value, min_value = get_min_max(polymer)
    print("Result 2:",  max_value - min_value)


def read_input(input_file: Path):
    with input_file.open("r") as file_handle:
        input_lines = file_handle.readlines()

        return input_lines


@logger.catch()
def main():
    part_one(Path("input.txt"))
    part_two(Path("input.txt"))


main()
