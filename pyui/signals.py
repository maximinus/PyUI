from enum import Enum, auto


class SignalType(Enum):
    """
    Enum representing different types of signals.
    """
    MOUSE_IN = auto()
    MOUSE_OUT = auto()
    MOUSE_LEFT_CLICK = auto()
    MOUSE_RIGHT_CLICK = auto()
    MOUSE_MIDDLE_CLICK = auto()


DEFAULT_SIGNALS = [
    SignalType.MOUSE_IN,
    SignalType.MOUSE_OUT,
    SignalType.MOUSE_LEFT_CLICK,
    SignalType.MOUSE_RIGHT_CLICK,
    SignalType.MOUSE_MIDDLE_CLICK]


class SignalHandler:
    def __init__(self, signals=None):
        if signals is not None:
            assert isinstance(signals, list), "Signals must be a list of SignalType"
            signals = DEFAULT_SIGNALS + signals
        else:
            signals = DEFAULT_SIGNALS
        self.callbacks = {signal: [] for signal in signals}

    def trigger(self, signal_type, widget):
        # store the signal for later, we will process later
        if signal_type not in self.callbacks:
            return
        if len(self.callbacks[signal_type]) == 0:
            return
        for callback in self.callbacks[signal_type]:
            signal_stack.append([callback, widget])


def process_signal_stack():
    for signal in signal_stack:
        callback = signal[0]
        widget = signal[1]
        callback(widget)

signal_stack = []
