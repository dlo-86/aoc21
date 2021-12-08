import re
import sys
from pathlib import Path
from typing import List
from loguru import logger


class DistanceCostCalculator:
    def __init__(self, max_range):
        self.distance_to_cost = {}
        cost_sum = 0
        for i in range(0, max_range + 1):
            cost_sum += i
            self.distance_to_cost[i] = cost_sum


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
    number_range = abs(max_number - min_number)
    diff_sum = sys.maxsize
    number_with_smallest_diff = None
    distance_cost_calculator = DistanceCostCalculator(number_range)
    for i in range(min_number, max_number + 1):
        current_diff_sum = sum([distance_cost_calculator.distance_to_cost[abs(i - x)] for x in numbers])
        if current_diff_sum < diff_sum:
            diff_sum = current_diff_sum
            number_with_smallest_diff = i
    print(number_with_smallest_diff, diff_sum)



main()
