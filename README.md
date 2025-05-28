# PyUI - A Modular Pygame GUI Library

PyUI is a custom GUI system built in Python using Pygame, designed with modularity, composability, and clean separation of concerns in mind. It provides a flexible widget system with comprehensive layout management and layering support.

## Features

- **Modular Widget System**
  - Base widget architecture with position, size, visibility, and margin support
  - Container widgets for flexible layouts (HBox, VBox, Stack)
  - Built-in widgets: ColorRect, Image, Label, and more
  - Support for nested widget hierarchies

- **Advanced Layout System**
  - Horizontal and vertical box layouts
  - Stack layout for overlapping widgets
  - Margin and padding support
  - Precise positioning and sizing controls
  - Parent-child relationship management
  - Relative coordinate system
  - Alignment control (LEFT, CENTER, RIGHT, TOP, BOTTOM)

- **Layer Management**
  - Z-order rendering support
  - Independent widget trees per layer
  - Support for overlapping widgets
  - Perfect for modals, popups, tooltips, and menus

- **Asset Management**
  - Built-in support for images, icons and fonts
  - Nine-patch texture support
  - Efficient asset loading and caching

## Examples

You can find example applications in the `examples/` directory:
- `examples/no_layout/` - Basic widget usage without layouts
  - Simple color rectangles
  - Image display
  - Widget expansion demonstrations
- `examples/simple_layout/` - Layout container examples
  - HBox and VBox layouts
  - Stack layout for overlapping widgets
- `examples/window/` - Window management examples

## Project Structure

```
pyui/
├── widgets/         # Widget implementations
├── assets/          # Asset management and resources
│   ├── icons/       # UI icons
│   ├── images/      # Image resources
│   ├── fonts/       # Font resources
│   └── nine_patch/  # Nine-patch textures
├── tests/           # Comprehensive test suite
└── __pycache__/     # Python bytecode cache
```

## Getting Started

1. Ensure you have Python and Pygame installed
2. Clone the repository
3. Run the examples to see PyUI in action

```python
from pyui.widgets import ColorRect
from pyui.helpers import Size, Position

# Create a simple colored rectangle
rect = ColorRect(color=(255, 0, 0))
rect.size = Size(100, 100)
rect.position = Position(50, 50)

# Render in your game loop
rect.draw(screen)
```

## Testing

The project includes a comprehensive test suite covering all major components. To run the tests:

```bash
./run_tests.sh
```

## License

PyUI is licensed under the GNU General Public License v3.0. See the LICENSE file for details.

## Development Status

PyUI is under active development. The core widget system, drawing capabilities, and basic layouts are implemented. Current features include:

- Widget system with positioning, sizing, and margin support
- Layout containers (HBox, VBox, Stack)
- Basic widgets: ColorRect, Image, Label
- Font and text support
- Alignment system (horizontal and vertical)

Future developments will include:
- Additional widgets (Button, TextInput)
- Composed widgets (menus, menu bars, tooltips, dialogs)
- Event handling system
- Animation support
- Theming capabilities
