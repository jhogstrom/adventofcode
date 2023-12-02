from timer import timeit
from collections import defaultdict, deque
import logging
from reader import get_data, set_logging

runtest = True
runtest = False
set_logging(runtest)
stardate = "2"

# logging.basicConfig(level=logging.DEBUG, format="%(message)s")

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
            s (str): _description_
        """
        self.gamestr = s
        number, hands = s.split(":")
        self.game_number = int(number.split()[1].strip())
        self.hands = []
        for hand in hands.split(";"):
            self.hands.append(self.parse_hand(hand))

    def parse_hand(self, hand: str) -> dict:
        """
        Parses a hand string on the form "3 blue, 4 red" into a dict
        Args:
            hand (str): _description_
        """
        hand = hand.strip()
        hand_dict = defaultdict(int)
        for cube in hand.split(","):
            cube = cube.strip()
            if not cube:
                continue
            number, color = cube.split()
            hand_dict[color] += int(number)
        return hand_dict

    def __repr__(self) -> str:
        return self.gamestr

    def is_possible(self, template_set: dict) -> bool:
        """
        Checks if the game is possible with the template set.
        Args:
            template_set (dict): _description_
        """
        for hand in self.hands:
            for color, number in hand.items():
                if template_set[color] < number:
                    logging.debug(f">> {self} \n\t{color}: {number} > {template_set[color]}")
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


@timeit
def star1(data):
    games = []
    for line in data:
        games.append(Game(line))
    # print(games)

    template_set = {
        "red": 12,
        "blue": 14,
        "green": 13,
    }
    result = 0
    for _ in games:
        if _.is_possible(template_set):
            # print(_)
            result += _.game_number
    print(result)


@timeit
def star2(data):
    games = []
    for line in data:
        games.append(Game(line))
    res = 0
    for _ in games:
        m = _.minimum_set()
        factors = list(m.values())
        res += factors[0] * factors[1] * factors[2]

    print(res)


data2 = data[:]

star1(data)
star2(data2)