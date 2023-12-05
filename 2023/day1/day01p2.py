import logging

logger = logging.getLogger(__name__)


def calculate_sum():
    total_sum = 0

    # Open input file
    with open(0) as f:
        # Read file
        for line in f.readlines():
            logger.debug(f"Line: {line}")
            first_digit = None
            last_digit = None
            for c in line:
                if not c.isdigit():
                    continue
                if first_digit is None:
                    first_digit = c
                last_digit = c
            logger.debug(f"First digit: {first_digit}, Last digit: {last_digit}")
            total_sum += int(f"{first_digit}{last_digit}")
    print(f"Total sum: {total_sum}")

    return total_sum


def calculate_sum_2():
    total_sum = 0

    # Open input file
    with open(0) as f:
        # Read file
        for line in f.readlines():
            logger.debug(f"Line: {line}")
            first_digit = None
            last_digit = None
            for c in line:
                if c.isdigit():
                    first_digit = c
                    break
            for c in reversed(line):
                if c.isdigit():
                    last_digit = c
                    break
            logger.debug(f"First digit: {first_digit}, Last digit: {last_digit}")
            total_sum += int(f"{first_digit}{last_digit}")
    print(f"Total sum (v2): {total_sum}")

    return total_sum


def calculate_sum_with_words():
    WORDS = [
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
    ]

    WORD_TO_DIGIT = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }

    def build_prefix_tree(reverse: bool = False):
        if reverse:
            maybe_reversed = lambda x: reversed(x)
        else:
            maybe_reversed = lambda x: x
        tree = {}
        for word in WORDS:
            current_node = tree
            prev_node = None
            last_character = None
            for c in maybe_reversed(word):
                last_character = c
                if c not in current_node:
                    current_node[c] = {}
                prev_node = current_node
                current_node = current_node[c]
            # Store int value of the word at the end of the tree
            prev_node[last_character] = WORD_TO_DIGIT[word]
        return tree

    prefix_tree = build_prefix_tree()
    print(prefix_tree)
    assert prefix_tree["t"]["w"]["o"] == "2", prefix_tree["t"]["w"]["o"]

    reversed_prefix_tree = build_prefix_tree(reverse=True)
    print(reversed_prefix_tree)
    assert reversed_prefix_tree["o"]["w"]["t"] == "2"

    def find_digit(line, prefix_tree: dict):
        current_nodes = []
        for c in line:
            current_nodes.append(prefix_tree)
            if c.isdigit():
                logger.info(f"Found numeric digit {c}")
                return c
            nodes_to_drop = []
            for i, _ in enumerate(current_nodes):
                node = current_nodes[i]
                if c not in node:
                    nodes_to_drop.append(i)
                    continue
                if isinstance(node[c], dict):
                    current_nodes[i] = node[c]
                else:
                    # Found a digit
                    logger.info(f"Found word digit {node[c]}")
                    return node[c]
        raise Exception(f"No digit found in line {line}")

    def digits_for_line(line: str):
        first_digit = find_digit(line=line, prefix_tree=prefix_tree)
        last_digit = find_digit(line=reversed(line), prefix_tree=reversed_prefix_tree)
        logger.debug(f"Digits: {first_digit}{last_digit}")
        return int(f"{first_digit}{last_digit}")

    assert digits_for_line("two35kxjtnbhxrmdhbgzeight") == 28
    assert digits_for_line("3nineonermn") == 31

    total_sum = 0

    # Open input file
    with open(0) as f:
        # Read file
        for i, line in enumerate(f.readlines()):
            logger.debug(f"Line: {line.strip()}")
            total_sum += digits_for_line(line)
            # if i > 10:
            #     break
    print(f"Total sum with words as digits: {total_sum}")

    return total_sum


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # print("Part one solutions:")
    # calculate_sum()
    # calculate_sum_2()
    print("Part two solutions:")
    calculate_sum_with_words()
