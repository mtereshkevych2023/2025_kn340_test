import unittest
from main import find_min


class TestFindMin(unittest.TestCase):

    def test_min_integers(self):
        numbers = [5, 2, 9, -1, 0]
        self.assertEqual(find_min(numbers), -1)

    def test_min_floats(self):
        numbers = [2.5, 1.1, 3.9, -0.4]
        self.assertEqual(find_min(numbers), -0.4)

    def test_min_mixed_int_float(self):
        numbers = [3, 2.2, -5, 0.0, 10]
        self.assertEqual(find_min(numbers), -5)


if __name__ == "__main__":
    unittest.main()
