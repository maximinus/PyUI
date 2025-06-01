import pygame

from pyui.widgets import HBox, VBox, Label, Frame
from pyui.helpers import Margin, Align, Expand
from pyui.assets import get_font, get_nine_patch_data
from pyui.messaging import message_bus, MessageType, Message


class Menu(Frame):
    def __init__(self, *args, **kwargs):
        patch_data = get_nine_patch_data("frame.json")
        background = (180, 180, 180)
        box = VBox()
        font = get_font("creato.otf", 16)
        for i in ["New File", "Open File", "Save", "Save As", "Exit"]:
            box.add_child(Label(i, font, (40, 40, 40),
                                margin=Margin(6, 6, 6, 6),
                                align=Align(Align.LEFT, Align.CENTER)))
        super().__init__(box, patch_data, background=background)


class MenuItem(Label):
    """A menu item that can be clicked."""
    def __init__(self, text: str, font, menu: Menu, **kwargs):
        super().__init__(text, font, (40, 40, 40),
                         margin=Margin(12, 12, 5, 5), **kwargs)
        self.menu = menu
        self.menu.modal = True

    def render(self, mouse, destination, position, size):
        self.image.clear()
        if self.is_mouse_over(mouse, position, size):
            if mouse.left_click_down:
                # here we need to add the menu
                message_bus.post(Message(MessageType.ADD_WIDGET, self, self.menu))
            self.background = (100, 100, 100, 255)
        else:
            self.background = (0, 0, 0, 0)
        return super().render(mouse, destination, position, size)


class MenuBar(HBox):
    """A simple menu bar widget that can hold multiple menu items."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, align=Align(Align.FILL, Align.TOP),
                         expand=Expand.HORIZONTAL, **kwargs)
        self.font = get_font("creato.otf", 18)
    
    def add_menu(self, menu: str, right: bool = False):
        label = MenuItem(menu, self.font, Menu())
        self.add_child(label)
    
    def render(self, mouse, destination, position, size):
        """Render the menu bar and its items."""
        if self.background is not None:
            pygame.draw.rect(destination, self.background,
                             (position.x, position.y, size.width, size.height))
        super().render(mouse, destination, position, size)
