from pyui.window import Window, pyui_init
from pyui.widgets import Label, HBox, ColorRect
from pyui.helpers import Size, Margin, Expand, Align
from pyui.assets import get_font

if __name__ == "__main__":
    pyui_init()
    font = get_font("creato.otf", 20)
    label1 = Label("Really", font, color=(255, 0, 0),
                   expand=Expand.BOTH,
                   align=Align(Align.CENTER, Align.CENTER))
    label2 = Label("Basic", font, color=(0, 255, 0),
                   expand=Expand.VERTICAL,
                   align=Align(Align.CENTER, Align.CENTER))
    label3 = Label("Text", font, color=(0, 0, 255),
                   expand=Expand.BOTH,
                   align=Align(Align.CENTER, Align.CENTER))
    box = HBox(margin=Margin(10, 10, 10, 10), expand=Expand.BOTH)
    box.add_children([label1, label2, label3])
    window = Window(Size(400, 300), box, background=(200, 200, 200))
    window.run()
