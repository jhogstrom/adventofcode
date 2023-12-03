from math import prod
from collections import defaultdict
from reader import get_data, set_logging, timeit

stardate = "2"
runtest = True
runtest = False
set_logging(runtest)
data = get_data(stardate, runtest)


class Game:
    def __init__(self, s: str) -> None:
        """
        The game is initialized with a string on the form
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        where the first part is the game number, followed by "hands"
        separated by semicolon. Each hand is a set of colored cubes. Each hand is stored as an item in an array
        of hands. Each hand is a dict with color as key and number of cubes as value.
        Args:
            s (str): String describing game
        """
        self.gamestr = s
        number, hands = s.split(":")
        self.game_number = int(number.split()[1].strip())
        self.hands = [self.parse_hand(hand) for hand in hands.split(";")]

    def parse_hand(self, hand: str) -> dict:
        """
        Parses a hand string on the form "3 blue, 4 red" into a dict
        Args:
            hand (str): string describing hand on the form <color>: count
        """
        hand_dict = defaultdict(int)
        for cube in hand.split(","):
            count, color = cube.split()
            hand_dict[color] += int(count)
        return hand_dict

    def __repr__(self) -> str:
        return self.gamestr

    def is_possible(self, template_set: dict) -> bool:
        """
        Checks if the game is possible with the template set.
        Args:
            template_set (dict): counts per color
        """
        for hand in self.hands:
            if not all(template_set[color] >= number for color, number in hand.items()):
                return False
        return True

    def minimum_set(self) -> dict:
        """
        Returns the minimum set of cubes needed to play the game.
        """
        result = defaultdict(int)
        for hand in self.hands:
            for color, number in hand.items():
                result[color] = max(result[color], number)
        return result

    def power(self):
        """
        Returns the power of the game
        """
        return prod(self.minimum_set().values())


@timeit
def star1(data):
    template_set = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }
    result = sum([_.game_number
                  for _ in [Game(_) for _ in data]
                  if _.is_possible(template_set)])
    print(result)


@timeit
def star2(data):
    print(sum([Game(_).power() for _ in data]))

star1(data)
star2(data)
