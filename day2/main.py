import logging

logger = logging.getLogger(__name__)


def id_of_game_or_zero(line: str) -> int:
    line.split(":")



def calculate_sum() -> int:
    total_sum = 0

    # Open input file
    with open("input.txt", "r") as f:
        # Read file
        for line in f.readlines():
            total_sum += id_of_game_or_zero(line)
    return total_sum


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # print("Part one solutions:")
    calculate_sum()
