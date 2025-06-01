import pygame

from pyui.widgets import HBox, VBox, Label, Frame, Image
from pyui.helpers import Margin, Align, Expand, Position
from pyui.assets import get_font, get_nine_patch_data, get_icon
from pyui.messaging import message_bus, MessageType, Message


class MenuSelection(HBox):
    # This can consist of an icon, and 2 texts
    def __init__(self, text: str, icon=None, keys=None):
        super().__init__(align=Align(Align.FILL, Align.CENTER),
                         margin=Margin(6, 6, 6, 6))
        font = get_font("creato.otf", 16)
        if icon is not None:
            self.add_child(icon)
            self.add_child(Label(text, font, (40, 40, 40),
                                 align=Align(Align.LEFT, Align.CENTER),
                                 margin=Margin(4, 0, 0, 0)))
        else:
            self.add_child(Label(text, font, (40, 40, 40),
                                 align=Align(Align.LEFT, Align.CENTER),
                                 margin=Margin(32, 0, 0, 0)))
        if keys is not None:
            self.add_child(Label(keys, get_font("creato.otf", 16),
                                 (60, 60, 46), align=Align(Align.RIGHT, Align.CENTER)))
    
    def render(self, mouse, destination, position, size):
        real_position = position + self.parent.parent.pos
        if self.is_mouse_over(mouse, real_position, size):
            self.background = (150, 150, 150, 255)
        else:
            self.background = None
        return super().render(mouse, destination, position, size)


class Menu(Frame):
    def __init__(self, *args, **kwargs):
        self.pos = Position(0, 0)
        patch_data = get_nine_patch_data("frame.json")
        background = (180, 180, 180)
        box = VBox()
        icon = Image(get_icon("open.png"))
        for i in ["New File", "Open File", "Save", "Save As", "Exit"]:
            box.add_child(MenuSelection(i, icon))
        super().__init__(box, patch_data, background=background,
                         align=Align(Align.LEFT, Align.TOP))
    
    def render(self, mouse, destination, position, size):
        super().render(mouse, destination, position + self.pos, size)


class MenuItem(Label):
    """A menu item that can be clicked."""
    def __init__(self, text: str, font, menu: Menu, **kwargs):
        super().__init__(text, font, (40, 40, 40),
                         margin=Margin(12, 12, 5, 5), **kwargs)
        self.menu = menu
        self.menu.modal = True
        message_bus.subscribe(self, MessageType.ESCAPE_PRESSED, self.escape_pressed)

    def render(self, mouse, destination, position, size):
        self.image.clear()
        if self.is_mouse_over(mouse, position, size):
            if mouse.left_click_down:
                # here we need to add the menu
                self.menu.pos = Position(position.x, position.y + size.height)
                message_bus.post(Message(MessageType.ADD_WIDGET, self, self.menu))
            self.background = (100, 100, 100, 255)
        else:
            self.background = (0, 0, 0, 0)
        return super().render(mouse, destination, position, size)
    
    def escape_pressed(self):
        """Handle escape key press to close the menu."""
        print("Escape pressed, closing menu")

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
