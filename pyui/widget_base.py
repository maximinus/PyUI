import pygame

from pyui.base import Expand, Margin, Align, Size, Position


# a widget always has:
# a min_size: the smallest this widget can be
# a render_rect; the area where the widget was drawn to (this does not include the margin)
# a boolean "redraw" which lets us know the widget needs to be redrawn

class Widget:
    def __init__(self, expand=None, margin=None, align=None):
        self.expand = expand if expand is not None else Expand.NONE
        self.margin = margin if margin is not None else Margin()
        self.align = Align(align) if align is not None else Align(Align.CENTER)
        self.render_rect = None
        self.redraw = True

    @property
    def min_size(self):
        # this needs to be overridden by the subclass
        return Size(0, 0)

    def render(self, surface, pos, available_size=None):
        # if the available size is None, then the default is to render at the minimum size
        self.render_rect = pygame.Rect(pos.x, pos.y, 0, 0)

    def handle_event(self, event):
        # return true to indicate event has been processed
        return False
