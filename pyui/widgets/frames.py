import pygame
import pygame.gfxdraw

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
    def __init__(self, background=Color.BACKGROUND, margin=None):
        super().__init__()
        self.image = get_asset('frame.png')
        self.corner = Size(8, 8)
        self.middle = Size(4, 8)
        self.background = background
        self.size = Size(120, 80)

    def render(self, surface, x, y, available_size):
        # draw the top left
        surface.blit(self.image, (x, y), (0, 0, self.corner.width, self.corner.height))
        # top right
        surface.blit(self.image, (x + self.size.width - self.corner.width, y),
                     (self.corner.width + self.middle.width, 0, self.corner.width, self.corner.height))
        # bottom left
        surface.blit(self.image, (x, y + self.size.height - self.corner.height),
                     (0, self.corner.height + self.middle.width, self.corner.width, self.corner.height))
        # bottom right
        surface.blit(self.image, (x + self.size.width - self.corner.width, y + self.size.height - self.corner.height),
                     (self.corner.width + self.middle.width, self.corner.height + self.middle.width, self.corner.height, self.corner.width))

        # draw the borders by using pygame.transform.smoothscale to create a new image and blitting that
        side_width = self.size.width - (2 * self.corner.width)
        side_height = self.size.height - (2 * self.corner.height)
        side_ypos = y + self.corner.height

        left_unscaled = pygame.Surface((self.middle.height, self.middle.width), pygame.SRCALPHA)
        left_unscaled.blit(self.image, (0, 0), (0, self.corner.height, self.middle.height, self.middle.width))
        left_side = pygame.transform.scale(left_unscaled, (self.middle.height, side_height))
        surface.blit(left_side, (x, side_ypos))

        right_unscaled = pygame.Surface((self.middle.height, self.middle.width), pygame.SRCALPHA)
        right_unscaled.blit(self.image, (0, 0),
                            (self.corner.width + self.middle.width, self.corner.height, self.middle.height, self.middle.width))
        right_side = pygame.transform.scale(right_unscaled, (self.middle.height, side_height))
        surface.blit(right_side, (x + self.corner.width + side_width, side_ypos))

        # then top and bottom
        top_unscaled = pygame.Surface((self.middle.width, self.middle.height), pygame.SRCALPHA)
        top_unscaled.blit(self.image, (0, 0), (self.corner.width, 0, self.middle.width, self.middle.height))
        top_side = pygame.transform.scale(top_unscaled, (side_width, self.middle.height))
        surface.blit(top_side, (x + self.corner.width, y))

        bottom_unscaled = pygame.Surface((self.middle.width, self.middle.height), pygame.SRCALPHA)
        bottom_unscaled.blit(self.image, (0, 0), (self.corner.width, self.corner.height + self.middle.width, self.middle.width, self.middle.height))
        bottom_side = pygame.transform.scale(bottom_unscaled, (side_width, self.middle.height))
        surface.blit(bottom_side, (x + self.corner.width, y + self.size.height - self.middle.height))

        # draw the middle
        pygame.draw.rect(surface, Color.BACKGROUND, (x + self.corner.width, y + self.corner.width,
                                                     self.size.width - (2 * self.corner.width),
                                                     self.size.height - (2 * self.corner.height)))
