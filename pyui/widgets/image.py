import pygame

from pyui.base import Expand, Size, Align
from pyui.widget_base import Widget


class Image(Widget):
    def __init__(self, image, margin=None, expand=None, fill=Expand.NONE, align=Align.CENTER):
        # the image is an already loaded surface
        super().__init__(expand, margin, align)
        self.image = image
        self.size = Size(image.get_width(), image.get_height())
        self.fill = fill

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def render(self, surface, pos, available_size=None):
        surface.blit(self.image, (pos.x + self.margin.left, pos.y + self.margin.top))
        self.render_rect = pygame.Rect(pos.x + self.margin.left, pos.y + self.margin.top,
                                       self.size.width, self.size.height)
