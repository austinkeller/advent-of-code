from collections import deque

total_sum = 0


# Turn list of strings into dict of strings and their counts
def count_set(li: list[str]) -> dict[str, int]:
    d = {}
    for s in li:
        if s in d:
            d[s] += 1
        else:
            d[s] = 1
    return d


extra_cards = deque()


# Open input file
with open(0) as f:
    # Read file
    for i, line in enumerate(f.readlines()):
        print(f"Card {i + 1}")
        line = line.strip()
        _, line = line.split(':')
        line = line.strip()
        winning_nums, card_nums = line.split('|')
        winning_nums = winning_nums.strip().split(' ')
        # Filter out empty strings
        winning_nums = list(filter(None, winning_nums))
        card_nums = card_nums.strip().split(' ')
        # Filter out empty strings
        card_nums = list(filter(None, card_nums))

        # Count unique numbers in each list
        winning_nums = count_set(winning_nums)
        card_nums = count_set(card_nums)

        num_wins = 0

        # Add points for each winning number in the card
        for num, count in winning_nums.items():
            if num in card_nums:
                num_wins += 1
        
        print(f"Won {num_wins} times")

        # Get extra cards for this card (if any)
        try:
            extra_cards_for_this_card = extra_cards.popleft()
        except IndexError:
            extra_cards_for_this_card = 0

        print(f"Extra cards for card {i + 1}: {extra_cards_for_this_card}")

        total_sum += 1 + (num_wins * (extra_cards_for_this_card + 1))

        print(f"Won {extra_cards_for_this_card + 1} copies of {num_wins} cards")

        # Add extra cards to the list
        for j in range(num_wins):
            if j == len(extra_cards):
                extra_cards.append(extra_cards_for_this_card + 1)
            else:
                extra_cards[j] += extra_cards_for_this_card + 1


print(f"Total sum: {total_sum}")
