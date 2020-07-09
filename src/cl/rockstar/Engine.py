from src.Emotor import Emotor
from src.Steering import Steering


def start(e_motor):
    e_motor.on()


def stop(e_motor):
    e_motor.off()


class Engine:
    def __init__(self, e_motor, steering):
        fordward = 17
        backward = 18
        self.e_motor = Emotor.__init__(e_motor, fordward, backward)
        left = 20
        right = 21
        self.steering = Steering.__init__(steering, left, right)
