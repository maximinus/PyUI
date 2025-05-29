from pyui.window import Window
from pyui.widgets import Image, HBox, Frame, NinePatchData
from pyui.helpers import Size, Margin, Expand, Align
from pyui.assets import get_image

if __name__ == "__main__":
    window = Window(Size(800, 600), background=(200, 200, 200))
    picture = get_image("dog_alpha.png")
    img1 = Image(picture)
    img2 = Image(picture)
    box = HBox()
    box.add_child(img1)
    box.add_child(img2)
    frame = Frame(box, NinePatchData.from_json("frame.json"),
                  background=(150, 150, 180))
    window.add_child(frame)
    window.run()
