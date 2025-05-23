from enum import Enum, auto
from dataclasses import dataclass


class Alignment(Enum):
    LEFT = auto()
    RIGHT = auto
    CENTER = auto()
    TOP = auto()
    BOTTOM = auto()
    TOP_LEFT = auto()
    TOP_RIGHT = auto()
    BOTTOM_LEFT = auto()
    BOTTOM_RIGHT = auto()
    CENTER_LEFT = auto()
    CENTER_RIGHT = auto()
    CENTER_TOP = auto()
    CENTER_BOTTOM = auto()


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
