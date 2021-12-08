import itertools
import re
import sys
from pathlib import Path
from typing import List, Dict
from loguru import logger


class Decoder:
    def __init__(self):
        self.mapping:Dict[str, int] = {}

    def _get_digit_with_length(self, digit_list, length, number):
        digits = [x for x in digit_list if len(x) == length]
        if digits:
            self.mapping[digits[0]] = number

    @staticmethod
    def _check_if_digit_is_covered_by_digit(digit:str, cover_digit:str):
        for char in digit:
            if char not in cover_digit:
                return False
        return True

    def _identify_digits_with_five_segments(self, digit_list):
        considered_digits = [x for x in digit_list if len(x) == 5]
        self._extract_three(considered_digits)
        self._extract_five(considered_digits)
        self._extract_two(considered_digits)

    def _extract_two(self, considered_digits):
        assert len(considered_digits) == 1
        self.mapping[considered_digits[0]] = 2

    def _extract_five(self, considered_digits):
        assert 9 in self.mapping.values()
        for digit in considered_digits:
            if self._check_if_digit_is_covered_by_digit(digit, self._get_by_number(9)):
                self.mapping[digit] = 5
                considered_digits.remove(digit)
                break

    def _extract_three(self, considered_digits):
        assert 7 in self.mapping.values()
        for digit in considered_digits:
            if self._check_if_digit_is_covered_by_digit(self._get_by_number(7), digit):
                self.mapping[digit] = 3
                considered_digits.remove(digit)
                break

    def _identify_digits_with_six_segments(self, digit_list):
        considered_digits = [x for x in digit_list if len(x) == 6]
        self._extract_six(considered_digits)
        self._extract_nine(considered_digits)
        self._extract_zero(considered_digits)

    def _extract_zero(self, considered_digits):
        assert len(considered_digits) == 1
        self.mapping[considered_digits[0]] = 0

    def _extract_nine(self, considered_digits):
        assert 4 in self.mapping.values()
        for digit in considered_digits:
            if self._check_if_digit_is_covered_by_digit(self._get_by_number(4), digit):
                self.mapping[digit] = 9
                considered_digits.remove(digit)
                break

    def _extract_six(self, considered_digits):
        assert 7 in self.mapping.values()
        for digit in considered_digits:
            if not self._check_if_digit_is_covered_by_digit(self._get_by_number(7), digit):
                self.mapping[digit] = 6
                considered_digits.remove(digit)
                break

    def identify_mapping(self, digit_list: List[str]):
        self._get_digit_with_length(digit_list, 2, 1)
        self._get_digit_with_length(digit_list, 3, 7)
        self._get_digit_with_length(digit_list, 4, 4)
        self._get_digit_with_length(digit_list, 7, 8)
        self._identify_digits_with_six_segments(digit_list)
        self._identify_digits_with_five_segments(digit_list)

    def _get_by_number(self, number):
        for key, value in self.mapping.items():
            if value == number:
                return key
        return None

    def decode(self, digit_list: List[str]):
        digit_sum = 0
        multiplier = 1
        for i in reversed(digit_list):
            digit_sum += self.mapping[i] * multiplier
            multiplier *= 10
        return digit_sum


@logger.catch()
def main():
    file_input = Path("input.txt")
    with file_input.open("r") as file_handle:
        input_lines = file_handle.readlines()
    digit_sum = decode_all_digits(input_lines)
    print(digit_sum)


def decode_all_digits(input_lines):
    digit_sum = 0
    for line in input_lines:
        first_digits, second_digits = extract_digits(line)
        decoder = Decoder()
        decoder.identify_mapping(first_digits)
        digit_sum += decoder.decode(second_digits)
    return digit_sum


def extract_digits(line):
    first_digits, second_digits = line.split("|")
    first_digits = sort_segments(first_digits.strip().split())
    second_digits = sort_segments(second_digits.strip().split())
    return first_digits, second_digits


def sort_segments(digit_list: List[str]):
    return_list = []
    for element in digit_list:
        e = list(element)
        e.sort()
        return_list.append("".join(e))
    return return_list


main()
