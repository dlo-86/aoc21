from pathlib import Path
from typing import List, Dict, Tuple
from loguru import logger

# Idea for part 1:
# - Use a hashmap to store all points
# - every point greater than fold line is mirrored to the other side
# Idea for part 2:
# - straight forward: just print the result after all folds

class Origami:
    def __init__(self):
        self.points: Dict[Tuple[int, int]] = {}
        self.folds: List[Tuple[str, int]] = []

    def parse_input(self, input_lines):
        for line in input_lines:
            if "," in line:
                x, y = line.strip().split(",")
                self.points[(int(x), int(y))] = "x"
            if "=" in line:
                axis, value = line.strip().split()[2].split("=")
                self.folds.append((axis, int(value)))

    def fold_first(self):
        self._fold(self.folds[0][0], self.folds[0][1])

    def fold_all(self):
        for i in range(len(self.folds)):
            self._fold(self.folds[i][0], self.folds[i][1])

    def print(self):
        max_x = max([x[0] for x in self.points.keys()])
        max_y = max([x[1] for x in self.points.keys()])
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                if (x,y) in self.points:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

    def _fold(self, axis, fold_value):
        folded_origami: Dict[Tuple[int, int]] = {}
        for point in self.points:
            x = point[0]
            y = point[1]
            if axis == "y" and y > fold_value:
                y = fold_value - (point[1] - fold_value)
            elif axis == "x" and x > fold_value:
                x = fold_value - (point[0] - fold_value)
            folded_origami[(x, y)] = "x"
        self.points = folded_origami

    def get_amount_of_points(self):
        return len(self.points)


def part_one(input_file: Path):
    input_lines = read_input(input_file)
    origami = Origami()
    origami.parse_input(input_lines)
    origami.fold_first()
    print("Result 1:", origami.get_amount_of_points())


def part_two(input_file: Path):
    input_lines = read_input(input_file)
    origami = Origami()
    origami.parse_input(input_lines)
    origami.fold_all()
    print("Result 2:")
    origami.print()


def read_input(input_file: Path):
    with input_file.open("r") as file_handle:
        input_lines = file_handle.readlines()

        return input_lines


@logger.catch()
def main():
    part_one(Path("input.txt"))
    part_two(Path("input.txt"))


main()
