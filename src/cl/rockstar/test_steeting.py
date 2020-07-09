import unittest
from Steering import Steering
from gpiozero import Device, LED
from gpiozero.pins.mock import MockFactory


class TestBasicos(unittest.TestCase):
    # Set the default pin factory to a mock factory
    Device.pin_factory = MockFactory()

    def test_right(self):
        with LED(20) as led20, LED(21) as led21:
            steering = Steering(led20, led21)
            self.assertEqual(led21, steering.right)

    def test_left(self):
        with LED(20) as led20, LED(21) as led21:
            steering = Steering(led20, led21)
            self.assertEqual(led20, steering.left)

    def test_get_status(self):
        with LED(20) as led20, LED(21) as led21:
            steering = Steering(led20, led21)
            self.assertEqual(0, led20.value)

            self.assertEqual(0, steering.status())

    def test_turn_left(self):
        with LED(20) as led20, LED(21) as led21:
            steering = Steering(led20, led21)
            self.assertEqual(True, steering.turn_left())

    def test_turn_right(self):
        with LED(20) as led20, LED(21) as led21:
            steering = Steering(led20, led21)
            self.assertEqual(True, steering.turn_right())

    def test_straight(self):
        with LED(20) as led20, LED(21) as led21:
            steering = Steering(led20, led21)
            self.assertEqual(True, steering.straight())

