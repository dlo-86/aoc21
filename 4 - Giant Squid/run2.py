from pathlib import Path
from typing import List
from loguru import logger


class BingoBoard:
    def __init__(self, lines):
        self.lines = []
        for line in lines:
            line = line.strip()
            self.lines.append([int(x) for x in line.split()])
        self.marked_numbers = []

    def add_marked_number(self, number):
        self.marked_numbers.append(number)

    def check_bingo(self):
        return self.check_rows() or self.check_lines()

    def check_rows(self):
        for i in range(0, 5):
            for j in range(0, 5):
                if not self.lines[j][i] in self.marked_numbers:
                    break
            else:
                return True
        return False

    def check_lines(self):
        for i in range(0, 5):
            for j in range(0, 5):
                if not self.lines[i][j] in self.marked_numbers:
                    break
            else:
                return True
        return False

    def get_sum_of_unmarked_numbers(self):
        unmarked_number_sum = 0
        for i in range(0, 5):
            for j in range(0, 5):
                if not self.lines[i][j] in self.marked_numbers:
                    unmarked_number_sum += self.lines[i][j]
        return unmarked_number_sum


def get_bingo_numbers(lines) -> List[int]:
    return [int(x) for x in lines[0].split(",")]


def get_bingo_boards(lines):
    bingo_boards = []
    for i in range(2, len(lines)-1, 6):
        bingo_boards.append(BingoBoard(lines[i:i+5]))
    return bingo_boards


def mark_bingo_numbers(number: int, bingo_boards: List[BingoBoard]):
    for bingo_board in bingo_boards:
        bingo_board.add_marked_number(number)


def get_boards_without_bingo(bingo_boards: List[BingoBoard]):
    boards_without_bingo: List[BingoBoard] = []
    for bingo_board in bingo_boards:
        if not bingo_board.check_bingo():
            boards_without_bingo.append(bingo_board)
    return boards_without_bingo


def play(bingo_numbers: List[int], bingo_boards: List[BingoBoard]):
    for number in bingo_numbers:
        mark_bingo_numbers(number, bingo_boards)
        if len(bingo_boards) == 1:
            bingo_board = bingo_boards[0]
            if bingo_board.check_bingo():
                return number * bingo_board.get_sum_of_unmarked_numbers()
        bingo_boards = get_boards_without_bingo(bingo_boards)


@logger.catch()
def main():
    file_input = Path("input.txt")
    with file_input.open("r") as file_handle:
        lines = file_handle.readlines()
    bingo_numbers = get_bingo_numbers(lines)
    bingo_boards = get_bingo_boards(lines)
    result = play(bingo_numbers, bingo_boards)
    print(result)


main()
