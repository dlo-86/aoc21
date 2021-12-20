import math
from pathlib import Path
from typing import Dict, List
from loguru import logger


version_counter = 0


def parse_integer_value(i, length, binary_number):
    value = int(binary_number[i:i+length], 2)
    return i + length, value


def parse_binary_string(i, length, binary_number):
    value = binary_number[i:i+length]
    return i + length, value


def parse_packet(i, binary_number):
    global version_counter
    i, version_number = parse_integer_value(i, 3, binary_number)
    version_counter += version_number
    i, packet_type = parse_integer_value(i, 3, binary_number)
    if packet_type == 4:
        return parse_number(binary_number, i)
    else:
        return parse_operation(binary_number, i, packet_type)


def parse_operation(binary_number, i, packet_type):
    length_type = int(binary_number[i], 2)
    i += 1
    numbers = []
    if length_type == 0:
        i = extract_numbers_with_binary_length(binary_number, i, numbers)
    elif length_type == 1:
        i = extract_numbers_with_number_packets(binary_number, i, numbers)
    else:
        assert False, "The length type must be 0 or 1"
    result = process_numbers(packet_type, numbers)
    return i, result


def extract_numbers_with_number_packets(binary_number, i, numbers):
    i, number_packets = parse_integer_value(i, 11, binary_number)
    packet_counter = 0
    while True:
        i, number = parse_packet(i, binary_number)
        numbers.append(number)
        packet_counter += 1
        if packet_counter == number_packets:
            break
    return i


def extract_numbers_with_binary_length(binary_number, i, numbers):
    i, binary_length = parse_integer_value(i, 15, binary_number)
    start = i
    while True:
        i, number = parse_packet(i, binary_number)
        numbers.append(number)
        if start + binary_length == i:
            break
    return i


def parse_number(binary_number, i):
    number = ""
    while True:
        i, intermediate_value = parse_integer_value(i, 1, binary_number)
        i, new_number = parse_binary_string(i, 4, binary_number)
        number += new_number
        last_value = not intermediate_value
        if last_value:
            break
    return i, int(number, 2)


def process_numbers(packet_type: int, numbers: List[int]):
    if packet_type == 0:
        return sum(numbers)
    elif packet_type == 1:
        return math.prod(numbers)
    elif packet_type == 2:
        return min(numbers)
    elif packet_type == 3:
        return max(numbers)
    elif packet_type == 5:
        return int(numbers[0] > numbers[1])
    elif packet_type == 6:
        return int(numbers[0] < numbers[1])
    elif packet_type == 7:
        return int(numbers[0] == numbers[1])


def get_binary_number(hex_number: str):
    binary_number = ""
    for digit in hex_number:
        binary_number += str(bin(int(digit, 16)))[2:].zfill(4)
    return binary_number


def part_one(input_file: Path):
    input_lines = read_input(input_file)
    binary_number = get_binary_number(input_lines[0])
    i = 0
    parse_packet(i, binary_number)
    print("Result 1:", version_counter)


def part_two(input_file: Path):
    input_lines = read_input(input_file)
    binary_number = get_binary_number(input_lines[0])
    i = 0
    result = parse_packet(i, binary_number)[1]
    print("Result 2:", result)


def read_input(input_file: Path):
    with input_file.open("r") as file_handle:
        input_lines = file_handle.readlines()
        return input_lines


@logger.catch()
def main():
    part_one(Path("input.txt"))
    part_two(Path("input.txt"))


main()
