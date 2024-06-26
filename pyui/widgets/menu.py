import pygame

from pyui.base import get_asset, Size, Margin, Position
from pyui.widget_base import Widget
from pyui.widgets import Border, VBox, HBox, TextLabel, Image, Spacer


class MenuItem(Widget):
    def __init__(self, text, icon_name=None):
        super().__init__()
        self.widget = HBox()
        if icon_name is not None:
            icon = Image(get_asset(f'icons/{icon_name}.png'), margin=Margin(2, 6, 4, 4))
            self.widget.add_widget(icon)
        else:
            self.widget.add_widget(Spacer(size=Size(22, 20)))
        self.widget.add_widget(TextLabel(text))
        self.size = self.widget.min_size
        self.highlighted = False

    @property
    def min_size(self):
        return self.size.add_margin(self.margin)

    def render(self, surface, pos, available_size=None):
        self.widget.render(surface, pos, available_size)
        self.render_rect = self.widget.render_rect
        self.redraw = False


class Menu(Border):
    def __init__(self, pos, items=None):
        box = VBox(margin=Margin(6, 6, 6, 6))
        if items is not None:
            for item in items:
                box.add_widget(item)
        super().__init__(pos, widget=box)

    def add_menu_item(self, menu_item):
        self.widget.add_widget(menu_item)

    def register_events(self):
        pass
