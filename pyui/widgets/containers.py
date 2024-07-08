import pygame.draw

from pyui.base import Expand, Size, Position
from pyui.widget_base import Widget

# Containers: Widgets that hold other widgets
#   A Box container sorts widgets horizontally or vertically
#   Containers have no defined size, but they have a minimum size
#   Frames are like containers but only hold 1 widget, and have a defined size
#   a widget has a min_size, but rarely has a size


class Box(Widget):
    def __init__(self, widgets=None, horizontal=True, margin=None, expand=None, align=None, background=None):
        super().__init__(expand, margin, align)
        self.background = background
        self.horizontal = horizontal
        if widgets is not None:
            for widget in widgets:
                widget.parent = self
            self.widgets = widgets
        else:
            self.widgets = []

    def add_widget(self, widget):
        widget.parent = self
        self.widgets.append(widget)

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

    def draw(self, new_size):
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

        # at this point we have our own frame offset set
        widget_offset = self.frame_offset + Position(x, y)

        # compute the total size we need and then align the result; which will also affect the frame offsets
        max_height = max([x.height for x in all_sizes])
        total_child_area = Size(sum([x.width for x in all_sizes]), max_height)

        offset = self.get_align_offset(total_child_area, new_size.subtract_margin(self.margin))
        widget_offset += offset

        x += offset.x
        y += offset.y

        for widget, widget_size in zip(self.widgets, all_sizes):
            # this needs the screen position added, we must do it now because this could be another Box
            widget_size.height = max_height
            widget.render(widget_size, offset=widget_offset.copy())
            # now copy this texture over to this widget
            self.texture.blit(widget.texture, (x, y))
            # no need to add the margin because it is computed in the widget size
            x += widget_size.width
            widget_offset.x += widget_size.width


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
        #if len(self.widgets) > 0:
        #    width = max([x.min_size.width for x in self.widgets])
        for widget in self.widgets:
            if widget.expand.is_horizontal:
                width = available_size.width
            else:
                width = widget.min_size.width
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

    def draw(self, new_size):
        self.texture = self.get_texture(new_size)
        self.current_size = new_size
        if self.background is not None:
            self.texture.fill(self.background)

        if len(self.widgets) == 0:
            return

        total_size = new_size.subtract_margin(self.margin)
        x = self.margin.left
        y = self.margin.top
        all_sizes = self.calculate_sizes(total_size)

        widget_offset = self.frame_offset + Position(x, y)

        for widget, widget_size in zip(self.widgets, all_sizes):
            widget.render(widget_size, offset=widget_offset.copy())
            self.texture.blit(widget.texture, (x, y))
            # no need to add the margin because it is computed in the widget size
            y += widget_size.height
            widget_offset.y += widget_size.height
