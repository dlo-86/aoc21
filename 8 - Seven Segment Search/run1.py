from pathlib import Path
from loguru import logger


@logger.catch()
def main():
    file_input = Path("input.txt")
    with file_input.open("r") as file_handle:
        input_lines = file_handle.readlines()
    digit_sum = 0
    for line in input_lines:
        digits = line.split("|")[1].strip().split()
        digit_sum += len([x for x in digits if len(x) == 2 or len(x) == 3 or len(x) == 4 or len(x) == 7])
    print(digit_sum)


main()
