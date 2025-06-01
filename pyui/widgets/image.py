from pygame import Surface
import pygame

from pyui.widget import Widget
from pyui.helpers import Size, Position


class Image(Widget):
    """
    A widget that displays an image
    """
    def __init__(self, image: Surface, **kwargs):
        super().__init__(**kwargs)
        self.size = Size(image.get_width(), image.get_height())
        self.render_image = image

    @property
    def min_size(self) -> Size:
        return self.size + self.margin.size

    def render(self, mouse, destination: Surface, position: Position, size: Size):
        """
        Render the image to the given surface at the specified position.
        """
        if self.image.matches(size):
            destination.blit(self.image.image, position.as_tuple)
            return
        new_image = self.get_new_image(size)
        render_pos = self.get_position(size)
        # add the margin left and top
        render_pos.x += self.margin.left
        render_pos.y += self.margin.top
        # draw the rectangle
        new_image.blit(self.render_image, render_pos.as_tuple)
        self.image.update(new_image)
        destination.blit(self.image.image, position.as_tuple)
