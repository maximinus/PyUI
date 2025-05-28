import pygame
from pygame import Surface

from pyui.widget import Widget
from pyui.helpers import Size, Position


class Label(Widget):
    """
    A widget that displays text.
    """
    def __init__(self, text, font, color=(0, 0, 0), **kwargs):
        """
        Initialize a Label widget.
        Args:
            text: The text to display
            font: A Font object
            color: The color of the text
            **kwargs: Additional arguments to pass to Widget
        """
        super().__init__(**kwargs)
        self.text = text
        self.font = font
        self.color = color
        self.update_size()

    def update_size(self):
        """Update the size based on the text content."""
        self.size = self.font.size_of(self.text)

    @property
    def min_size(self) -> Size:
        return self.size + self.margin.size
    
    def set_text(self, new_text):
        """Set new text content and update the size."""
        if self.text == new_text:
            return
        self.text = new_text
        self.update_size()
        # Reset the image cache
        self.image.clear()

    def render(self, destination: Surface, position: Position, size: Size):
        """
        Render the text to the given surface at the specified position.
        """
        if self.image.matches(size):
            destination.blit(self.image.image, position.as_tuple)
            return
        
        new_image = self.get_new_image(size)
        render_pos = self.get_position(size)
        
        # Add the margin left and top
        render_pos.x += self.margin.left
        render_pos.y += self.margin.top
        
        # Render the text
        text_surface = self.font.render(self.text, self.color)
        new_image.blit(text_surface, render_pos.as_tuple)
        
        # Update the image cache
        self.image.update(new_image)
        destination.blit(new_image, position.as_tuple)
