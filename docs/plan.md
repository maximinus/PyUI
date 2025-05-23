Python + Pygame UI system
=========================

We are building a custom GUI system in Python using Pygame. The design is modular, compositional, and minimal, with clear separation of concerns. It will support standard widgets, containers, layering, and event handling.

🧱 Core Concepts

    Widget: Base class for all GUI elements. Has:
        x, y, width, height
        visible, parent, children
        margin: (left, top, right, bottom) — space around the widget, applied by containers

    Container: A special widget that lays out children. Has:
        padding: (left, top, right, bottom) — space inside the container
        Lays out children using either HBox (horizontal) or VBox (vertical)
        Can include spacing (uniform space between children, optional syntactic sugar)

    Layering: The GUI supports multiple layers for stacking widgets. Each layer is an independent tree of widgets. Layers are drawn and receive input in order (from topmost to bottom).

🧩 Planned Widgets and Features

    Concrete Widgets: Label, Button, Image, TextInput (later)
    Containers: HBox, VBox, Window (single-child container)
    Composed Widgets: Menus, menu bars, tooltips, dialogs — built from primitives

📦 Layout and Rendering

    Widgets report size and position.
    Containers position children using layout rules and margins.
    Rendering is done via a draw(surface) method called top-down.
    Event propagation respects Z-order, visibility, and widget bounds.

🧪 Development Strategy

Work progresses in ordered steps:

    Widget tree and hierarchy (structure)
    Drawing and layering
    Layout and spacing
    Event handling
    Concrete widgets
    Composed elements (menus, dialogs)
    Advanced behavior (input, animation, theming)

Each step includes unit tests and builds only what is necessary for the next layer.

✅ Step 2: Drawing + Layering System
🎯 Goal

Introduce rendering capabilities to the widget system and implement Z-layer support, so widgets and containers can visually appear in the correct order and over each other.
🧱 Key Concepts to Introduce
🔹 draw(surface) method on Widget

    Each widget should implement a draw() method that:

        Draws its own visual content (background, outline, etc.)

        Then recursively calls draw() on visible children

🔹 z_index or Layering

    Support multiple layers (independent widget trees) within a RootContainer or similar top-level manager.

    Each layer is drawn in order, with higher layers appearing above lower ones.

    Layers are used for: modals, popups, tooltips, menus, etc.

🏗️ Architectural Adjustments
🔸 RootContainer

    The entry point of the UI system

    Holds an ordered list of layers (each a container or widget tree)

    Calls draw(surface) on each layer in sequence

🔸 Widget

    Gains a draw(surface) method

    Responsible for:

        Checking visible

        Drawing itself

        Translating drawing coordinates (based on x, y)

        Recursively calling draw() on children

🧪 Required Tests (for This Step to Be Considered Complete)
✅ Widget Drawing

Widget.draw(surface) is called only if visible == True

Children are drawn after their parent

    Child positions are offset correctly by parent position (i.e., relative coordinates)

✅ Layering

Layers are drawn in correct Z-order: lower-indexed layers appear under higher-indexed ones

A widget added to a higher layer appears above widgets in lower layers even if overlapping

    You can add/remove layers dynamically

✅ Visual Consistency

A widget’s draw() respects its x, y, width, height

Nested widgets are rendered in the correct place relative to the screen

    If a parent is invisible, its children are not drawn

✅ RootContainer (or equivalent)

Holds multiple widget trees as layers

Provides draw_all(surface) or similar method that calls draw() for each layer in Z order
