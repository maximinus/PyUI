import pygame

from pyui.base import Size, Expand, Align, Position
from pyui.widget_base import Widget


class ColorRect(Widget):
    # ColorRects are primarily a testing widget
    # If ColorRects expand, then they fill the space with the colored rect

    def __init__(self, size, color, **kwargs):
        super().__init__(**kwargs)
        self.size = size
        self.color = color

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def draw(self, new_size):
        self.current_size = new_size
        self.texture = self.get_texture(self.current_size)
        if self.background is not None:
            self.texture.fill(self.background)

        # only draw to the space we need to
        draw_pos = Position(self.margin.left, self.margin.top)
        if self.expand.is_horizontal:
            # fill the space
            width = new_size.width - (self.margin.left + self.margin.right)
        else:
            # the size does not include the width, but it will have been calculated in the min size
            width = self.size.width

        if self.expand.is_vertical:
            height = new_size.height - (self.margin.top + self.margin.bottom)
        else:
            height = self.size.height

        offset = self.get_align_offset(Size(width, height), new_size.subtract_margin(self.margin))
        draw_pos += offset
        pygame.draw.rect(self.texture, self.color, (draw_pos.x, draw_pos.y, width, height))
