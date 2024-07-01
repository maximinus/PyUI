import pygame

from pyui.base import Size, Align
from pyui.widget_base import Widget
from pyui.theme import THEME


class TextLabel(Widget):
    def __init__(self, text, style=None, background=None, expand=None, margin=None, align=None, fill=None):
        super().__init__(expand, margin, align, fill)
        self.text = text
        self.style = style
        self.background = background
        if style is None:
            self.style = THEME.text['menu']
        self.font = pygame.font.Font(self.style.font, self.style.size)
        self.image = self.font.render(text, True, self.style.color)
        self.size = Size(self.image.get_width(), self.image.get_height())

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def render(self, surface, pos, available_size=None):
        # text labels ignore "fill" as they cannot naturally expand
        x = pos.x
        y = pos.y
        if available_size is None:
            available_size = self.min_size

        if self.background is not None:
            pygame.draw.rect(surface, self.background, pygame.Rect(x, y, available_size.width, available_size.height))

        x += self.margin.left
        y += self.margin.top

        horiz_align = self.align.horizontal()
        full_size = self.min_size
        if horiz_align == Align.CENTER:
            x += (available_size.width - full_size.width) // 2
        elif horiz_align == Align.RIGHT:
            x += (available_size.width - full_size.width)

        vert_align = self.align.vertical()
        if vert_align == Align.CENTER:
            y += (available_size.height - full_size.height) // 2
        elif vert_align == Align.BOTTOM:
            y += (available_size.height - full_size.height)

        surface.blit(self.image, (x, y))
        self.render_rect = pygame.Rect(pos.x, pos.y, full_size.width, full_size.height)
