import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Round:
    red: int = 0
    blue: int = 0
    green: int = 0


LIMIT_ROUND = Round(red=12, green=13, blue=14)


def parse_round(round: str) -> Round:
    chunks = round.split(",")
    round_dict = {}
    for chunk in chunks:
        number, color = chunk.strip().split(" ")
        round_dict[color] = int(number)
    return Round(**round_dict)


def is_round_possible(round: Round) -> bool:
    return (
        round.red <= LIMIT_ROUND.red
        and round.blue <= LIMIT_ROUND.blue
        and round.green <= LIMIT_ROUND.green
    )


def id_of_game_or_zero(line: str) -> int:
    game, rounds = line.split(":")

    rounds = rounds.strip().split(";")
    for r_str in rounds:
        round = parse_round(r_str)
        if not is_round_possible(round):
            return 0

    game = game.removeprefix("Game ")
    game_id = int(game)
    return game_id


def calculate_sum() -> int:
    total_sum = 0

    # Open input file
    with open("input.txt", "r") as f:
        # Read file
        for line in f.readlines():
            total_sum += id_of_game_or_zero(line)
    return total_sum


def power_of_game(line: str) -> int:
    # find minimum for each color
    min_round = Round()

    game, rounds = line.split(":")

    rounds = rounds.strip().split(";")
    for r_str in rounds:
        round = parse_round(r_str)
        min_round.red = max(min_round.red, round.red)
        min_round.blue = max(min_round.blue, round.blue)
        min_round.green = max(min_round.green, round.green)
    return min_round.red * min_round.blue * min_round.green


def calculate_sum_2() -> int:
    total_sum = 0

    # Open input file
    with open("input.txt", "r") as f:
        # Read file
        for line in f.readlines():
            total_sum += power_of_game(line)
    return total_sum


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print("Part one solutions:")
    print(f"Sum: {calculate_sum()}")
    print("Part two solutions:")
    print(f"Sum: {calculate_sum_2()}")
