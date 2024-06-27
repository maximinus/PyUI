import unittest

from pyui.base import Align


class TestAlignment(unittest.TestCase):
    def test_top_left(self):
        foo = Align(Align.LEFT | Align.TOP)
        self.assertEqual(foo.horizontal(), Align.LEFT)
        self.assertEqual(foo.vertical(), Align.TOP)

    def test_top_right(self):
        foo = Align(Align.RIGHT | Align.TOP)
        self.assertEqual(foo.horizontal(), Align.RIGHT)
        self.assertEqual(foo.vertical(), Align.TOP)

    def test_bottom_left(self):
        foo = Align(Align.BOTTOM | Align.LEFT)
        self.assertEqual(foo.horizontal(), Align.LEFT)
        self.assertEqual(foo.vertical(), Align.BOTTOM)

    def test_bottom_right(self):
        foo = Align(Align.BOTTOM | Align.RIGHT)
        self.assertEqual(foo.horizontal(), Align.RIGHT)
        self.assertEqual(foo.vertical(), Align.BOTTOM)

    def test_top(self):
        foo = Align(Align.TOP)
        self.assertEqual(foo.horizontal(), Align.CENTER)
        self.assertEqual(foo.vertical(), Align.TOP)

    def test_bottom(self):
        foo = Align(Align.BOTTOM)
        self.assertEqual(foo.horizontal(), Align.CENTER)
        self.assertEqual(foo.vertical(), Align.BOTTOM)

    def test_left(self):
        foo = Align(Align.LEFT)
        self.assertEqual(foo.horizontal(), Align.LEFT)
        self.assertEqual(foo.vertical(), Align.CENTER)

    def test_right(self):
        foo = Align(Align.RIGHT)
        self.assertEqual(foo.horizontal(), Align.RIGHT)
        self.assertEqual(foo.vertical(), Align.CENTER)

    def test_center(self):
        foo = Align(Align.CENTER)
        self.assertEqual(foo.horizontal(), Align.CENTER)
        self.assertEqual(foo.vertical(), Align.CENTER)
