from dataclasses import dataclass
from functools import total_ordering, cached_property
from enum import Enum
from typing import Optional

JOKER_RULE = True
if JOKER_RULE:
    CARD_ORDERING = "J23456789TQKA"
else:
    CARD_ORDERING = "23456789TJQKA"


@total_ordering
class Card:
    def __init__(self, c: str):
        assert len(c) == 1
        assert c in CARD_ORDERING
        self.symbol = c

    @cached_property
    def rank(self) -> int:
        return CARD_ORDERING.index(self.symbol)

    def __lt__(self, other):
        return self.rank < other.rank

    def __eq__(self, other):
        return self.rank == other.rank

    def __hash__(self):
        return self.symbol.__hash__()


assert Card("A") > Card("K")
assert Card("K") < Card("A")
assert Card("2") < Card("3")
assert Card("2") == Card("2")
assert Card("T") == Card("T")


@total_ordering
class HandType(Enum):
    UNDEFINED = 0
    HIGH_CARD = 1
    ONE_PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    FULL_HOUSE = 5
    FOUR_OF_A_KIND = 6
    FIVE_OF_A_KIND = 7

    def __lt__(self, other):
        return self.value < other


assert HandType.HIGH_CARD < HandType.ONE_PAIR
assert HandType.HIGH_CARD == HandType.HIGH_CARD


@total_ordering
@dataclass
class Hand:
    cards_string: str
    _original_cards_string: Optional[str] = None

    @cached_property
    def original_cards_string(self) -> str:
        return (
            self._original_cards_string
            if self._original_cards_string is not None
            else self.cards_string
        )

    @staticmethod
    def cards_string_to_cards(cards_string: str) -> list[Card]:
        cards_string = cards_string.strip()
        assert len(cards_string) == 5
        return list(Card(x) for x in cards_string.strip())

    @cached_property
    def cards(self):
        return Hand.cards_string_to_cards(self.cards_string)

    @cached_property
    def original_cards(self):
        return Hand.cards_string_to_cards(self.original_cards_string)

    @cached_property
    def type(self):
        card_map = {}
        for c in self.cards:
            if c not in card_map:
                card_map[c] = 1
            else:
                card_map[c] += 1
        counts = list(sorted(card_map.values()))
        if 5 in counts:
            return HandType.FIVE_OF_A_KIND
        elif 4 in counts:
            return HandType.FOUR_OF_A_KIND
        elif 3 in counts:
            if 2 in counts:
                return HandType.FULL_HOUSE
            return HandType.THREE_OF_A_KIND
        if 2 in counts:
            if counts[-2] == 2:
                return HandType.TWO_PAIR
            return HandType.ONE_PAIR
        return HandType.HIGH_CARD

    def __lt__(self, other):
        if not isinstance(other, Hand):
            return False
        if self.type == other.type:
            return self.original_cards < other.original_cards
        return self.type < other.type

    # def __eq__(self, other):
    #     if not isinstance(other, Hand):
    #         return False
    #     return hash(self) == hash(other)

    # def __hash__(self):
    #     return self.original_cards_string.__hash__()


assert Hand("33332").type == HandType.FOUR_OF_A_KIND
assert Hand("2AAAA").type == HandType.FOUR_OF_A_KIND
assert Hand("T55J5").type == HandType.THREE_OF_A_KIND
assert Hand("ATATA").type == HandType.FULL_HOUSE

assert Hand("33332") > Hand("2AAAA")
assert Hand("33332") == Hand("33332")
assert Hand("TT999") != 1

assert Hand("KTJJT") < Hand("KK677")

# assert hash(Hand("22873", "J2873")) == hash(Hand("J2873"))

# assert hash(Hand("T5TT5", "T5JT5")) == hash(Hand("T5JT5"))


def find_max_hand_with_jokers(hand: Hand) -> Hand:
    """
    Depth-first search for max hand
    """
    # Find first joker
    j = Card("J")
    j = hand.cards.index(j) if j in hand.cards else None
    if j is None:
        return hand
    hand_candidates = [hand]
    for c in CARD_ORDERING:
        if c == "J":
            continue
        hand_candidates.append(
            find_max_hand_with_jokers(
                Hand(
                    hand.cards_string[:j] + c + hand.cards_string[(j + 1) :],
                    hand.original_cards_string,
                )
            )
        )
    return max(hand_candidates)


if __name__ == "__main__":
    hand_to_bid = {}
    hand_to_joker_hand = []
    hands = []
    # Open input file
    with open(0) as f:
        # Read file
        for line in f.readlines():
            hand, bid = line.split(" ")
            hand = Hand(hand)
            assert hand.original_cards_string not in hand_to_bid
            hand_to_bid[hand.original_cards_string] = int(bid)
            if JOKER_RULE:
                hand = find_max_hand_with_jokers(hand)
            assert (
                hand.original_cards_string in hand_to_bid
            ), f"{hand} not in hands to bid map"
            hands.append(hand)
    winnings = 0
    for rank, hand in enumerate(sorted(hands)):
        bid = hand_to_bid[hand.original_cards_string]
        print(
            f"Win: {rank + 1}\t{hand.type}\t{hand.cards_string}\t{hand.original_cards_string}\t{bid}"
        )
        winnings += (rank + 1) * bid
    print(winnings)
