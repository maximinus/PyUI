import pygame

from pyui.base import Size, Align
from pyui.widget_base import Widget


class TextLabel(Widget):
    def __init__(self, text, font_size=24, color=(255, 255, 255), expand=None, margin=None, align=None):
        super().__init__(expand, margin, align)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.image = self.font.render(text, True, color)
        self.size = Size(self.image.get_width(), self.image.get_height())

    def render(self, surface, x, y, available_size=None):
        if available_size is None:
            available_size = self.min_size
        x += self.margin.left
        y += self.margin.top
        width = available_size.width - self.margin.left - self.margin.right
        height = available_size.height - self.margin.top - self.margin.bottom

        horiz_align = self.align.horizontal()
        if horiz_align == Align.CENTER:
            x += (available_size.width - self.size.width) // 2
        elif horiz_align == Align.RIGHT:
            x += (available_size.width - self.size.width)

        vert_align = self.align.vertical()
        if vert_align == Align.CENTER:
            y += (available_size.height - self.size.height) // 2
        elif vert_align == Align.BOTTOM:
            y += (available_size.height - self.size.height)

        surface.blit(self.image, (x, y))
