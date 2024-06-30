import pygame
from enum import Enum, auto


MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_MIDDLE = 2
MOUSE_BUTTON_RIGHT = 3


class Event(Enum):
    # an event is something that a widget will ask for a callback for
    EventNull = -1
    MouseMove = 0
    MouseLeftClickDown = 1
    MouseRightClickDown = 2
    MouseLeftClickUp = 3
    MouseRightClickUp = 4
    ClickOutside = 5


class PyUiEvent:
    type = Event.EventNull

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
    type = Event.MouseMove

    def __init__(self, event):
        self.xpos = event.pos[0]
        self.ypos = event.pos[1]
        self.xmove = event.rel[0]
        self.ymove = event.rel[1]


class MouseLeftClickDown(PyUiEvent):
    type = Event.MouseLeftClickDown

    def __init__(self, event):
        self.xpos = event.pos[0]
        self.ypos = event.pos[1]


class MouseRightClickDown(PyUiEvent):
    type = Event.MouseRightClickDown

    def __init__(self, event):
        self.xpos = event.pos[0]
        self.ypos = event.pos[1]


class MouseLeftClickUp(PyUiEvent):
    type = Event.MouseLeftClickUp

    def __init__(self, event):
        self.xpos = event.pos[0]
        self.ypos = event.pos[1]


class MouseRightClickUp(PyUiEvent):
    type = Event.MouseRightClickUp

    def __init__(self, event):
        self.xpos = event.pos[0]
        self.ypos = event.pos[1]


class ClickOutside(PyUiEvent):
    type = Event.ClickOutside

    def __init__(self, event):
        self.xpos = event.pos[0]
        self.ypos = event.pos[1]


def adjust_mouse_coords(position, event):
    if 0 <= event.type.value <= Event.ClickOutside.value:
        event.xpos -= position.x
        event.ypos -= position.y
    return event


def is_mouse_click(event_type):
    return event_type in [Event.MouseLeftClickDown, Event.MouseRightClickDown]
