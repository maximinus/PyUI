from enum import Enum, auto


# When a widget is created, it can ask for events or not
# When a SDL event happens, we first of all look at what widget is covering that screen
# In every PyUi app, each window consists of exactly one widget
# We drill down that widget to ask if it needs this event
# If it doesn't, we then drill UP to the widgets parent to see if it needs that event
# A widget can block events from rising up the menu

# Things can send events, it's not just the SDL events that cause this
# As a GUI, we only look at key presses and mouse clicks for now

# No need to rewrite events classes, use the SDL ones