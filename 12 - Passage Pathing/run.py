from pathlib import Path
from typing import List, Dict
from loguru import logger

# Idea for part 1:
# - Parse all caves, store if they are small, big, start, or end.
# - store all connected caves
# - Start at cave start and iterate through all connected caves. Remember the small caves in a list to not select them
#   again.
# - If one path comes to the end cave, stop and increment counter

# Idea for part 2:
# - skip caves as soon as the set of small caves gets bigger as the unique set of small caves + 1 because now we count
#   two small cave two times


class Cave:
    def __init__(self, name: str):
        self.name = name
        self.connected_caves: Dict[str, Cave] = {}
        self.start = False
        self.end = False
        if name == "start":
            self.start = True
            self.end = False
        if name == "end":
            self.start = False
            self.end = True
        if name.isupper():
            self.big_cave = True
        else:
            self.big_cave = False

    def add_connected_cave(self, cave):
        self.connected_caves[cave.name] = cave


class CaveSystem:
    def __init__(self):
        self.cave_list: Dict[str, Cave] = {}
        self.paths = 0

    def find_paths_from_start_part_one(self):
        self._find_paths(self.cave_list["start"], [], True)

    def find_paths_from_start_part_two(self):
        self._find_paths(self.cave_list["start"], [], False)

    def _find_paths(self, cave: Cave, small_caves: List[Cave], first_part):
        for connected_cave in cave.connected_caves.values():
            if connected_cave.start or \
                    connected_cave in small_caves and first_part or \
                    self._has_visited_a_small_cave_more_than_once(small_caves) and not first_part:
                continue
            if connected_cave.end:
                self.paths += 1
                continue
            if connected_cave.big_cave:
                self._find_paths(connected_cave, small_caves, first_part)
            else:
                self._find_paths(connected_cave, small_caves + [connected_cave], first_part)

    @staticmethod
    def _has_visited_a_small_cave_more_than_once(small_caves: List[Cave]):
        return len(small_caves) > len(set(small_caves)) + 1

    def add_path(self, cave1: str, cave2: str):
        if cave1 not in self.cave_list:
            self.cave_list[cave1] = Cave(cave1)
        if cave2 not in self.cave_list:
            self.cave_list[cave2] = Cave(cave2)
        self.cave_list[cave1].add_connected_cave(self.cave_list[cave2])
        self.cave_list[cave2].add_connected_cave(self.cave_list[cave1])


def part_one(input_file: Path):
    input_lines = read_input(input_file)
    cave_system = CaveSystem()
    for line in input_lines:
        cave1, cave2 = line.strip().split("-")
        cave_system.add_path(cave1, cave2)
    cave_system.find_paths_from_start_part_one()
    print("Result 1:", cave_system.paths)


def part_two(input_file: Path):
    input_lines = read_input(input_file)
    cave_system = CaveSystem()
    for line in input_lines:
        cave1, cave2 = line.strip().split("-")
        cave_system.add_path(cave1, cave2)
    cave_system.find_paths_from_start_part_two()
    print("Result 2:", cave_system.paths)


def read_input(input_file: Path):
    with input_file.open("r") as file_handle:
        input_lines = file_handle.readlines()
        return input_lines


@logger.catch()
def main():
    part_one(Path("input.txt"))
    part_two(Path("input.txt"))


main()
