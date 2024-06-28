import pygame
import pygame.gfxdraw

from pyui.theme import THEME
from pyui.base import get_asset, Size, Position
from pyui.widget_base import Widget


# these items have a size, which is the size of the area to render other widgets
# TODO: these widgets must have their own surface, which the child widgets render to
# this means that the positions for rendering must be realtive to the parent widget
# this makes dirty rect drawing a lot easier

class Frame(Widget):
    # a frame is a container that holds a single widget, and is a fixed size
    # the size does NOT include the margin
    # a frame always needs a position
    def __init__(self, pos, modal=False, size=None, widget=None, margin=None):
        super().__init__(margin=margin)
        self.position = pos
        self.modal = modal
        if size is None:
            # infer the size from the widget
            if widget is None:
                self.size = Size(0, 0)
            else:
                self.size = widget.min_size
                widget.parent = self
        else:
            self.size = size
        self.widget = widget
        # null container, is parent
        self.container = None

    @property
    def children(self):
        return [self.widget]

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def render(self, surface, _, available_size=None):
        if self.widget is None:
            return
        self.widget.render(surface, self.position, self.size)
        self.render_rect = self.widget.render_rect

    def draw(self, surface):
        self.render(surface, self.position, available_size=self.size)


class Border(Widget):
    def __init__(self, pos, modal=False, background=None, widget=None):
        # the border contains another widget, however the default will be to grab the default size of the widget
        # there is a resize method if you want to change this
        # the actual size of the Border will be the child widget min size + border size
        # the border size will depend on the size of the nine-patch
        # the widget render will occur at the corner of the child widget
        # any margin will be ignored
        super().__init__()
        self.position = pos
        self.modal = modal
        self.image = get_asset('nine_patch/frame.png')
        self.corner = Size(8, 8)
        self.middle = Size(4, 8)
        if background is None:
            background = THEME.color['widget_background']
        self.background = background
        self.widget = widget
        if widget is None:
            self.size = Size(0, 0)
        else:
            self.size = widget.min_size
            self.widget.parent = self
        self.parent = None

    @property
    def children(self):
        return [self.widget]

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def update_widget(self, widget):
        self.widget = widget
        self.size = widget.min_size()

    def update_size(self, new_size):
        self.size = new_size

    def render(self, surface, _, available_size=None):
        # draw the top left
        x = self.position.x - self.corner.width
        y = self.position.y - self.corner.height

        # the size of the area the widgets need
        render_size = self.min_size

        surface.blit(self.image, (x, y), (0, 0, self.corner.width, self.corner.height))
        # top right
        surface.blit(self.image, (x + render_size.width + self.corner.width, y),
                     (self.corner.width + self.middle.width, 0, self.corner.width, self.corner.height))
        # bottom left
        surface.blit(self.image, (x, y + self.corner.height + render_size.height),
                     (0, self.corner.height + self.middle.width, self.corner.width, self.corner.height))
        # bottom right
        surface.blit(self.image, (x + render_size.width + self.corner.width, y + self.corner.height + render_size.height),
                     (self.corner.width + self.middle.width, self.corner.height + self.middle.width, self.corner.height, self.corner.width))

        # draw the borders by using pygame.transform.smoothscale to create a new image and blitting that
        side_ypos = y + self.corner.height

        left_unscaled = pygame.Surface((self.middle.height, self.middle.width), pygame.SRCALPHA)
        left_unscaled.blit(self.image, (0, 0), (0, self.corner.height, self.middle.height, self.middle.width))
        left_side = pygame.transform.scale(left_unscaled, (self.middle.height, render_size.height))
        surface.blit(left_side, (x, side_ypos))

        right_unscaled = pygame.Surface((self.middle.height, self.middle.width), pygame.SRCALPHA)
        right_unscaled.blit(self.image, (0, 0),
                            (self.corner.width + self.middle.width, self.corner.height, self.middle.height, self.middle.width))
        right_side = pygame.transform.scale(right_unscaled, (self.middle.height, render_size.height))
        surface.blit(right_side, (x + self.corner.width + render_size.width, side_ypos))

        # then top and bottom
        top_unscaled = pygame.Surface((self.middle.width, self.middle.height), pygame.SRCALPHA)
        top_unscaled.blit(self.image, (0, 0), (self.corner.width, 0, self.middle.width, self.middle.height))
        top_side = pygame.transform.scale(top_unscaled, (render_size.width, self.middle.height))
        surface.blit(top_side, (x + self.corner.width, y))

        bottom_unscaled = pygame.Surface((self.middle.width, self.middle.height), pygame.SRCALPHA)
        bottom_unscaled.blit(self.image, (0, 0), (self.corner.width, self.corner.height + self.middle.width, self.middle.width, self.middle.height))
        bottom_side = pygame.transform.scale(bottom_unscaled, (render_size.width, self.middle.height))
        surface.blit(bottom_side, (x + self.corner.width, y + self.corner.height + render_size.height))

        # draw the middle
        x += self.corner.width
        y += self.corner.height
        pygame.draw.rect(surface, self.background, (x, y, render_size.width, render_size.height))
        self.widget.render(surface, Position(x, y), render_size)
        self.render_rect = pygame.Rect(x, y, render_size.width, render_size.height)
