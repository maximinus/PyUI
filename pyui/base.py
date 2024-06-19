from enum import Enum, auto


class Color:
    # we don't use enums as they return the enum, not the value
    RED = (192, 32, 32)
    GREEN = (32, 192, 32)
    BLUE = (32, 32, 192)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)


class Expand(Enum):
    NONE = auto()
    HORIZONTAL = auto()
    VERTICAL = auto()
    BOTH = auto()

    @property
    def is_horizontal(self):
        return self in [Expand.HORIZONTAL, Expand.BOTH]

    @property
    def is_vertical(self):
        return self in [Expand.VERTICAL, Expand.BOTH]


class Margin:
    def __init__(self, left=0, right=0, top=0, bottom=0):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom


class Align:
    START = 0
    CENTER = 1
    END = 2

    def __init__(self, horizontal=START, vertical=START):
        self.horizontal = horizontal
        self.vertical = vertical


class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def add_margin(self, margin):
        width = self.width + margin.left + margin.right
        height = self.height + margin.top + margin.bottom
        return Size(width, height)

    def __add__(self, other):
        return Size(self.width + other.width, self.height + other.height)
