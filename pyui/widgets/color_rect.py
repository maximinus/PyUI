import pygame

from pyui.base import Size, Expand, Align
from pyui.widget_base import Widget


class ColorRect(Widget):
    def __init__(self, size, color, expand=None, margin=None, align=None, fill=Expand.NONE):
        super().__init__(expand, margin, align)
        self.size = size
        self.color = color
        # fill means "fill the expanded area (if there is any) with the expanded rect"
        # otherwise the widget will expand but be the same size (which is the norm)
        self.fill = fill

    def render(self, surface, x, y, available_size):
        render_size = Size(0, 0)
        # only draw to the space we need to
        x += self.margin.left
        y += self.margin.top
        if self.expand.is_horizontal and self.fill.is_horizontal:
            # fill the space
            width = available_size.width - (self.margin.left + self.margin.right)
        else:
            width = self.size.width - (self.margin.left + self.margin.right)
            # and align here as well, since we are not filling
            horiz_align = self.align.horizontal()
            if horiz_align == Align.CENTER:
                x += (available_size.width - width) // 2
            elif horiz_align == Align.RIGHT:
                x += (available_size.width - width)
        if self.expand.is_vertical and self.fill.is_vertical:
            height = available_size.height - (self.margin.top - self.margin.bottom)
        else:
            height = self.size.height - (self.margin.top - self.margin.bottom)
            # align here since we are not filling
            vert_align = self.align.vertical()
            if vert_align == Align.CENTER:
                y += (available_size.height - height) // 2
            elif vert_align == Align.BOTTOM:
                y += (available_size.height - height)

        pygame.draw.rect(surface, self.color, (x, y, width, height))
