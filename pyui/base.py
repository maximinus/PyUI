import json
import os.path
import pygame

from pathlib import Path
from enum import Enum, auto


class Color:
    # we don't use enums as they return the enum, not the value
    RED = (192, 32, 32)
    GREEN = (32, 192, 32)
    BLUE = (32, 32, 192)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    BACKGROUND = (232, 232, 232)


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


class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Position(x={self.x}, y={self.y})'

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        if isinstance(other, Position):
            return self.x == other.y and self.x == other.y
        return False

    def copy(self):
        return Position(self.x, self.y)


class Size:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def invert(self):
        tmp = self.width
        self.width = self.height
        self.height = tmp

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


def load_json(filepath):
    with open(filepath) as f:
        return json.load(f)


def get_asset(asset_name):
    # relative to this file, the assets are in ../assets
    assets_path = Path(__file__).parent.parent / 'assets'
    fullpath = assets_path / asset_name
    if not os.path.exists(fullpath):
        raise OSError(f'File {fullpath} does not exist')
    if fullpath.suffix == '.png':
        # load image as alpha and return
        return pygame.image.load(fullpath).convert_alpha()
    if fullpath.suffix == '.json':
        return load_json(fullpath)
    raise RuntimeError(f'File type {fullpath.suffix} not supported')


class TextStyle:
    def __init__(self, font, size, color):
        self.font = pygame.font.match_font(font)
        self.size = size
        self.color = color

    @classmethod
    def from_json_data(cls, data):
        return cls(data['font'], data['size'], data['color'])


class NinePatch:
    def __init__(self, name):
        # 9 patch is stored in 2 files: the image and the data
        data = get_asset(f'nine_patch/{name}.json')
        self.top = data['top']
        self.bottom = data['bottom']
        self.left = data['left']
        self.right = data['right']
        self.size = Size(data['width'], data['height'])
        self.image = get_asset(f'nine_patch/{name}.png')
        self.background = data['background']

    def get_margins(self):
        return Margin(self.left, self.right, self.top, self.bottom)

    def draw(self, new_size):
        # draw the top left
        x = 0
        y = 0
        image_size = new_size
        texture = pygame.Surface((new_size.width, new_size.height), pygame.SRCALPHA)
        pygame.draw.rect(texture, self.background, (1, 1, new_size.width - 2, new_size.height - 2))

        # draw the corners
        texture.blit(self.image, (x, y), (0, 0, self.left, self.top))
        texture.blit(self.image, (image_size.width - self.right, 0),
                     (self.size.width - self.right, 0, self.top, self.right))
        texture.blit(self.image, (0, image_size.height - self.bottom),
                     (0, self.size.height - self.bottom, self.left, self.bottom))
        texture.blit(self.image, (image_size.width - self.right, image_size.height - self.bottom),
                     (self.size.height - self.bottom, self.size.width - self.right, self.bottom, self.right))

        # draw the borders by using pygame.transform.smoothscale to create a new image and blitting that

        # 1: make an image of the required size
        # 2: Cout out what you need
        # 3: scale it up to the right size
        # 4: blit to the texture
        middle = Size(self.size.width - (self.left + self.right), self.size.height - (self.top + self.bottom))
        center_size = Size(new_size.width - (self.left + self.right), new_size.height - (self.top + self.bottom))

        left_unscaled = pygame.Surface((middle.width, middle.height), pygame.SRCALPHA)
        left_unscaled.blit(self.image, (0, 0), (0, self.top, middle.width, middle.height))
        left_side = pygame.transform.scale(left_unscaled, (middle.width, center_size.height))
        texture.blit(left_side, (0, self.top))

        right_unscaled = pygame.Surface((middle.width, middle.height), pygame.SRCALPHA)
        right_unscaled.blit(self.image, (0, 0),
                            (self.size.width - middle.width, self.top, middle.width, middle.height))
        right_side = pygame.transform.scale(right_unscaled, (middle.width, center_size.height))
        texture.blit(right_side, (new_size.width - middle.width, self.top))

        # top and bottom
        top_unscaled = pygame.Surface((middle.width, middle.height), pygame.SRCALPHA)
        top_unscaled.blit(self.image, (0, 0), (self.left, 0, middle.width, middle.height))
        top_side = pygame.transform.scale(top_unscaled, (center_size.width, middle.height))
        texture.blit(top_side, (self.left, 0))

        bottom_unscaled = pygame.Surface((middle.width, middle.height), pygame.SRCALPHA)
        bottom_unscaled.blit(self.image, (0, 0),
                             (self.left, self.size.height - 1, middle.width, middle.height))
        bottom_side = pygame.transform.scale(bottom_unscaled, (center_size.width, middle.height))

        texture.blit(bottom_side, (self.left, image_size.height - 1))
        return texture
