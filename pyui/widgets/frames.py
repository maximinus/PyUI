import pygame

from pyui.base import get_asset, Color, Size
from pyui.widget_base import Widget


class Frame(Widget):
    # a frame is a container that holds a single widget, and is a fixed size
    def __init__(self, position, size, widget=None):
        super().__init__()
        self.position = position
        self.size = size
        self.widget = widget

    def render(self, surface, x, y, available_size):
        if self.widget is None:
            return
        self.widget.render(surface, x, y, self.size)


class Border(Widget):
    def __init__(self, surface, background=Color.BACKGROUND, margin=None):
        super().__init__()
        self.surface = surface
        self.nine_patch = get_asset('frame.png')
        self.corner = Size(8, 8)
        self.middle = Size(4, 8)

    def render(self, surface, x, y, available_size):
        # draw the top left
        # draw the top right
        # draw the bottom left
        # draw the bottom right

        # Draw the corners
        surface.blit(self.surface, (x, y), (0, 0, left_width, top_height))  # Top-left
        surface.blit(self.surface, (x + width - right_width, y), (self.surface.get_width() - right_width, 0, right_width, top_height))  # Top-right
        surface.blit(self.surface, (x, y + height - bottom_height), (0, self.surface.get_height() - bottom_height, left_width, bottom_height))  # Bottom-left
        surface.blit(self.surface, (x + width - right_width, y + height - bottom_height), (self.surface.get_width() - right_width, self.surface.get_height() - bottom_height, right_width, bottom_height))  # Bottom-right
