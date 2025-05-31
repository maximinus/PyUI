from pyui.window import Window
from pyui.widgets import VBox, MenuBar, Spacer
from pyui.helpers import Size, Expand, Align


if __name__ == "__main__":
    window = Window(Size(640, 480), background=(200, 200, 200))
    
    menu = MenuBar(background=(150, 150, 150))
    menu.add_menu("File")
    menu.add_menu("Edit")
    menu.add_menu("Selection")
    menu.add_child(Spacer(expand=Expand.HORIZONTAL))
    menu.add_menu("Help")

    box = VBox(expand=Expand.BOTH)
    box.add_child(menu)
    window.add_widget(box)    
    window.run()
