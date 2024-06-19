import pygame
from pyui.base import Expand, Margin, Align, Size


class Widget:
    def __init__(self, expand=Expand.NONE, margin=None, align=None):
        self.expand = expand
        self.margin = margin if margin is not None else Margin()
        self.align = align if align is not None else Align()
        self.size = Size(0, 0)

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def render(self, surface, x, y, available_size):
        pass


class ColorRect(Widget):
    def __init__(self, size, color, expand=Expand.NONE, margin=None, align=None):
        super().__init__(expand, margin, align)
        self.size = size
        self.color = color

    def render(self, surface, x, y, available_size):
        size = self.min_size
        # only draw to the space we need to
        x += self.margin.left
        y += self.margin.top
        width = size.width - self.margin.left - self.margin.right
        height = size.height - self.margin.top - self.margin.bottom

        if self.expand in [Expand.HORIZONTAL, Expand.BOTH]:
            if self.align.horizontal == Align.CENTER:
                x += (available_size.width - width) // 2
            elif self.align.horizontal == Align.END:
                x += (available_size.width - width)

        if self.expand in [Expand.VERTICAL, Expand.BOTH]:
            if self.align.vertical == Align.CENTER:
                y += (available_size.height - height) // 2
            elif self.align.vertical == Align.END:
                y += (available_size.height - height)

        pygame.draw.rect(surface, self.color, (x, y, width, height))


class Box(Widget):
    def __init__(self, horizontal=True, margin=None, expand=Expand.NONE, align=None):
        super().__init__(expand, margin, align)
        self.horizontal = horizontal
        self.widgets = []

    def add_widget(self, widget):
        self.widgets.append(widget)

    @property
    def expand(self):
        # whether a box will expand or not depends on it's children
        x_expand = False
        y_expand = False
        for widget in self.widgets:
            if widget.expand != Expand.NONE:
                if widget.expand == Expand.BOTH:
                    return Expand.BOTH
            if widget.expand == Expand.HORIZONTAL:
                x_expand = True
            if widget.expand == Expand.VERTICAL:
                y_expand = True
            if x_expand and y_expand:
                return Expand.BOTH
        if x_expand:
            return Expand.HORIZONTAL
        if y_expand:
            return Expand.VERTICAL
        return Expand.NONE

    @expand.setter
    def expand(self, new_value):
        # cannot set this value in a Box
        pass


class HBox(Box):
    def __init__(self, margin=None, expand=Expand.NONE, align=None, widgets=None):
        super().__init__(horizontal=True, margin=margin, expand=expand, align=align)
        if widgets is not None:
            self.widgets = widgets

    @property
    def min_size(self):
        # go through the size
        base_size = Size(0, 0)
        for child in self.widgets:
            child_size = child.min_size
            base_size.width += child_size.width
            base_size.height = max(base_size.height, child_size.height)
        return base_size.add_margin(self.margin)

    def calculate_sizes(self, available_size):
        available_size = available_size.subtract_margin(self.margin)
        fixed_width = 0
        expandable_count = 0

        # Calculate the total fixed width and count expandable widgets
        for widget in self.widgets:
            if widget.expand.is_horizontal:
                expandable_count += 1
            fixed_width += widget.min_size.width

        # Calculate remaining width to be distributed among expandable widgets
        remaining_width = available_size.width - fixed_width

        # Handle cases where remaining width is less than zero
        if remaining_width < 0:
            remaining_width = 0

        # Calculate individual width for expandable widgets
        if expandable_count > 0:
            expand_width = remaining_width // expandable_count
            extra_width = remaining_width % expandable_count
        else:
            expand_width = 0
            extra_width = 0

        # Set final widths
        final_widths = []
        for widget in self.widgets:
            # calculate height, is easy
            height = widget.min_size.height
            if widget.expand.is_vertical:
                height = available_size.height
            if widget.expand.is_horizontal:
                # Distribute the remaining extra width one by one to ensure total width matches N
                if extra_width > 0:
                    final_widths.append(Size(widget.min_size.width + expand_width + 1, height))
                    extra_width -= 1
                else:
                    final_widths.append(Size(widget.min_size.width + expand_width, height))
            else:
                final_widths.append(Size(widget.min_size.width, height))
        return final_widths

    def render(self, surface, x, y, available_size):
        available_size = available_size.subtract_margin(self.margin)
        current_x = x + self.margin.left
        for widget, widget_size in zip(self.widgets, self.calculate_sizes(available_size)):
            widget.render(surface, current_x, y, widget_size)
            current_x += widget_size.width + widget.margin.left + widget.margin.right


