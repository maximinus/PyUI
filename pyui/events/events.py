import pygame

MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_MIDDLE = 2
MOUSE_BUTTON_RIGHT = 3

# an event is something that a widget will ask for a callback for


class PyUiEvent:
    @property
    def name(self):
        return f'{self.__class__.__name__}'

    @classmethod
    def event(cls, event):
        # return the real event or none
        match event.type:
            case pygame.MOUSEMOTION:
                return MouseMove(event)
            case pygame.MOUSEBUTTONDOWN:
                if event.button == MOUSE_BUTTON_LEFT:
                    return MouseLeftClickDown(event)
                if event.button == MOUSE_BUTTON_RIGHT:
                    return MouseRightClickDown(event)
            case pygame.MOUSEBUTTONUP:
                if event.button == MOUSE_BUTTON_LEFT:
                    return MouseLeftClickUp(event)
                if event.button == MOUSE_BUTTON_RIGHT:
                    return MouseRightClickUp(event)
            case _:
                pass


class MouseMove(PyUiEvent):
    def __init__(self, event):
        self.xpos = event.pos[0]
        self.ypos = event.pos[1]
        self.xmove = event.rel[0]
        self.ymove = event.rel[1]


class MouseLeftClickDown(PyUiEvent):
    def __init__(self, event):
        self.xpos = event.pos[0]
        self.ypos = event.pos[1]


class MouseRightClickDown(PyUiEvent):
    def __init__(self, event):
        self.xpos = event.pos[0]
        self.ypos = event.pos[1]


class MouseLeftClickUp(PyUiEvent):
    def __init__(self, event):
        self.xpos = event.pos[0]
        self.ypos = event.pos[1]


class MouseRightClickUp(PyUiEvent):
    def __init__(self, event):
        self.xpos = event.pos[0]
        self.ypos = event.pos[1]
