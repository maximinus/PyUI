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
    LEFT = 1
    RIGHT = 2
    TOP = 4
    BOTTOM = 8
    CENTER = 16

    def __init__(self, alignment):
        self.alignment = alignment

    def horizontal(self):
        horizontal_alignment = self.alignment & (self.LEFT | self.RIGHT)
        return horizontal_alignment if horizontal_alignment else self.CENTER

    def vertical(self):
        vertical_alignment = self.alignment & (self.TOP | self.BOTTOM)
        return vertical_alignment if vertical_alignment else self.CENTER


class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def add_margin(self, margin):
        width = self.width + margin.left + margin.right
        height = self.height + margin.top + margin.bottom
        return Size(width, height)

    def subtract_margin(self, margin):
        width = self.width - (margin.left + margin.right)
        height = self.height - (margin.top + margin.bottom)
        return Size(width, height)

    def __add__(self, other):
        return Size(self.width + other.width, self.height + other.height)

    def __eq__(self, other):
        if isinstance(other, Size):
            return self.width == other.width and self.height == other.height
        return False

    def __repr__(self):
        return f'Size(width={self.width}, height={self.height})'
