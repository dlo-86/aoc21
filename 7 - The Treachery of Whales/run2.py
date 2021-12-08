import re
import sys
from pathlib import Path
from typing import List
from loguru import logger


def get_min_max(numbers: List[int]):
    min_number = max_mumber = numbers[0]
    for number in numbers:
        if number < min_number:
            min_number = number
        if number > max_mumber:
            max_mumber = number
    return min_number, max_mumber


@logger.catch()
def main():
    file_input = Path("input.txt")
    with file_input.open("r") as file_handle:
        input_lines = file_handle.readlines()
    numbers = [int(x) for x in input_lines[0].split(",")]
    min_number, max_number = get_min_max(numbers)
    diff_sum = sys.maxsize
    number_with_smallest_diff = None
    for i in range(min_number, max_number + 1):
        current_diff_sum = sum([abs(i - x) for x in numbers])
        if current_diff_sum < diff_sum:
            diff_sum = current_diff_sum
            number_with_smallest_diff = i
    print(number_with_smallest_diff, diff_sum)


main()
