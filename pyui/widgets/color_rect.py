import pygame

from pyui.base import Size, Expand, Align
from pyui.widget_base import Widget


class ColorRect(Widget):
    def __init__(self, size, color, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.color = color

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def render(self, surface, pos, available_size=None):
        # if we have a texture that currently matches the size, then simply render that
        if self.draw_old_texture(surface, pos, available_size):
            return

        if available_size is None:
            available_size = self.min_size
        self.texture = self.get_texture(Size(available_size.width, available_size.height))

        if self.background is not None:
            self.texture.fill(self.background)

        # only draw to the space we need to
        x = self.margin.left
        y = self.margin.top
        if self.expand.is_horizontal and self.fill.is_horizontal:
            # fill the space
            width = available_size.width - (self.margin.left + self.margin.right)
        else:
            # the size does not include the width, but it will have been calculated in the min size
            width = self.size.width
            width_plus_margin = width + self.margin.left + self.margin.right
            # and align here as well, since we are not filling
            horiz_align = self.align.horizontal()
            if horiz_align == Align.CENTER:
                x += (available_size.width - width_plus_margin) // 2
            elif horiz_align == Align.RIGHT:
                x += (available_size.width - width_plus_margin)
        if self.expand.is_vertical and self.fill.is_vertical:
            height = available_size.height - (self.margin.top - self.margin.bottom)
        else:
            height = self.size.height
            height_plus_margin = height + self.margin.top + self.margin.bottom
            # align here since we are not filling
            vert_align = self.align.vertical()
            if vert_align == Align.CENTER:
                y += (available_size.height - height_plus_margin) // 2
            elif vert_align == Align.BOTTOM:
                y += (available_size.height - height_plus_margin)

        pygame.draw.rect(self.texture, self.color, (x, y, width, height))
        surface.blit(self.texture, (pos.x, pos.y))
        self.render_rect = pygame.Rect(x, y, width, height)
