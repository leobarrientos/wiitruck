from gpiozero import LED


class Steering:

    def __init__(self, left: LED, right: LED):
        self.left = left
        self.right = right

    def status(self):
        print(self.left.value)
        val = self.left.value
        return val

    def turn_left(self):
        self.left.on()
        self.right.off()
        return True

    def turn_right(self):
        self.left.off()
        self.right.on()
        return True

    def turn_straight(self):
        self.left.off()
        self.right.off()
        return True

