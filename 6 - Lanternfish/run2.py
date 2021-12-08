from pathlib import Path
from loguru import logger


class LanternFishSimulator:
    def __init__(self, initial_state: str):
        fishes = [int(x) for x in initial_state.split(",")]
        self.fishes = {}
        for i in range(0,9):
            self.fishes[i] = fishes.count(i)

    def get_amount_of_fishes(self):
        fish_sum = 0
        for number_fishes in self.fishes.values():
            fish_sum += number_fishes
        return fish_sum

    def simulate(self, days: int):
        for i in range(0, days):
            self.simulate_one_day()

    def simulate_one_day(self):
        new_fish_stocks = {}
        for i in range(1, 9):
            new_fish_stocks[i-1] = self.fishes[i]
        new_fish_stocks[6] += self.fishes[0]
        new_fish_stocks[8] = self.fishes[0]
        self.fishes = new_fish_stocks


@logger.catch()
def main():
    file_input = Path("input.txt")
    with file_input.open("r") as file_handle:
        input_lines = file_handle.readlines()
    simulator = LanternFishSimulator(input_lines[0])
    simulator.simulate(256)
    print(simulator.get_amount_of_fishes())


main()
