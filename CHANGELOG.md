# Changelog

## 0.1.1

### Added

*   **Drawing & Layering (Step 2):**
    *   Added basic `draw(surface)` method to `Widget` for recursive drawing.
    *   Created `pyui/root_container.py` with `RootContainer` class to manage drawing layers.
    *   `RootContainer` draws layers in Z-order (list order).
    *   Created `tests/test_drawing_layering.py` with tests for drawing visibility, recursion, and layer order.
    *   Added `DrawableWidget` helper class within tests to facilitate testing draw recursion without complex patching.

### Changed

*   `Widget.draw` now calls `draw` on visible children.
*   `pyui/__init__.py` now exports `RootContainer`.
*   Refactored drawing tests to use `DrawableWidget` helper instead of patching `Widget.draw` directly, resolving persistent test errors.

### Removed

*   Removed `sys.path` manipulations from test files (`tests/test_widget.py`, `tests/test_drawing_layering.py`); tests should be run using `python -m unittest` from the project root.
*   Removed unnecessary `pygame` module mocking and type hints that interfered with testing.

## 0.1.0

### Added

*   **Core Widget Structure (Step 1):**
    *   Created `pyui/widget.py` with the base `Widget` class.
    *   Implemented core properties: `x`, `y`, `width`, `height`, `visible`, `parent` (using weakref), `children`, `name`.
    *   Implemented hierarchy management methods: `add_child`, `remove_child`.
    *   Implemented hierarchy traversal/query methods: `get_root`, `find_by_name`, `is_descendant_of`.
    *   Implemented position calculation: `get_absolute_position`.
    *   Implemented hierarchical visibility check: `is_visible`.
    *   Added checks to prevent circular parenting.
    *   Created `pyui/__init__.py` to make `pyui` a package.
*   **Testing:**
    *   Created `tests/test_widget.py` with comprehensive unit tests for the `Widget` class using the `unittest` library.

### Fixed

*   Corrected the logic for circular dependency prevention in `Widget.parent` setter and `Widget.add_child`. 
