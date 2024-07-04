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
#               This area should be: (screen_x, screen_y, width, height)
#  parent:      the parent widget, or None if the root
# callbacks:    array of [event, callback] ro capture events
# children:     returns an array of all children (no children - an empty array)
# texture:      the texture drawn. Includes the margin
# background:   a color that covers the whole of the rear of the image
# container:    A property that is True if this widget is a container for other widgets

# some functions:
# render:       draw yourself to this new place

class Widget:
    def __init__(self, expand=None, margin=None, align=None, fill=None, background=None):
        self.expand = expand if expand is not None else Expand.NONE
        self.margin = margin if margin is not None else Margin()
        self.align = Align(align) if align is not None else Align(Align.CENTER)
        self.fill = fill if fill is not None else Expand.NONE
        self.render_rect = None
        self.parent = None
        self.callbacks = []
        self.texture = None
        self.background = background

    @property
    def min_size(self):
        # this needs to be overridden by the subclass
        return Size(0, 0)

    @property
    def children(self):
        return []

    @property
    def container(self):
        return False

    def render(self, surface, pos, screen_pos, available_size=None):
        # if the available size is None, then the default is to render at the minimum size
        # in normal use, the position is relative to the parent widget
        # this can be obtained with self.parent.render_rect.x|y
        self.render_rect = pygame.Rect(pos.x, pos.y, 0, 0)

    def get_ideal_draw_size(self, new_size):
        # calculate the size of the widget, either on the given size, or the last render, or the min size
        if new_size is None:
            if self.render_rect is None:
                new_size = self.min_size
            else:
                new_size = Size(self.render_rect.width, self.render_rect.height)
        else:
            ideal_size = self.min_size
            if self.fill.is_horizontal or self.expand.is_horizontal:
                ideal_size.width = new_size.width
            if self.fill.is_vertical or self.expand.is_vertical:
                ideal_size.height = new_size.height
            new_size = ideal_size
        return new_size

    def draw(self, new_size=None):
        # draw image based on previous render_rect, or on size given
        pass

    def update(self, surface):
        # try and draw yourself based on the previous render_rect
        if self.render_rect is None:
            return
        root_widget = self.get_root()
        # we need to grab the base texture and draw on that
        self.render(root_widget.texture, Position(self.render_rect.x, self.render_rect.y),
                    Size(self.render_rect.width, self.render_rect.height))
        # return the area of the screen that needs updating
        dirty_area = self.render_rect.copy()
        # adjust for the position of the widget
        dirty_area.x += root_widget.position.x
        dirty_area.y += root_widget.position.y
        return dirty_area

    def update_dirty_rect(self, dirty_rect):
        # either it's in this widget or not
        if not self.render_rect.colliderect(dirty_rect):
            # nothing to do with us
            return
        overlap_area = self.render_rect.clip(dirty_rect)
        # so now we check with all of our children:
        for child in self.children:
            # if this widget has children, then it should render its own children
            # Note: The various overlap areas will be the overlap on the SCREEN; however, we need to copy from
            # the WIDGET. To do this, modify the final overlap by the widgets render_rect x and y positions??
            if child.container:
                child.update_dirty_rect(overlap_area)
                self.texture.blit(child.texture, (overlap_area.x, overlap_area.y), overlap_area)
            elif child.render_rect.colliderect(overlap_area):
                child_overlap = child.render_rect.clip(overlap_area)
                self.texture.blit(child.texture, (child_overlap.x, child_overlap.y), child_overlap)

    def get_texture(self, size):
        new_surface = pygame.Surface((size.width, size.height), pygame.SRCALPHA)
        return new_surface

    def draw_old_texture(self, surface, pos, available_size):
        # blit to the parent widget if nothing has changed
        if available_size is None:
            return False
        if self.texture is not None:
            if available_size.width == self.texture.get_width() and available_size.height == self.texture.get_height():
                surface.blit(self.texture, (pos.x, pos.y))
                return True
        return False

    def get_root(self):
        if self.parent is None:
            return self
        return self.parent.get_root()

    def connect(self, event_type, callback, data=None):
        self.callbacks.append(Callback(callback, event_type, self, data))
