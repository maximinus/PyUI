from pyui.base import Size, Expand, Align, Margin, Position
from pyui.events.loop import app
from pyui.widgets import Button, HBox, Frame


def get_layout():
    button1 = Button('Hello', Size(120, 60), expand=Expand.HORIZONTAL, align=Align.CENTER)
    button2 = Button('World', Size(120, 60), expand=Expand.HORIZONTAL, align=Align.CENTER)
    button3 = Button('Again', Size(120, 60), expand=Expand.HORIZONTAL, align=Align.CENTER)
    box = HBox(align=Align.CENTER, widgets=[button1, button2, button3])
    frame = Frame(size=Size(800, 600), pos=Position(0, 0), widget=box, margin=Margin(50, 50, 50, 50), background=(80, 80, 80))
    return frame


if __name__ == '__main__':
    layout = get_layout()
    app.push_frame(layout)
    app.event_loop()
