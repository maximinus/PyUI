import pygame
from pyui.widget_base import Widget


class NinePatch(Widget):
    def __init__(self, surface, left, right, top, bottom, expand=None, margin=None, align=None):
        super().__init__(expand, margin, align)
        self.surface = surface
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom

    def render(self, surface, x, y, available_size):
        x += self.margin.left
        y += self.margin.top
        width = available_size.width - self.margin.left - self.margin.right
        height = available_size.height - self.margin.top - self.margin.bottom

        left_width = self.left
        right_width = self.right
        top_height = self.top
        bottom_height = self.bottom
        center_width = width - left_width - right_width
        center_height = height - top_height - bottom_height

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
