import unittest


from Steering import Steering


class TestBasicos(unittest.TestCase):

    def test_right(self):
        steering = Steering()
        self.assertEqual(21, steering.right)

    def test_left(self):
        steering = Steering()
        self.assertEqual(20, steering.left)