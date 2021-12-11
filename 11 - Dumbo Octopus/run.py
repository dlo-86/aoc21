from pathlib import Path
from typing import List
from loguru import logger

# Idea for part 1:
# - read in the map and represent it in 2D array list
# - for each step:
#   - increment all values by 1
#   - traverse all elements and look for elements greater than 10
#   - if an element is greater than 10, set it to 0, increment the flash counter and do following
#     for all adjecent neighbours
#   - increment by one if it is not 0 and look if it is greater than 10. If so, do the last step
# - after 100 steps, how many flashes did occur?
# Idea for part 2:
# - simulate as long as all octopuses have the value 0 and count the steps


class DumboOctopusSimulator:
    def __init__(self, input_lines: List[str]):
        self.octopuses: List[List[int]] = []
        for line in input_lines:
            octopus_line: List[int] = []
            for octopus in line.strip():
                octopus_line.append(int(octopus))
            self.octopuses.append(octopus_line)
        self.flashes = 0
        self.steps = 0

    def simulate(self, steps: int):
        for i in range(steps):
            self.simulate_one_step()

    def simulate_until_synchronization(self):
        while True:
            self.simulate_one_step()
            if self._check_for_synchronization():
                return

    def _check_for_synchronization(self):
        for i in range(len(self.octopuses)):
            for j in range(len(self.octopuses[i])):
                if self.octopuses[i][j] != 0:
                    return False
        return True

    def simulate_one_step(self):
        self.steps += 1
        self._do_for_all_octopuses(self._increment_by_one)
        self._do_for_all_octopuses(self._flash_octopus_if_necessary)

    def _flash_octopus_if_necessary(self, i, j):
        octopus_value = self.octopuses[i][j]
        if octopus_value == 0:
            return
        if octopus_value > 9:
            self.flashes += 1
            self.octopuses[i][j] = 0
            self._flash_adjacent_octopuses_if_necessary(i, j)

    def _flash_adjacent_octopuses_if_necessary(self, i, j):
        for new_i in range(i - 1, i + 2):
            for new_j in range(j - 1, j + 2):
                if self._i_or_j_not_range(new_i, new_j) and self._octopus_did_not_yet_flash(new_i, new_j):
                    self.octopuses[new_i][new_j] += 1
                    self._flash_octopus_if_necessary(new_i, new_j)

    def _octopus_did_not_yet_flash(self, i, j):
        return self.octopuses[i][j] != 0

    def _i_or_j_not_range(self, i, j):
        return 0 <= i < len(self.octopuses) and 0 <= j < len(self.octopuses[i])


    def _increment_by_one(self, i, j):
        self.octopuses[i][j] += 1

    def _do_for_all_octopuses(self, function):
        for i in range(len(self.octopuses)):
            for j in range(len(self.octopuses[i])):
                function(i, j)

    def print(self):
        print(self.octopuses)


def part_one(input_file: Path):
    input_lines = read_input(input_file)
    simulator = DumboOctopusSimulator(input_lines)
    simulator.simulate(100)
    print("Result 1:", simulator.flashes)


def part_two(input_file: Path):
    input_lines = read_input(input_file)
    simulator = DumboOctopusSimulator(input_lines)
    simulator.simulate_until_synchronization()
    print("Result 2:", simulator.steps)


def read_input(input_file: Path):
    with input_file.open("r") as file_handle:
        input_lines = file_handle.readlines()
        return input_lines


@logger.catch()
def main():
    part_one(Path("input.txt"))
    part_two(Path("input.txt"))


main()
