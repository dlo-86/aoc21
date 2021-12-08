import copy
from pathlib import Path
from typing import List


def get_input():
    file_input = Path("input.txt")
    with file_input.open("r") as file_handle:
        lines = file_handle.readlines()
    return lines


def get_gamma_and_epsilon(word_list: List[str]):
    gamma = ""
    epsilon = ""
    length_of_words = len(word_list[0])
    for i in range(0, length_of_words-1):
        ones = [word[i] for word in word_list if word[i] == "1"]
        zeros = [word[i] for word in word_list if word[i] == "0"]
        if len(ones) > len(zeros):
            gamma += "1"
            epsilon += "0"
        elif len(zeros) > len(ones):
            gamma += "0"
            epsilon += "1"
        else:
            gamma += "1"
            epsilon += "0"
    return gamma, epsilon


def main():
    lines = get_input()
    oxygen_generator_rate_list = lines
    co2_scrubber_rate_list = lines
    length_of_words = len(lines[0])
    while True:
        found_one_value = False
        for i in range(0, length_of_words - 1):
            gamma, epsilon = get_gamma_and_epsilon(oxygen_generator_rate_list)
            oxygen_generator_rate_list = [word for word in oxygen_generator_rate_list if word[i] == gamma[i]]
            if 1 == len(oxygen_generator_rate_list):
                found_one_value = True
                break
        if found_one_value:
            break
    while True:
        found_one_value = False
        for i in range(0, length_of_words - 1):
            gamma, epsilon = get_gamma_and_epsilon(co2_scrubber_rate_list)
            co2_scrubber_rate_list = [word for word in co2_scrubber_rate_list if word[i] == epsilon[i]]
            if 1 == len(co2_scrubber_rate_list):
                found_one_value = True
                break
        if found_one_value:
            break
    oxygen_generator_int = int(oxygen_generator_rate_list[0], 2)
    co2_scrubber_rate_list = int(co2_scrubber_rate_list[0], 2)
    print(oxygen_generator_int, co2_scrubber_rate_list)
    print("result", oxygen_generator_int * co2_scrubber_rate_list)


main()

