import pygame

from pyui.base import Size
from pyui.widget_base import Widget


class Spacer(Widget):
    def __init__(self, size, expand=None):
        # a spacer is a simple widget whose only job is to consume space
        # it has no margin
        super().__init__(expand=expand)
        self.size = size
        # we never draw this widget
        self.redraw = False
        self.current_size = Size(0, 0)

    @property
    def min_size(self):
        return self.size

    def draw(self, new_size=None):
        pass

    def render(self, available_size):
        if self.texture is None:
            self.texture = self.get_texture(Size(0, 0))
