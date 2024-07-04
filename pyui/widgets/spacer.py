import pygame

from pyui.widget_base import Widget


class Spacer(Widget):
    def __init__(self, size, expand=None):
        # a spacer is a simple widget whose only job is to consume space
        # it has no margin
        super().__init__(expand=expand)
        self.size = size
        # we never draw this widget
        self.redraw = False

    @property
    def min_size(self):
        return self.size

    def draw(self, new_size=None):
        pass

    def render(self, surface, pos, screen_pos, available_size=None):
        self.render_rect = pygame.Rect(screen_pos.x, screen_pos.y, self.size.width, self.size.height)
