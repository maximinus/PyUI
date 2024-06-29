import pygame

from pyui.base import Expand, Margin, Align, Size, Position
from pyui.events.loop import Callback


# Widget
#  expand:      does the widget ask for as much space as possible, or just the minimum?
#  fill:        whether the widget should expand into any extra space when given it anyway
#  margin:      the size of the margin around the widget
#  min_size:    the smallest size the widget could be, with its margin
#  align:       if there is more size than the min size, and we are not filling, where should we align the widget?
#  render_rect: the rectangular area of the last blit we made to draw the widget
#  parent:      the parent widget, or None if the root
# callbacks:    array of [event, callback] ro capture events
# children:     returns an array of all children (no children - an empty array)

class Widget:
    def __init__(self, expand=None, margin=None, align=None, fill=None):
        self.expand = expand if expand is not None else Expand.NONE
        self.margin = margin if margin is not None else Margin()
        self.align = Align(align) if align is not None else Align(Align.CENTER)
        self.fill = fill if fill is not None else Expand.NONE
        self.render_rect = None
        self.parent = None
        self.callbacks = []

    @property
    def min_size(self):
        # this needs to be overridden by the subclass
        return Size(0, 0)

    @property
    def children(self):
        return []

    def render(self, surface, pos, available_size=None):
        # if the available size is None, then the default is to render at the minimum size
        self.render_rect = pygame.Rect(pos.x, pos.y, 0, 0)

    def update(self, surface):
        # try and draw yourself based on the previous render_rect
        if self.render_rect is None:
            return
        self.render(surface, Position(self.render_rect.x, self.render_rect.y),
                    Size(self.render_rect.width, self.render_rect.height))

    def get_root(self):
        if self.parent is None:
            return self
        return self.parent.get_root()

    def connect(self, event_type, callback):
        self.callbacks.append(Callback(callback, event_type, self))