class VBox(Box):
    def __init__(self, margin=None, expand=Expand.NONE, align=None, widgets=None):
        super().__init__(horizontal=False, margin=margin, expand=expand, align=align)
        if widgets is not None:
            self.widgets = widgets

    @property
    def min_size(self):
        # go through the size
        base_size = Size(0, 0)
        for child in self.widgets:
            child_size = child.min_size
            base_size.width = max(base_size.width, child_size.width)
            base_size.height += child_size.height
        return base_size

    def calculate_sizes(self, available_size):
        fixed_height = 0
        expandable_count = 0

        # Calculate the total fixed width and count expandable widgets
        for widget in self.widgets:
            if widget.expand.is_vertical:
                expandable_count += 1
            fixed_height += widget.min_size.height

        # Calculate remaining height to be distributed among expandable widgets
        remaining_height = available_size.height - fixed_height

        # Handle cases where remaining width is less than zero
        if remaining_height < 0:
            remaining_height = 0

        # Calculate individual width for expandable widgets
        if expandable_count > 0:
            expand_height = remaining_height // expandable_count
            extra_height = remaining_height % expandable_count
        else:
            expand_height = 0
            extra_height = 0

        # Set final widths
        final_heights = []
        for widget in self.widgets:
            # calculate width, is easy
            width = widget.min_size.width
            if widget.expand.is_horizontal:
                width = available_size.width
            if widget.expand.is_vertical:
                # Distribute the remaining extra width one by one to ensure total width matches N
                if extra_height > 0:
                    final_heights.append(Size(width, widget.min_size.height + expand_height + 1))
                    extra_height -= 1
                else:
                    final_heights.append(Size(width, widget.min_size.height + expand_height))
            else:
                final_heights.append(Size(width, widget.min_size.height))
        return final_heights

    def render(self, surface, x, y, available_size):
        available_size = available_size.subtract_margin(self.margin)
        current_y = y + self.margin.top
        for widget, widget_size in zip(self.widgets, self.calculate_sizes(available_size)):
            widget.render(surface, x, current_y, widget_size)
            current_y += widget_size.height + widget.margin.top + widget.margin.bottom


class NinePatch(Widget):
    def __init__(self, surface, left, right, top, bottom, expand=Expand.NONE, margin=None, align=None):
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


class TextLabel(Widget):
    def __init__(self, text, font_size=24, color=(255, 255, 255), expand=Expand.NONE, margin=None, align=None):
        super().__init__(expand, margin, align)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.font = pygame.font.Font(None, font_size)
        self.image = self.font.render(text, True, color)
        self.size = Size(self.image.get_width(), self.image.get_height())

    def render(self, surface, x, y, available_size):
        x += self.margin.left
        y += self.margin.top
        width = available_size.width - self.margin.left - self.margin.right
        height = available_size.height - self.margin.top - self.margin.bottom

        if self.align.horizontal == Align.CENTER:
            x += (available_size.width - self.size.width) // 2
        elif self.align.horizontal == Align.END:
            x += (available_size.width - self.size.width)

        if self.align.vertical == Align.CENTER:
            y += (available_size.height - self.size.height) // 2
        elif self.align.vertical == Align.END:
            y += (available_size.height - self.size.height)

        surface.blit(self.image, (x, y))
