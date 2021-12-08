import re
from pathlib import Path
from typing import List
from loguru import logger


class Line:
    def __init__(self, input_string: str):
        m_line = re.search(r"^(\d+),(\d+) -> (\d+),(\d+)$", input_string)
        x1 = int(m_line.group(1))
        y2 = int(m_line.group(4))
        y1 = int(m_line.group(2))
        x2 = int(m_line.group(3))
        if x1 < x2:
            self._same_order(x1, y1, x2, y2)
        elif x2 < x1:
            self._changed_order(x1, y1, x2, y2)
        elif y1 <= y2:
            self._same_order(x1, y1, x2, y2)
        else:
            self._changed_order(x1, y1, x2, y2)
        if self.x1 == self.x2:
            self.direction = "vertical"
        elif self.y1 == self.y2:
            self.direction = "horizontal"
        elif self.y1 < self.y2:
            self.direction = "down"
        else:
            self.direction = "up"
        self.points = self.get_points()

    def _same_order(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def _changed_order(self, x1, y1, x2, y2):
        self.x1 = x2
        self.y1 = y2
        self.x2 = x1
        self.y2 = y1

    def get_points(self):
        if self.direction == "vertical":
            y_points = list(range(self.y1, self.y2 + 1))
            x_points = [self.x1] * len(y_points)
        elif self.direction == "horizontal":
            x_points = list(range(self.x1, self.x2 + 1))
            y_points = [self.y1] * len(x_points)
        else:
            x_points = []
            y_points = []
        return list(zip(x_points, y_points))


@logger.catch()
def main():
    file_input = Path("input.txt")
    with file_input.open("r") as file_handle:
        input_lines = file_handle.readlines()
    lines: List[Line] = []
    for line in input_lines:
        lines.append(Line(line))
    point_list = dict()
    for line in lines:
        for point in line.points:
            if point not in point_list:
                point_list[point] = 1
            else:
                point_list[point] += 1

    print(len([x for x in point_list.values() if x > 1]))


main()
