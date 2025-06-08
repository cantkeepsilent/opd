import unittest
from trigonometry import calculate_trigonometry
class TestCalculateTrigonometry(unittest.TestCase):
    def test_sin_trigonometry(self):
        self.assertEqual(calculate_trigonometry(30, "sin", "radians"), -0.988, delta=0.0001)
    def test_sin_trigonometry(self):
        self.assertAlmostEquals(calculate_trigonometry(45, "sin", "degrees"), 0.7071, delta=0.0001)
    def test_cos_trigonometry(self):
        self.assertAlmostEquals(calculate_trigonometry(60, "cos", "radians"), -0.9524, delta=0.0001)
    def test_cos_trigonometry(self):
        self.assertAlmostEquals(calculate_trigonometry(30, "cos", "degrees"), 0.866, delta=0.0001)
    def test_tan_trigonometry(self):
        self.assertAlmostEquals(calculate_trigonometry(45, "tan", "radians"), 1.6198, delta=0.0001)
    def test_tan_trigonometry(self):
        self.assertAlmostEquals(calculate_trigonometry( 0,"tan","degrees"), 0, delta=0.0001)
if __name__ == '__main__':
    unittest.main()