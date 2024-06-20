import pygame

from pyui.widget_base import Widget


class Frame(Widget):
    # a frame is a container that holds a single widget, and is a fixed size
    def __init__(self, position, size, widget=None):
        super().__init__()
        self.position = position
        self.size = size
        self.widget = widget

    def render(self, surface, x, y, available_size):
        if self.widget is None:
            return
        self.widget.render(surface, x, y, self.size)


class Border(Widget):
    def __init__(self, surface, margin=None):
        super().__init__()
        self.surface = surface
        self.nine_patch =

    def render(self, surface, x, y, available_size):
        # draw the top left
        # draw the top right
        # draw the bottom left
        # draw the bottom right

        # Draw the corners
        surface.blit(self.surface, (x, y), (0, 0, left_width, top_height))  # Top-left
        surface.blit(self.surface, (x + width - right_width, y), (self.surface.get_width() - right_width, 0, right_width, top_height))  # Top-right
        surface.blit(self.surface, (x, y + height - bottom_height), (0, self.surface.get_height() - bottom_height, left_width, bottom_height))  # Bottom-left
        surface.blit(self.surface, (x + width - right_width, y + height - bottom_height), (self.surface.get_width() - right_width, self.surface.get_height() - bottom_height, right_width, bottom_height))  # Bottom-right

        # Draw the edges
        surface.blit(pygame.transform.scale(self.surface.subsurface((left_width, 0, self.surface.get_width() - left_width - right_width, top_height)), (center_width, top_height)), (x + left_width, y))  # Top
        surface.blit(pygame.transform.scale(self.surface.subsurface((left_width, self.surface.get_height() - bottom_height, self.surface.get_width() - left_width - right_width, bottom_height)), (center_width, bottom_height)), (x + left_width, y + height - bottom_height))  # Bottom
        surface.blit(pygame.transform.scale(self.surface.subsurface((0, top_height, left_width, self.surface.get_height() - top_height - bottom_height)), (left_width, center_height)), (x, y + top_height))  # Left
        surface.blit(pygame.transform.scale(self.surface.subsurface((self.surface.get_width() - right_width, top_height, right_width, self.surface.get_height() - top_height - bottom_height)), (right_width, center_height)), (x + width - right_width, y + top_height))  # Right

        # Draw the center
        surface.blit(pygame.transform.scale(self.surface.subsurface((left_width, top_height, self.surface.get_width() - left_width - right_width, self.surface.get_height() - top_height - bottom_height)), (center_width, center_height)), (x + left_width, y + top_height))
