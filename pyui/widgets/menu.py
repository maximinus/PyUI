from pyui.base import get_asset, Align
from pyui.widget_base import Widget
from pyui.widgets import Border, VBox, HBox, TextLabel, Image


class MenuItem(Widget):
    def __init__(self, text, icon_name=None):
        super().__init__()
        self.box = HBox()
        text_label = TextLabel(text)
        if icon_name is not None:
            icon_image = Image(get_asset(f'icons/{icon_name}.png'))
            # either one of the following is true:
            # the icon and text are the same size -> nothing to do
            # the icon is bigger or the text is bigger: center the other one
            icon_height = icon_image.min_size.height
            text_height = text_label.min_size.height
            if icon_height != text_height:
                if icon_height > text_height:
                    text_label.align = Align(Align.LEFT|Align.CENTER)
                else:
                    icon_image.align = Align(Align.LEFT|Align.CENTER)
            self.box.add_widget(icon_image)
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
