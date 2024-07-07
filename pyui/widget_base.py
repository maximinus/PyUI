import pygame

from pyui.base import Expand, Margin, Align, Size, Position
from pyui.events.loop import Callback


# Widget
# expand:       does the widget ask for as much space as possible, or just the minimum?
# margin:      the size of the margin around the widget
# min_size:    the smallest size the widget could be, with its margin
# align:       if there is more size than the min size, and we are not filling, where should we align the widget?
# parent:      the parent widget, or None if the root
# callbacks:    array of [event, callback] capture events
# children:     returns an array of all children (no children - an empty array)
# texture:      the texture drawn. Includes the margin
# background:   a color that covers the whole of the rear of the image
# container:    A property that is True if this widget is a container for other widgets
# current_size: The Size of the widget on last draw, or Size(-1, -1) with no texture

# some functions:
# render:       draw yourself

class Widget:
    def __init__(self, expand=None, margin=None, align=None, background=None):
        self.expand = expand if expand is not None else Expand.NONE
        self.margin = margin if margin is not None else Margin()
        self.align = Align(align) if align is not None else Align(Align.CENTER)
        self.parent = None
        self.callbacks = []
        self.texture = None
        self.background = background
        self.current_size = Size(-1, -1)
        self.frame_offset = Position(0, 0)
        self.mouse_rect = None

    @property
    def min_size(self):
        # this needs to be overridden by the subclass
        return Size(0, 0)

    @property
    def container(self):
        return False

    def render(self, available_size, offset=Position(0, 0)):
        if available_size == self.current_size:
            return
        self.frame_offset = offset
        self.draw(available_size)

    def draw(self, new_size):
        # draw image based on previous render_rect, or on size given
        self.texture = self.get_texture(new_size)
        if self.background is not None:
            self.texture.fill(self.background)
        self.current_size = new_size

    def get_texture(self, size):
        new_surface = pygame.Surface((size.width, size.height), pygame.SRCALPHA)
        self.current_size = size
        return new_surface

    def get_root(self):
        if self.parent is None:
            return self
        return self.parent.get_root()

    def connect(self, event_type, callback, data=None):
        self.callbacks.append(Callback(callback, event_type, self, data))

    def get_align_offset(self, widget_size, given_size):
        # if the given size is larger, work out where to place the widget based on the alignment
        offset = Position(0, 0)
        horizontal_space = given_size.width - widget_size.width
        if horizontal_space > 0:
            horiz_align = self.align.horizontal()
            if horiz_align == Align.CENTER:
                offset.x += horizontal_space // 2
            elif horiz_align == Align.RIGHT:
                offset.x += horizontal_space
        vertical_space = given_size.height - widget_size.height
        if vertical_space > 0:
            vert_align = self.align.vertical()
            if vert_align == Align.CENTER:
                offset.y += vertical_space // 2
            elif vert_align == Align.BOTTOM:
                offset.y += vertical_space
        return offset
