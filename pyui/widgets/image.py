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

    def draw(self, new_size=None):
        # images ignore the fill, they are always a fixed size
        self.texture = self.get_texture(self.min_size)
        if self.background is not None:
            self.texture.fill(self.background)
        self.texture.blit(self.image, (self.margin.left, self.margin.top))

    def render(self, surface, pos, available_size=None):
        if self.draw_old_texture(surface, pos, available_size):
            return
        self.draw(available_size)
        surface.blit(self.texture, (pos.x, pos.y))
        render_size = self.min_size
        self.render_rect = pygame.Rect(pos.x, pos.y, render_size.width, render_size.height)
