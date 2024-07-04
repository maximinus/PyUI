import pygame.draw

from pyui.base import Expand, Size, Position
from pyui.widget_base import Widget

# Containers: Widgets that hold other widgets
#   A Box container sorts widgets horizontally or vertically
#   Containers have no defined size, but they have a minimum size
#   Frames are like containers but only hold 1 widget, and have a defined size
#   a widget has a min_size, but rarely has a size


class Box(Widget):
    def __init__(self, widgets=None, horizontal=True, margin=None, expand=None, align=None, fill=None, background=None):
        super().__init__(expand, margin, align, fill)
        self.background = background
        self.horizontal = horizontal
        if widgets is not None:
            for widget in widgets:
                widget.parent = self
            self.widgets = widgets
        else:
            self.widgets = []
        self.size = Size(0, 0)

    def add_widget(self, widget):
        widget.parent = self
        self.widgets.append(widget)
        # a box has to account for the child widgets
        self.size = Size(0, 0)
        for widget in self.widgets:
            self.size += widget.min_size

    @property
    def container(self):
        return True

    @property
    def children(self):
        return self.widgets

    @property
    def expand(self):
        # whether a box will expand or not depends on its children
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
        pass

    def handle_event(self, event):
        for widget in self.widgets:
            if widget.handle_event(event):
                return True
        return False

    def fill_render_rect(self, available_size):
        if self.fill.is_horizontal:
            self.render_rect.width = available_size.width
        if self.fill.is_vertical:
            self.render_rect.height = available_size.height

    def draw_background(self, available_size, surface):
        if self.background is not None:
            # if Expand is set to horizontal or vertical, fill the background
            background_rect = self.render_rect.copy()
            if self.fill.is_horizontal:
                background_rect.width = available_size.width
            if self.fill.is_vertical:
                background_rect.height = available_size.height
            pygame.draw.rect(surface, self.background, self.render_rect)


class HBox(Box):
    def __init__(self, widgets=None, background=None, **kwargs):
        super().__init__(horizontal=True, widgets=widgets, background=background, **kwargs)

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
        # note: the height for each widget should be the same as highest widget, else the widget cannot center
        height = 0
        if len(self.widgets) > 0:
            height = max([x.min_size.height for x in self.widgets])
        for widget in self.widgets:
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

    def draw_container(self, screen_pos, new_size=None):
        new_size = self.get_ideal_draw_size(new_size)
        self.texture = self.get_texture(new_size)
        if self.background is not None:
            self.texture.fill(self.background)

        # no need to do anything else if there are no widgets
        if len(self.widgets) == 0:
            return

        total_size = new_size.subtract_margin(self.margin)
        x = self.margin.left
        y = self.margin.top
        all_sizes = self.calculate_sizes(total_size)

        for widget, widget_size in zip(self.widgets, all_sizes):
            # this needs the screen position added, we must do it now because this could another Box
            widget.render(self.texture, Position(x, y), screen_pos + Position(x, y), widget_size)
            # no need to add the margin because it is computed in the widget size
            x += widget_size.width

    def render(self, surface, pos, screen_pos, available_size=None):
        if self.draw_old_texture(surface, pos, available_size):
            return

        self.draw_container(screen_pos, available_size)
        surface.blit(self.texture, (pos.x, pos.y))
        self.render_rect = pygame.Rect(screen_pos.x, screen_pos.y, self.texture.get_width(), self.texture.get_height())


class VBox(Box):
    def __init__(self, widgets=None, background=None, **kwargs):
        super().__init__(horizontal=False, widgets=widgets, background=background, **kwargs)

    @property
    def min_size(self):
        # go through the size
        base_size = Size(0, 0)
        for child in self.widgets:
            child_size = child.min_size
            base_size.width = max(base_size.width, child_size.width)
            base_size.height += child_size.height
        return base_size.add_margin(self.margin)

    def calculate_sizes(self, available_size=None):
        if available_size is None:
            available_size = self.min_size
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

        # Set final values
        final_heights = []
        width = 0
        if len(self.widgets) > 0:
            width = max([x.min_size.width for x in self.widgets])
        for widget in self.widgets:
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

    def draw_container(self, screen_pos, new_size=None):
        new_size = self.get_ideal_draw_size(new_size)
        self.texture = self.get_texture(new_size)
        if self.background is not None:
            self.texture.fill(self.background)

        if len(self.widgets) == 0:
            return

        total_size = new_size.subtract_margin(self.margin)
        x = self.margin.left
        y = self.margin.top
        all_sizes = self.calculate_sizes(total_size)

        for widget, widget_size in zip(self.widgets, all_sizes):
            widget.render(self.texture, Position(x, y), screen_pos + Position(x, y), widget_size)
            # no need to add the margin because it is computed in the widget size
            y += widget_size.height

    def render(self, surface, pos, screen_pos, available_size=None):
        if self.draw_old_texture(surface, pos, available_size):
            return

        self.draw_container(screen_pos, available_size)
        surface.blit(self.texture, (pos.x, pos.y))
        self.render_rect = pygame.Rect(screen_pos.x, screen_pos.y, self.texture.get_width(), self.texture.get_height())