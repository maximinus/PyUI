from pyui.window import Window
from pyui.widgets import Label, VBox, HBox, Frame, NinePatchData
from pyui.helpers import Size, Margin
from pyui.assets import get_font


if __name__ == "__main__":
    window = Window(Size(800, 600), background=(200, 200, 200))
    font = get_font("creato.otf", 18)
    label1 = Label("Open File", font, (40, 40, 40), margin=Margin(6, 6, 6, 6))
    label2 = Label("Save File", font, (40, 40, 40), margin=Margin(6, 6, 6, 6))
    label3 = Label("Exit", font, (40, 40, 40), margin=Margin(6, 6, 6, 6))

    box = VBox()
    box.add_child(label1)
    box.add_child(label2)
    box.add_child(label3)
    frame = Frame(box, NinePatchData.from_json("frame.json"),
                  background=(230, 230, 230))
    window.add_widget(frame)
    window.run()
