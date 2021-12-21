import itertools
from typing import Dict, List
from loguru import logger


def roll_dice(dice, player_positions, active_player):
    player_positions[active_player] = (player_positions[active_player] + dice - 1) % 10 + 1


def increase_dice_value(dice):
    dice = dice + 1
    if dice > 100:
        dice -= 100
    return dice


def play():
    player_positions = [3, 7]
    player_scores = [0, 0]
    active_player = 0
    dice = 1
    dice_count = 0
    while True:
        for i in range(3):
            roll_dice(dice, player_positions, active_player)
            dice = increase_dice_value(dice)
            dice_count += 1
        player_scores[active_player] += player_positions[active_player]
        if player_scores[active_player] >= 1000:
            return player_scores, dice_count
        active_player = (active_player + 1) % 2


def play_with_quantum_die():
    player_positions = [3, 7]
    results = {}
    player_scores = [0, 0]
    active_player = 0
    player1_wins, player2_wins = play_combinations(player_positions.copy(), player_scores.copy(),
                                                   active_player, results)
    return max(player1_wins, player2_wins)


def play_with_quantum_die_step(player_positions, player_scores, active_player, throws: List[int], results):
    for throw in throws:
        roll_dice(throw, player_positions, active_player)
    player_scores[active_player] += player_positions[active_player]
    if player_scores[active_player] >= 21:
        if active_player == 0:
            return 1, 0
        else:
            return 0, 1
    active_player = int(not active_player)
    player1_wins, player2_wins = play_combinations(player_positions.copy(), player_scores.copy(),
                                                   active_player, results)
    return player1_wins, player2_wins


def play_combinations(player_positions, player_scores, active_player, results):
    player1_wins = 0
    player2_wins = 0
    combinations = itertools.product([1, 2, 3], repeat=3)
    for combination in combinations:
        key = tuple(player_positions + player_scores + [active_player] + list(combination))
        if key in results:
            new1, new2 = results[key]
        else:
            new1, new2 = play_with_quantum_die_step(player_positions.copy(), player_scores.copy(), active_player,
                                                    combination, results)
            results[key] = (new1, new2)
        player1_wins += new1
        player2_wins += new2
    return player1_wins, player2_wins


def part_one():
    player_scores, dice_count = play()
    print("Result 1:", min(player_scores) * dice_count)


def part_two():
    max_wins = play_with_quantum_die()
    print("Result 2:", max_wins)


@logger.catch()
def main():
    part_one()
    part_two()


main()
