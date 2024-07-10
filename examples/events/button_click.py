from pyui.base import Size, Align, Margin, Position
from pyui.events.events import Event
from pyui.events.loop import app
from pyui.widgets import Button, VBox, Frame, TextLabel


class ExampleApp:
    def __init__(self):
        m = Margin(16, 16, 16, 16)
        self.button = Button('Click Me', Size(120, 60), margin=m, align=Align.CENTER)
        self.label = TextLabel('Clicked 0 times', margin=m, align=Align.CENTER)
        box = VBox(align=Align.CENTER, widgets=[self.button, self.label])
        self.count = 0
        frame = Frame(size=Size(800, 600), pos=Position(0, 0), widget=box, background=(80, 80, 80))
        # when the button is clicked, update the string
        self.button.connect(Event.MouseLeftClickDown, self.button_clicked)
        app.push_frame(frame)

    def button_clicked(self, data):
        self.count += 1
        self.label.update_text(f'Clicked {self.count} times')
        app.set_dirty(self.label)


if __name__ == '__main__':
    my_app = ExampleApp()
    app.event_loop()
