import pygame
from pygame import Color, Surface

from pyui.widget import Widget
from pyui.helpers import Size, Position, Align


class ColorRect(Widget):
    """
    A widget that displays a solid color rectangle.
    """
    def __init__(self, color: Color, size: Size, **kwargs):
        assert "align" not in kwargs, "ColorRect does not support alignment."
        super().__init__(align=Align(Align.FILL, Align.FILL), **kwargs)
        self.size = size
        self.color = color

    @property
    def min_size(self) -> Size:
        return self.size + self.margin.size

    def render(self, mouse, destination: Surface, position: Position, size: Size):
        """
        Render the color rectangle to the given surface at the specified position.
        """
        if self.image.matches(size):
            destination.blit(self.image.image, position.as_tuple)
            return
        new_image = self.get_new_image(size)
        render_pos = self.get_position(size)
        # add the margin left and top
        render_pos.x += self.margin.left
        render_pos.y += self.margin.top
        # draw the rectangle, expand if needed
        # the maximum expansion is the size of the destination minus the margin
        render_width = self.size.width
        if self.expand.horizontal:
            render_width = size.width - self.margin.width
        render_height = self.size.height
        if self.expand.vertical:
            render_height = size.height - self.margin.height
        pygame.draw.rect(new_image,
                         self.color, (0, 0, render_width, render_height))
        self.image.update(new_image)
        destination.blit(new_image, (render_pos + position).as_tuple)
