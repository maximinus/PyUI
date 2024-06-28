import pygame

from pyui.base import Size, Expand, Align
from pyui.widget_base import Widget


class ColorRect(Widget):
    def __init__(self, size, color, expand=None, margin=None, align=None, fill=Expand.NONE):
        super().__init__(expand, margin, align, fill)
        self.size = size
        self.color = color

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def render(self, surface, pos, available_size=None):
        x = pos.x
        y = pos.y
        if available_size is None:
            available_size = self.min_size
        # only draw to the space we need to
        x += self.margin.left
        y += self.margin.top
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

        pygame.draw.rect(surface, self.color, (x, y, width, height))
        self.render_rect = pygame.Rect(x, y, width, height)
