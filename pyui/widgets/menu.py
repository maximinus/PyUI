from pyui.base import get_asset, Align
from pyui.widget_base import Widget
from pyui.widgets import Border, VBox, HBox, TextLabel, Image


class MenuItem(Widget):
    def __init__(self, text, icon_name=None):
        super().__init__()
        self.box = HBox()
        self.icon = None
        if icon_name is not None:
            self.icon = get_asset(f'icons/{icon_name}.png')
            self.box.add_widget(Image(self.icon))
        self.box.add_widget(TextLabel(text))
        self.size = self.box.min_size

    def render(self, surface, x, y, available_size=None):
        self.box.render(surface, x, y, available_size)


class Menu(Border):
    def __init__(self, items=None):
        box = VBox()
        if items is not None:
            for item in items:
                box.add_widget(item)
        super().__init__(widget=box)

    def add_menu_item(self, menu_item):
        self.widget.add_widget(menu_item)
