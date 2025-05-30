# PyUI - A Modular Pygame GUI Library

PyUI is a custom GUI system built in Python using Pygame, designed with modularity, composability, and clean separation of concerns in mind. It provides a flexible widget system with comprehensive layout management and layering support.

## Features

- **Modular Widget System**
  - Base widget architecture with position, size, visibility, and margin support
  - Container widgets for flexible layouts (HBox, VBox, Stack)
  - Built-in widgets: ColorRect, Image, Label, Frame, NinePatch
  - Support for nested widget hierarchies

- **Advanced Layout System**
  - Horizontal and vertical box layouts
  - Stack layout for overlapping widgets
  - Margin and padding support
  - Precise positioning and sizing controls
  - Parent-child relationship management
  - Relative coordinate system
  - Alignment control (LEFT, CENTER, RIGHT, TOP, BOTTOM, FILL)
  - Widget expansion control (HORIZONTAL, VERTICAL, BOTH)

- **Window Management**
  - Window creation and management
  - Event handling
  - Widget rendering and updating
  - Support for building complete applications

- **Asset Management**
  - Built-in support for images, icons and fonts
  - Nine-patch texture support with JSON configuration
  - Efficient asset loading and caching

## Examples

You can find example applications in the `examples/` directory:
- `examples/no_layout/` - Basic widget usage without layouts
  - Simple color rectangles
  - Image display
  - Widget expansion demonstrations
- `examples/simple_layout/` - Layout container examples
  - HBox and VBox layouts
  - Error checking for layout issues
- `examples/frame/` - Frame widget examples
  - Nine-patch frame usage
- `examples/window/` - Window management examples
  - Simple window creation
  - Menu implementation

## Project Structure

```
pyui/
├── widgets/         # Widget implementations
│   ├── color_rect.py  # ColorRect widget
│   ├── containers.py  # HBox and VBox containers
│   ├── frame.py       # Frame widget with nine-patch
│   ├── image.py       # Image widget
│   ├── label.py       # Text label widget
│   ├── nine_patch.py  # Nine-patch implementation
│   ├── stack.py       # Stack widget for layering
├── assets/          # Asset management and resources
│   ├── icons/       # UI icons
│   ├── images/      # Image resources
│   ├── fonts/       # Font resources
│   ├── nine_patch/  # Nine-patch textures and JSON configs
├── tests/           # Comprehensive test suite
├── assets.py        # Asset loading and caching
├── helpers.py       # Helper classes (Size, Position, Margin, Align)
├── widget.py        # Base Widget class
└── window.py        # Window management
```

## Getting Started

1. Ensure you have Python and Pygame installed
2. Clone the repository
3. Run the examples to see PyUI in action

```python
# Simple example: creating a window with a color rectangle
from pyui.widgets import ColorRect
from pyui.window import Window
from pyui.helpers import Size, Expand, Align

# Create window
window = Window(Size(800, 600), title="PyUI Example")

# Create a red rectangle that expands to fill the window
rect = ColorRect(color=(255, 0, 0), expand=Expand.BOTH)

# Add the rectangle to the window
window.add_widget(rect)

# Run the window
window.run()
```

### Using Layouts

```python
# Example with layout containers
from pyui.widgets import ColorRect, HBox, VBox
from pyui.window import Window
from pyui.helpers import Size, Expand, Align, Margin

# Create window
window = Window(Size(800, 600))

# Create a horizontal box with three colored rectangles
hbox = HBox(spacing=10, margin=Margin(10, 10, 10, 10))

# Add three colored rectangles to the horizontal box
hbox.add_children([
    ColorRect(color=(255, 0, 0), expand=Expand.BOTH),
    ColorRect(color=(0, 255, 0), expand=Expand.BOTH),
    ColorRect(color=(0, 0, 255), expand=Expand.BOTH)
])

# Add the horizontal box to the window
window.add_widget(hbox)

# Run the window
window.run()
```

## Testing

The project includes a comprehensive test suite covering all major components. To run the tests:

```bash
python -m unittest discover tests
```

## License

PyUI is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

## Development Status

PyUI is under active development. The current features include:

- Window management with event handling
- Widget system with positioning, sizing, and margin support
- Layout containers (HBox, VBox, Stack)
- Basic widgets: ColorRect, Image, Label, Frame, NinePatch
- Font and text support
- Alignment system (horizontal and vertical)
- Widget expansion control
- Nine-patch texture support for complex borders and frames

Future developments may include:
- Interactive widgets (Button, TextInput)
- Event handling system for widgets
- Animation support
- Theming capabilities
- More advanced layout options
