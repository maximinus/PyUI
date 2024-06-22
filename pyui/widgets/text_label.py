import pygame

from pyui.base import Size, Align
from pyui.widget_base import Widget
from pyui.theme import THEME


class TextLabel(Widget):
    def __init__(self, text, style=None, expand=None, margin=None, align=None):
        super().__init__(expand, margin, align)
        self.text = text
        self.style = style
        if style is None:
            self.style = THEME.text['menu']
        self.font = pygame.font.Font(self.style.font, self.style.size)
        self.image = self.font.render(text, True, self.style.color)
        self.size = Size(self.image.get_width(), self.image.get_height())

    def render(self, surface, x, y, available_size=None):
        if available_size is None:
            available_size = self.min_size
        x += self.margin.left
        y += self.margin.top

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
