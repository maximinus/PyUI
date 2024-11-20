import pygame

from pyui.base import Expand, Align, Size, Position
from pyui.events.loop import Callback, set_dirty


# Widget
# expand:       does the widget ask for as much space as possible, or just the minimum?
# min_size:    the smallest size the widget could be, with its margin
# align:       if there is more size than the min size, and we are not filling, where should we align the widget?
# parent:      the parent widget, or None if the root
# callbacks:    array of [event, callback] capture events
# children:     returns an array of all children (no children - an empty array)
# texture:      the texture drawn. Includes the margin
# background:   a color that covers the whole of the rear of the image
# container:    A property that is True if this widget is a container for other widgets
# current_size: The Size of the widget on last draw, or Size(-1, -1) with no texture
# widget_area:  The rect of the drawn widget, excluding margins
#               Used when updating the image oe testing mouse checks

# some functions:
# render:       draw yourself
# mouse_hit     is the given position over this widget?
# set_dirty     tell the main loop to re-render this widget

class Widget:
    def __init__(self, expand=None, align=None, background=None):
        self.expand = expand if expand is not None else Expand.NONE
        self.align = Align(align) if align is not None else Align(Align.CENTER)
        self.parent = None
        self.callbacks = []
        self.texture = None
        self.background = background
        self.current_size = Size(-1, -1)
        self.frame_offset = Position(0, 0)
        self.widget_area = None

    @property
    def min_size(self):
        # this needs to be overridden by the subclass
        return Size(0, 0)

    @property
    def container(self):
        return False

    def mouse_hit(self, mouse_pos):
        if self.widget_area is None:
            return False
        return self.widget_area.collidepoint((mouse_pos.x, mouse_pos.y))

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

    def set_dirty(self):
        set_dirty(self)

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
