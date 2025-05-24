from enum import IntEnum
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


@dataclass
class Size:
    width: int
    height: int

    def __eq__(self, other):
        if not isinstance(other, Size):
            return NotImplemented
        return self.width == other.width and self.height == other.height

    def __add__(self, other):
        if not isinstance(other, Size):
            return NotImplemented
        return Size(self.width + other.width, self.height + other.height)

@dataclass
class Margin:
    left: int
    right: int
    top: int
    bottom: int

    @classmethod
    def none(cls):
        return cls(left=0, right=0, top=0, bottom=0)

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
