import unittest
from src.cl.rockstar.Steering import Steering
from gpiozero import Device, Servo, PWMOutputDevice
from gpiozero.pins.mock import MockFactory, MockPWMPin, MockPin


class TestBasicos(unittest.TestCase):
    # Set the default pin factory to a mock factory
    Device.pin_factory = MockFactory()
    Device.pin_factory.pin_class = MockPWMPin

    def test_servo_pins(self):
        p = Device.pin_factory.pin(1)
        with Servo(1) as device:
            assert device.pwm_device.pin is p
            assert isinstance(device.pwm_device, PWMOutputDevice)

    def test_straight(self):
        p = Device.pin_factory.pin(17)
        with Servo(17, min_pulse_width=5/10000, max_pulse_width=25/10000) as servo:
            steering = Steering(servo)
            servo.mid()
            self.assertEqual(True, steering.straight())
            self.assertEqual(0, servo.value)

    def test_turn_left(self):
        p = Device.pin_factory.pin(17)
        with Servo(17, min_pulse_width=5/10000, max_pulse_width=25/10000) as servo:
            steering = Steering(servo)
            self.assertGreater(0, steering.turn_left(15).value, 'OKff')
    #
    # def test_turn_right(self):
    #     with Servo(17) as servo:
    #         steering = Steering(servo)
    #         self.assertEqual(servo.value, steering.turn_right(1))
    #
