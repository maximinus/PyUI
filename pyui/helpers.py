from enum import Enum, IntEnum
from dataclasses import dataclass


class Expand(IntEnum):
    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2
    BOTH = 3

    @property
    def horizontal(self) -> bool:
        return self.value % 2 == 1

    @property
    def vertical(self) -> bool:
        return self.value > 1


class Align:
    HORIZONTAL = Enum('Horizontal', ['LEFT', 'CENTER', 'RIGHT', 'STRETCH'])
    VERTICAL = Enum('Vertical', ['TOP', 'CENTER', 'BOTTOM', 'STRETCH'])

    def __init__(self, x, y):
        self.horizontal = x
        self.vertical = y


"""
class Alignment(IntEnum):
    LEFT = 3
    RIGHT = 5
    CENTER = 4
    TOP = 7
    BOTTOM = 1
    TOP_LEFT = 6
    TOP_RIGHT = 8
    BOTTOM_LEFT = 0
    BOTTOM_RIGHT = 2

    @property
    def horizontal(self):
        match self.value % 3:
            case 0:
                return Alignment.LEFT
            case 1:
                return Alignment.CENTER
            case _:
                return Alignment.RIGHT

    @property
    def vertical(self):
        match self.value // 3:
            case 0:
                return Alignment.BOTTOM
            case 1:
                return Alignment.CENTER
            case _:
                return Alignment.TOP
"""

@dataclass
class Position:
    x: int
    y: int

    def __eq__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return Position(self.x + other.x, self.y + other.y)


class Size:
    def __init__(self, width: int = 0, height: int = 0):
        if min([width, height]) < 0:
            raise ValueError("Size dimensions cannot be negative.")
        self.width = width
        self.height = height

    def __eq__(self, other):
        if not isinstance(other, Size):
            return NotImplemented
        return self.width == other.width and self.height == other.height

    def __add__(self, other):
        if not isinstance(other, Size):
            return NotImplemented
        return Size(self.width + other.width, self.height + other.height)

    def __sub__(self, other):
        if not isinstance(other, Size):
            return NotImplemented
        return Size(self.width - other.width, self.height - other.height)


class Margin:
    def __init__(self, left: int = 0, right: int = 0, top: int = 0, bottom: int = 0):
        """
        Initialize a Margin with specified values for left, right, top, and bottom.
        """
        if min([left, right, top, bottom]) < 0:
            raise ValueError("Margin values cannot be negative.")
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def __eq__(self, other):
        if not isinstance(other, Margin):
            return NotImplemented
        return (self.left == other.left and self.right == other.right and
                self.top == other.top and self.bottom == other.bottom)

    @property
    def size(self) -> Size:
        width = self.left + self.right
        height = self.top + self.bottom
        return Size(width, height)
    
    @property
    def width(self) -> int:
        return self.left + self.right

    @property
    def height(self) -> int:
        return self.top + self.bottom
