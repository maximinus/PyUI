from pyui.window import Window
from pyui.widgets import Image, HBox, NinePatchData, NinePatch
from pyui.helpers import Size, Margin, Expand, Align
from pyui.assets import get_font, get_image

if __name__ == "__main__":
    window = Window(Size(640, 480), background=(200, 200, 200))
    
    font = get_font("creato.otf", 20)
    data = NinePatchData.from_json("frame.json")
    nine = NinePatch(data, Size(200, 200),
                     expand=Expand.NONE,
                     background=(200, 200, 200))
    picture = get_image("dog_alpha.png")
    img = Image(picture)
    box = HBox()
    box.add_child(nine)
    box.add_child(img)
    window.add_child(box)
    
    window.run()
