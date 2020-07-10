from gpiozero import LED

from cl.rockstar.Emotor import Emotor
from cl.rockstar.Steering import Steering
import cwiid
import time


class Engine:

    def __init__(self, p_emotor, p_steering):
        self.wii = None 
        self.emotor = p_emotor
        self.steering = p_steering

    def shutdown(self):
        print('\nClosing connection ...')
        # NOTE: This is how you RUMBLE the Wiimote
        self.wii.rumble = 1
        time.sleep(0.3)
        self.wii.rumble = 0
        self.wii.led = 0
        return self.wii

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
            return self
        except RuntimeError:
            print("Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!")
            return RuntimeError
