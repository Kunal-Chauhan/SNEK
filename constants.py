from typing import Union, Tuple, List, Dict


# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (238, 111, 87)
PINK = (255, 203, 203)
DARK_BLUE = (0, 51, 78)
BLUE = (44, 62, 80)
LIGHT_BLUE = (187, 225, 250)
GREEN = (39, 174, 96)
GOLDEN = (255, 224, 93)
CREAM = (255, 248, 205)
# Screen
WIDTH, HEIGHT = 700, 700
SIZE = (WIDTH, HEIGHT)

COLUMNS, ROWS = 20, 20

W = WIDTH // COLUMNS
H = HEIGHT // ROWS

# Algorithm Selection
DFS = 1
BFS = 0


# for Server-Client framework
class State:
    _noOfStates = 5
    init, ready, waiting, busy, run = range(_noOfStates)
    # ready: has done the work and are ready to go
    # waiting: '' for the other player
    # busy: doing the work
    # run: start signal, the game has begun

    def __init__(self):
        self.current = State.init

    def __eq__(self, other):
        return True if self.current == other else False

    def __ne__(self, other):
        return True if self.current != other else False

    def __repr__(self):
        if self.current == State.waiting:
            return "Waiting for player..."
        elif self.current == State.ready:
            return "Player is done!"
        elif self.current == State.busy:
            return "Player is drawing!"
        else:
            return "not set"

    def set(self, state: int):
        if state < State._noOfStates:
            self.current = state
        else:
            raise IndexError


# Data Types Aliases for Static Typing
class Type:
    Signal = int
    Basic = Union[bool, tuple, int, str, list, dict]
    Grid = Dict[str, Union[Tuple, List]]
    Packet = Tuple[Tuple[int, int], Signal, Grid]
