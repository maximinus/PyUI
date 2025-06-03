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


class Align:
    LEFT = 1
    CENTER = 2
    RIGHT = 3
    TOP = 4
    BOTTOM = 5
    FILL = 6

    def __init__(self, x, y):
        assert x in (self.LEFT, self.CENTER, self.RIGHT, self.FILL), "Invalid horizontal alignment"
        assert y in (self.TOP, self.CENTER, self.BOTTOM, self.FILL), "Invalid vertical alignment"
        self.horizontal = x
        self.vertical = y


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
    
    def __sub__(self, other):
        if not isinstance(other, Position):
            return NotImplemented
        return Position(self.x - other.x, self.y - other.y)

    def copy(self):
        return Position(self.x, self.y)

    @property
    def as_tuple(self):
        return (self.x, self.y)


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

    @property
    def as_tuple(self):
        return (self.width, self.height)

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


class MouseButtonState:
    def __init__(self):
        self.state = False
        self.up = False
        self.down = False

    def update(self, new_state):
        self.up = self.state and not new_state
        self.down = not self.state and new_state
        self.state = new_state

class Mouse:
    """
    A class that stores the state of the mouse.
    Includes position and button states.
    """
    def __init__(self):
        self.position = Position(0, 0)
        self.old_position = Position(0, 0)
        self.left = MouseButtonState()
        self.middle = MouseButtonState()
        self.right = MouseButtonState()

    def update(self, position, buttons):
        """
        Update the mouse state with the current position and button states.
        
        Args:
            position: A tuple of (x, y) coordinates
            buttons: A tuple of button states (left, middle, right)
        """
        self.old_position = self.position.copy()
        self.position = Position(position[0], position[1])

        self.left.update(buttons[0])
        self.middle.update(buttons[1])
        self.right.update(buttons[2])
