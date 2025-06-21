from pyui.window import Window
from pyui.widgets import VBox, MenuBar, Spacer, TextEditor
from pyui.helpers import Size, Expand


if __name__ == "__main__":
    window = Window(Size(800, 600), title="Minerva IDE")
    
    menu = MenuBar(background=(150, 150, 150))
    menu.add_menu("File")
    menu.add_menu("Edit")
    menu.add_menu("Selection")
    menu.add_child(Spacer(expand=Expand.HORIZONTAL))
    menu.add_menu("Help")

    text_editor = TextEditor(expand=Expand.BOTH)

    box = VBox(expand=Expand.BOTH)
    box.add_child(menu)
    box.add_child(text_editor)
    window.add_widget(box)    
    window.run()
