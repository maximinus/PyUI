import unittest

from pyui.helpers import Size, Margin, Position, Align, Expand


class TestSize(unittest.TestCase):
    def test_width(self):
        size = Size(10, 20)
        self.assertEqual(size.width, 10)
    
    def test_height(self):
        size = Size(10, 20)
        self.assertEqual(size.height, 20)
    
    def test_equality(self):
        size1 = Size(10, 20)
        size2 = Size(10, 20)
        self.assertEqual(size1, size2)
    
    def test_inequality(self):
        size1 = Size(10, 20)
        size2 = Size(20, 10)
        self.assertNotEqual(size1, size2)
    
    def test_addition(self):
        size1 = Size(10, 20)
        size2 = Size(5, 5)
        expected_size = Size(15, 25)
        self.assertEqual(size1 + size2, expected_size)


class TestPosition(unittest.TestCase):
    def test_x_position(self):
        pos = Position(10, 20)
        self.assertEqual(pos.x, 10)
    
    def test_y_position(self):
        pos = Position(10, 20)
        self.assertEqual(pos.y, 20)
    
    def test_equality(self):
        pos1 = Position(10, 20)
        pos2 = Position(10, 20)
        self.assertEqual(pos1, pos2)
    
    def test_inequality(self):
        pos1 = Position(10, 20)
        pos2 = Position(20, 10)
        self.assertNotEqual(pos1, pos2)
    
    def test_addition(self):
        pos1 = Position(10, 20)
        pos2 = Position(5, 5)
        expected_position = Position(15, 25)
        self.assertEqual(pos1 + pos2, expected_position)


class TestMargin(unittest.TestCase):
    def test_left(self):
        margin = Margin(10, 20, 30, 40)
        self.assertEqual(margin.left, 10)
    
    def test_right(self):
        margin = Margin(10, 20, 30, 40)
        self.assertEqual(margin.right, 20)
    
    def test_top(self):
        margin = Margin(10, 20, 30, 40)
        self.assertEqual(margin.top, 30)
    
    def test_bottom(self):
        margin = Margin(10, 20, 30, 40)
        self.assertEqual(margin.bottom, 40)
    
    def test_equality(self):
        margin1 = Margin(10, 20, 30, 40)
        margin2 = Margin(10, 20, 30, 40)
        self.assertEqual(margin1, margin2)
    
    def test_inequality(self):
        margin1 = Margin(10, 20, 30, 40)
        margin2 = Margin(20, 10, 40, 30)
        self.assertNotEqual(margin1, margin2)
    
    def test_size(self):
        margin = Margin(10, 20, 30, 40)
        expected_size = Size(30, 70)
        self.assertEqual(margin.size, expected_size)
    
    def test_default(self):
        margin = Margin()
        expected_margin = Margin(0, 0, 0, 0)
        self.assertEqual(margin, expected_margin)


class TestAlignment(unittest.TestCase):
    def test_top_left(self):
        align = Align(Align.LEFT, Align.TOP)
        self.assertEqual(align.horizontal, Align.LEFT)
        self.assertEqual(align.vertical, Align.TOP)

    def test_top(self):
        align = Align(Align.CENTER, Align.TOP)
        self.assertEqual(align.horizontal, Align.CENTER)
        self.assertEqual(align.vertical, Align.TOP)

    def test_top_right(self):
        align = Align(Align.RIGHT, Align.TOP)
        self.assertEqual(align.horizontal, Align.RIGHT)
        self.assertEqual(align.vertical, Align.TOP)
    
    def test_left(self):
        align = Align(Align.LEFT, Align.CENTER)
        self.assertEqual(align.horizontal, Align.LEFT)
        self.assertEqual(align.vertical, Align.CENTER)
    
    def test_center(self):
        align = Align(Align.CENTER, Align.CENTER)
        self.assertEqual(align.horizontal, Align.CENTER)
        self.assertEqual(align.vertical, Align.CENTER)
    
    def test_right(self):
        align = Align(Align.RIGHT, Align.CENTER)
        self.assertEqual(align.horizontal, Align.RIGHT)
        self.assertEqual(align.vertical, Align.CENTER)
    
    def test_bottom_left(self):
        align = Align(Align.LEFT, Align.BOTTOM)
        self.assertEqual(align.horizontal, Align.LEFT)
        self.assertEqual(align.vertical, Align.BOTTOM)
    
    def test_bottom(self):
        align = Align(Align.CENTER, Align.BOTTOM)
        self.assertEqual(align.horizontal, Align.CENTER)
        self.assertEqual(align.vertical, Align.BOTTOM)
    
    def test_bottom_right(self):
        align = Align(Align.RIGHT, Align.BOTTOM)
        self.assertEqual(align.horizontal, Align.RIGHT)
        self.assertEqual(align.vertical, Align.BOTTOM)
    
    def test_stretch(self):
        align = Align(Align.FILL, Align.FILL)
        self.assertEqual(align.horizontal, Align.FILL)
        self.assertEqual(align.vertical, Align.FILL)


class TestExpand(unittest.TestCase):
    def test_no_expand(self):
        expand = Expand.NONE
        self.assertEqual(expand.horizontal, False)
        self.assertEqual(expand.vertical, False)
    
    def test_horizontal_expand(self):
        expand = Expand.HORIZONTAL
        self.assertEqual(expand.horizontal, True)
        self.assertEqual(expand.vertical, False)
    
    def test_vertical_expand(self):
        expand = Expand.VERTICAL
        self.assertEqual(expand.horizontal, False)
        self.assertEqual(expand.vertical, True)
    
    def test_both_expand(self):
        expand = Expand.BOTH
        self.assertEqual(expand.horizontal, True)
        self.assertEqual(expand.vertical, True)
