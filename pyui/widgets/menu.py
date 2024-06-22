from pyui.base import get_asset, Size, Margin
from pyui.widget_base import Widget
from pyui.widgets import Border, VBox, HBox, TextLabel, Image, Spacer


class MenuItem(Widget):
    def __init__(self, text, icon_name=None):
        super().__init__()
        self.box = HBox()
        if icon_name is not None:
            icon = Image(get_asset(f'icons/{icon_name}.png'), margin=Margin(2, 2, 2, 2))
            self.box.add_widget(icon)
        else:
            # add a spacer
            self.box.add_widget(Spacer(size=Size(20, 20)))

        self.box.add_widget(TextLabel(text, margin=Margin(2, 2, 2, 2)))
        self.size = self.box.min_size

    def render(self, surface, x, y, available_size=None):
        self.box.render(surface, x, y, available_size)


class Menu(Border):
    def __init__(self, items=None):
        box = VBox(margin=Margin(0, 0, 0, 0))
        if items is not None:
            for item in items:
                box.add_widget(item)
        super().__init__(widget=box)

    def add_menu_item(self, menu_item):
        self.widget.add_widget(menu_item)
