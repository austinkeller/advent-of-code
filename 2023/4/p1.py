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


# Open input file
with open(0) as f:
    # Read file
    for i, line in enumerate(f.readlines()):
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

        card_points = 0

        # Add points for each winning number in the card
        for num, count in winning_nums.items():
            if num in card_nums:
                # Bit shift card points by 1 to double the point value
                card_points = max(1, card_points << 1)
        total_sum += card_points


print(f"Total sum: {total_sum}")
