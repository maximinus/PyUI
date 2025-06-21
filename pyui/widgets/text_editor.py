import pygame

from pyui.widget import Widget
from pyui.helpers import Position, Margin, Size
from pyui.assets import get_font
from pyui.text import TextStore

# milliseconds
CURSOR_BLINK_RATE = 500


def get_font_size(font):
    font_size = Size(0, font.get_linesize())


class TextEditor(Widget):
    def __init__(self, background=(250, 245, 245),
                 margin=Margin(4, 4, 4, 4), **kwargs):
        super().__init__(background=background, margin=margin, **kwargs)
        self.text = TextStore()
        self.cursor_position = Position(self.margin.left, self.margin.top)
        self.cursor_size = Size(20, 20)
        self.font = get_font('creato.otf', 16)
    
    def render_cursor(self, destination, position):
        # on or off?
        time = pygame.time.get_ticks() // CURSOR_BLINK_RATE
        if time % 2 == 0:
            # don't draw the cursor
            return
        
        start_x = position.x + self.cursor_position.x
        start_y = position.y + self.cursor_position.y
        pygame.draw.line(destination, (0, 0, 0),
                         (start_x, start_y),
                         (start_x, start_y + self.cursor_size.height))

    def render(self, mouse, destination, position, size):
        if self.image.matches(size):
            destination.blit(self.image.image, position.as_tuple)
            self.render_cursor(destination, position)
            return
        
        new_image = self.get_new_image(size)
        new_image.fill(self.background)
        destination.blit(new_image, position.as_tuple)
        self.render_cursor(destination, position)
        self.image.update(new_image)
