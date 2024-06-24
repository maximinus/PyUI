import pygame.draw

from pyui.base import Expand, Size, Position
from pyui.widget_base import Widget


class Box(Widget):
    def __init__(self, horizontal=True, margin=None, expand=None, align=None):
        if expand is not None:
            raise AttributeError('Box widgets cannot be passed an expand variable')
        super().__init__(expand, margin, align)
        self.horizontal = horizontal
        self.widgets = []
        self.size = Size(0, 0)

    def add_widget(self, widget):
        self.widgets.append(widget)
        # a box has to account for the child widgets, so we don't use size
        self.size = Size(0, 0)
        for widget in self.widgets:
            self.size += widget.min_size

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

    def handle_event(self, event):
        for widget in self.widgets:
            if widget.handle_event(event):
                return True
        return False


class HBox(Box):
    def __init__(self, margin=None, align=None, widgets=None):
        super().__init__(horizontal=True, margin=margin, align=align)
        if widgets is not None:
            self.widgets = widgets
        else:
            self.widgets = []

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

    def render(self, surface, pos, available_size=None):
        if available_size is None or len(self.widgets) == 0:
            return
        available_size = available_size.subtract_margin(self.margin)
        current_x = pos.x + self.margin.left
        current_y = pos.y + self.margin.top
        all_sizes = self.calculate_sizes(available_size)
        self.render_rect = pygame.Rect(current_x, current_y, sum([x.width for x in all_sizes]), all_sizes[0].height)
        for widget, widget_size in zip(self.widgets, all_sizes):
            widget.render(surface, Position(current_x, current_y), widget_size)
            # no need to add the margin because it is computed in the widget size
            current_x += widget_size.width


class VBox(Box):
    def __init__(self, margin=None, align=None, widgets=None):
        super().__init__(horizontal=False, margin=margin, align=align)
        if widgets is not None:
            self.widgets = widgets
        else:
            self.widgets = []

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

    def render(self, surface, pos, available_size=None):
        if available_size is None or len(self.widgets) == 0:
            return
        available_size = available_size.subtract_margin(self.margin)
        current_x = pos.x + self.margin.left
        current_y = pos.y + self.margin.top
        all_sizes = self.calculate_sizes(available_size)
        self.render_rect = pygame.Rect(current_x, current_y, all_sizes[0].width, sum([x.height for x in all_sizes]))
        for widget, widget_size in zip(self.widgets, all_sizes):
            widget.render(surface, Position(current_x, current_y), widget_size)
            current_y += widget_size.height
