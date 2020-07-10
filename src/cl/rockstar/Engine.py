from gpiozero import LED

from cl.rockstar.Emotor import Emotor
from cl.rockstar.Steering import Steering
import cwiid
import time


class Engine:

    def __init__(self, e_motor, steering):
        self.wii = None
        self.e_motor = e_motor
        self.steering = steering

    def stop(self, wii):
        print('\nClosing connection ...')
        # NOTE: This is how you RUMBLE the Wiimote
        wii.rumble = 1
        time.sleep(0.3)
        wii.rumble = 0
        wii.led = 0
        return wii

    def start(self):
        print('Encendido!!!')
        print('Please press buttons 1 + 2 on your Wiimote now ...')
        time.sleep(1)

        # This code attempts to connect to your Wiimote and if it fails the program quits
        try:
            wii = cwiid.Wiimote()
            print('Wiimote connection established!\n')
            print('Go ahead and press some buttons\n')
            print('Press PLUS and MINUS together to disconnect and quit.\n')

            # turn on led to show connected
            wii.led = 1
            time.sleep(3)
            wii.rumble = 1
            time.sleep(0.2)
            wii.rumble = 0

            self.wii = wii
            return self.wii
        except RuntimeError:
            print("Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!")
            return RuntimeError

