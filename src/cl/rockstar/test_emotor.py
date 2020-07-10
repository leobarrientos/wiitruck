import unittest
from cl.rockstar.Emotor import Emotor
from gpiozero import Device, LED
from gpiozero.pins.mock import MockFactory


class TestBasicosEmotor(unittest.TestCase):
    # Set the default pin factory to a mock factory
    Device.pin_factory = MockFactory()

    def test_ffw(self):
        with LED(17) as ffw, LED(18) as rwd:
            emotor = Emotor(ffw, rwd)
            ffw.on()
            self.assertEqual(ffw.is_active, emotor.move_fordward().is_active)

    def test_rwd(self):
        with LED(17) as ffw, LED(18) as rwd:
            emotor = Emotor(ffw, rwd)
            rwd.on()
            self.assertEqual(rwd.is_active, emotor.move_backward().is_active)

    def test_get_status(self):
        with LED(20) as led20, LED(21) as led21:
            emotor = Emotor(led20, led21)
            self.assertEqual(0, led20.value)
            self.assertEqual(0, emotor.status())
