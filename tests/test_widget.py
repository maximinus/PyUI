import unittest

from pyui.widget import Widget

class TestWidget(unittest.TestCase):

    def test_init_defaults(self):
        widget = Widget()
        self.assertEqual(widget.x, 0)
        self.assertEqual(widget.y, 0)
        self.assertEqual(widget.width, 0)
        self.assertEqual(widget.height, 0)
        self.assertTrue(widget.visible)
        self.assertIsNone(widget.parent)
        self.assertEqual(widget.children, [])
        self.assertIsNone(widget.name)

    def test_init_with_values(self):
        parent_widget = Widget(name="parent")
        widget = Widget(x=10, y=20, width=100, height=50, visible=False, parent=parent_widget, name="child")
        self.assertEqual(widget.x, 10)
        self.assertEqual(widget.y, 20)
        self.assertEqual(widget.width, 100)
        self.assertEqual(widget.height, 50)
        self.assertFalse(widget.visible)
        self.assertIs(widget.parent, parent_widget)
        self.assertIn(widget, parent_widget.children)
        self.assertEqual(widget.name, "child")

    def test_add_remove_child(self):
        parent = Widget()
        child1 = Widget()
        child2 = Widget()

        parent.add_child(child1)
        self.assertIn(child1, parent.children)
        self.assertIs(child1.parent, parent)

        parent.add_child(child2)
        self.assertIn(child2, parent.children)
        self.assertIs(child2.parent, parent)
        self.assertEqual(len(parent.children), 2)

        parent.remove_child(child1)
        self.assertNotIn(child1, parent.children)
        self.assertIsNone(child1.parent)
        self.assertEqual(len(parent.children), 1)

        parent.remove_child(child2)
        self.assertNotIn(child2, parent.children)
        self.assertIsNone(child2.parent)
        self.assertEqual(len(parent.children), 0)

    def test_add_child_moves_from_old_parent(self):
        parent1 = Widget()
        parent2 = Widget()
        child = Widget()

        parent1.add_child(child)
        self.assertIn(child, parent1.children)
        self.assertIs(child.parent, parent1)

        parent2.add_child(child) # Should automatically remove from parent1
        self.assertNotIn(child, parent1.children)
        self.assertIn(child, parent2.children)
        self.assertIs(child.parent, parent2)

    def test_get_root(self):
        root = Widget()
        child = Widget(parent=root)
        grandchild = Widget(parent=child)

        self.assertIs(root.get_root(), root)
        self.assertIs(child.get_root(), root)
        self.assertIs(grandchild.get_root(), root)

    def test_find_by_name(self):
        root = Widget(name="root")
        child1 = Widget(parent=root, name="child1")
        child2 = Widget(parent=root, name="child2")
        grandchild1 = Widget(parent=child1, name="grandchild1")

        self.assertIs(root.find_by_name("root"), root)
        self.assertIs(root.find_by_name("child1"), child1)
        self.assertIs(root.find_by_name("child2"), child2)
        self.assertIs(root.find_by_name("grandchild1"), grandchild1)
        self.assertIsNone(root.find_by_name("nonexistent"))
        self.assertIs(child1.find_by_name("grandchild1"), grandchild1)
        self.assertIsNone(child2.find_by_name("grandchild1"))

    def test_is_descendant_of(self):
        root = Widget()
        child = Widget(parent=root)
        grandchild = Widget(parent=child)
        other_widget = Widget()

        self.assertTrue(child.is_descendant_of(root))
        self.assertTrue(grandchild.is_descendant_of(root))
        self.assertTrue(grandchild.is_descendant_of(child))
        self.assertFalse(root.is_descendant_of(child))
        self.assertFalse(child.is_descendant_of(grandchild))
        self.assertFalse(root.is_descendant_of(root))
        self.assertFalse(child.is_descendant_of(child))
        self.assertFalse(child.is_descendant_of(other_widget))
        self.assertFalse(other_widget.is_descendant_of(root))

    def test_get_absolute_position(self):
        root = Widget(x=10, y=20)
        child = Widget(x=5, y=15, parent=root)
        grandchild = Widget(x=2, y=3, parent=child)

        self.assertEqual(root.get_absolute_position(), (10, 20))
        self.assertEqual(child.get_absolute_position(), (15, 35)) # 10+5, 20+15
        self.assertEqual(grandchild.get_absolute_position(), (17, 38)) # 15+2, 35+3

    def test_visibility(self):
        # Note: is_visible checks the hierarchy
        root = Widget(visible=True)
        child_visible = Widget(parent=root, visible=True)
        child_invisible = Widget(parent=root, visible=False)
        grandchild_of_visible = Widget(parent=child_visible, visible=True)
        grandchild_of_invisible = Widget(parent=child_invisible, visible=True)
        invisible_grandchild_of_visible = Widget(parent=child_visible, visible=False)

        self.assertTrue(root.is_visible())
        self.assertTrue(child_visible.is_visible())
        self.assertFalse(child_invisible.is_visible()) # Parent is visible, but child isn't
        self.assertTrue(grandchild_of_visible.is_visible()) # All ancestors visible
        self.assertFalse(grandchild_of_invisible.is_visible()) # Parent (child_invisible) is invisible
        self.assertFalse(invisible_grandchild_of_visible.is_visible()) # Grandchild itself is invisible

        # Test changing visibility
        root.visible = False
        self.assertFalse(root.is_visible())
        self.assertFalse(child_visible.is_visible()) # Root became invisible
        self.assertFalse(grandchild_of_visible.is_visible()) # Root became invisible

    def test_circular_parenting_prevention(self):
        w1 = Widget()
        w2 = Widget(parent=w1)
        w3 = Widget(parent=w2)

        # Cannot set self as parent
        with self.assertRaises(ValueError):
            w1.parent = w1
        with self.assertRaises(ValueError):
            w1.add_child(w1)

        # Cannot set an ancestor as parent
        with self.assertRaises(ValueError):
            w1.parent = w3 # w1 is ancestor of w3
        with self.assertRaises(ValueError):
            w3.add_child(w1) # w1 is ancestor of w3


if __name__ == '__main__':
    unittest.main() 