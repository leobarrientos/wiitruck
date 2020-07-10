import unittest
from Steering import Steering
from gpiozero import Device, LED
from gpiozero.pins.mock import MockFactory


class TestBasicos(unittest.TestCase):
    # Set the default pin factory to a mock factory
    Device.pin_factory = MockFactory()

    def test_right(self):
        with LED(20) as left, LED(21) as right:
            steering = Steering(left, right)
            self.assertEqual(right, steering.right)

    def test_left(self):
        with LED(20) as left, LED(21) as right:
            steering = Steering(left, right)
            self.assertEqual(left, steering.left)

    def test_get_status(self):
        with LED(20) as left, LED(21) as right:
            steering = Steering(left, right)
            left.on()
            self.assertEqual(1, left.value)
            self.assertEqual(1, steering.status())

    def test_straight(self):
        with LED(20) as left, LED(21) as right:
            steering = Steering(left, right)
            left.on()
            right.off()
            self.assertEqual(True, steering.straight())
            self.assertEqual(0, left.value)

    def test_turn_left(self):
        with LED(20) as left, LED(21) as right:
            steering = Steering(left, right)
            right.off()
            left.on()
            self.assertEqual(left.is_active, steering.turn_left().is_active)

    def test_turn_right(self):
        with LED(20) as left, LED(21) as right:
            steering = Steering(left, right)
            left.off()
            right.on()
            self.assertEqual(right.is_active, steering.turn_right().is_active)

