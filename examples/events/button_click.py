from pyui.base import Size, Align, Margin, Position, Expand
from pyui.events.loop import app
from pyui.widgets import Button, VBox, Frame, TextLabel


def get_layout():
    m = Margin(16, 16, 16, 16)
    button = Button('Click Me', Size(120, 60), margin=m, align=Align.CENTER)
    label = TextLabel('Clicked 0 times', margin=m, align=Align.CENTER)
    box = VBox(align=Align.CENTER, widgets=[button, label])
    frame = Frame(size=Size(800, 600), pos=Position(0, 0), widget=box, background=(80, 80, 80))
    return frame


if __name__ == '__main__':
    layout = get_layout()
    app.push_frame(layout)
    app.event_loop()
