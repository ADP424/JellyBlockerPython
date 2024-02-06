from enum import Enum

class Jelly(Enum):
    EMPTY = '[]'
    GARBAGE = '💀'
    RED = '😡'
    GREEN = '🤢'
    BLUE = '🥶'
    PURPLE = '🌚'
    YELLOW = '🌝'

class JellyBlock:
    """
    A single jelly block.

    Attributes
    ----------
    color : Jelly, default: Jelly.EMPTY
        The color of the jelly block.
    
    falling : bool, default: False
        Whether the jelly block is falling (controlled by the player) or not.

    row : int, default: 0
        The row of the board that the jelly block is in.

    col : int, default: 0
        The column of the board that the jelly block is in.
    """

    def __init__(self, color=Jelly.EMPTY, falling=False, row=-10, col=-10):
        self.color = color
        self.falling = falling
        self.row = row
        self.col = col