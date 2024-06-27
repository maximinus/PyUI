import unittest

from pyui.base import Size, Margin


class TestSize(unittest.TestCase):
    def test_init(self):
        size = Size(5, 8)
        self.assertEqual(size.width, 5)
        self.assertEqual(size.height, 8)

    def test_invert(self):
        size = Size(1, 2)
        size.invert()
        self.assertEqual(size.width, 2)
        self.assertEqual(size.height, 1)

    def test_double_inversion(self):
        size = Size(3, 5)
        size.invert()
        size.invert()
        self.assertEqual(size.width, 3)
        self.assertEqual(size.height, 5)

    def test_added_margin(self):
        size = Size(10, 20)
        size = size.add_margin(Margin(1, 2, 3, 4))
        self.assertEqual(size.width, 13)
        self.assertEqual(size.height, 27)

    def test_subtracted_margin(self):
        size = Size(15, 15)
        size = size.subtract_margin(Margin(4, 3, 2, 1))
        self.assertEqual(size.width, 8)
        self.assertEqual(size.height, 12)

    def test_add(self):
        size1 = Size(21, 22)
        size2 = Size(3, 8)
        total = size1 + size2
        self.assertEqual(total.width, 24)
        self.assertEqual(total.height, 30)

    def test_equality(self):
        size1 = Size(3, 3)
        size2 = Size(3, 3)
        self.assertEqual(size1, size2)

    def test_inequality(self):
        size1 = Size(1, 2)
        size2 = Size(7, 4)
        self.assertNotEqual(size1, size2)
