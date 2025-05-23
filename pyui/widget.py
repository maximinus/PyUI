import weakref
# import pygame # Removed for testing patch issue

class Widget:
    """Base class for all UI elements."""

    def __init__(self, x=0, y=0, width=0, height=0, visible=True, parent=None, name=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.visible = visible
        self._parent_ref = None  # Use weakref to avoid circular references
        self.children = []
        self.name = name

        if parent:
            parent.add_child(self)

    @property
    def parent(self):
        return self._parent_ref() if self._parent_ref else None

    @parent.setter
    def parent(self, value):
        if value is None:
            self._parent_ref = None
        else:
            # Prevent setting self or ancestors as parent
            # Check if the proposed parent ('value') is self or is already a descendant of self
            if value is self or value.is_descendant_of(self):
                raise ValueError("Cannot set self or a descendant as parent.")
            self._parent_ref = weakref.ref(value)

    def add_child(self, widget):
        """Adds a widget as a child of this widget."""
        if widget not in self.children:
            # Prevent adding self or an ancestor as a child
            if widget is self:
                 raise ValueError("Cannot add self as a child.")
            if self.is_descendant_of(widget):
                 raise ValueError("Cannot add an ancestor as a child.")

            if widget.parent:
                widget.parent.remove_child(widget)
            self.children.append(widget)
            widget.parent = self

    def remove_child(self, widget):
        """Removes a widget from the children of this widget."""
        if widget in self.children:
            self.children.remove(widget)
            widget.parent = None # Clear the weak reference

    def get_root(self):
        """Returns the topmost ancestor widget (the root of the UI tree)."""
        node = self
        while node.parent:
            node = node.parent
        return node

    def find_by_name(self, name):
        """Recursively searches the subtree for a widget with the given name."""
        if self.name == name:
            return self
        for child in self.children:
            found = child.find_by_name(name)
            if found:
                return found
        return None

    def is_descendant_of(self, widget):
        """Checks if this widget is a descendant of the specified widget."""
        node = self.parent
        while node:
            if node is widget:
                return True
            node = node.parent
        return False

    def get_absolute_position(self):
        """Calculates the absolute position of the widget relative to the root."""
        if self.parent:
            parent_x, parent_y = self.parent.get_absolute_position()
            return self.x + parent_x, self.y + parent_y
        else:
            return self.x, self.y

    def is_visible(self):
        """Checks if the widget and all its ancestors are visible."""
        if not self.visible:
            return False
        if self.parent:
            return self.parent.is_visible()
        return True # Root is visible if self.visible is True 

    # --- Drawing --- 
    # def draw(self, surface: pygame.Surface): # Removed type hint for testing
    def draw(self, surface):
        """Draws the widget and its visible children onto the given surface."""
        if not self.visible:
            return

        # Base widget doesn't draw anything itself, subclasses will override this
        # to draw their specific content. The position calculation will happen
        # within the subclass draw methods using get_absolute_position().

        # Recursively draw children
        for child in self.children:
            child.draw(surface) 