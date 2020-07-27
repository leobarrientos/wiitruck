from gpiozero import Servo


class Steering:

    def __init__(self, servo: Servo):
        servo.mid()
        self.servo = servo

    def turn_left(self, value):
        if -0.5 < self.servo.value < 0:
            value2 = (float(value) - 10) / 10
            self.servo.value = value2
        return self.servo

    def turn_right(self, value):
        if 0 < self.servo.value < 0.5:
            value2 = (float(value) - 10) / 10
            self.servo.value = value2
        return self.servo

    def straight(self):
        self.servo.mid()
        return True

