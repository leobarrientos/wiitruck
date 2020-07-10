from gpiozero import LED


class Emotor:

    def __init__(self, fordward: LED, backward: LED):
        self.fordward = fordward
        self.backward = backward

    def status(self):
        print(self.fordward.value)
        val = self.fordward.value
        return val

    def move_fordward(self):
        self.fordward.on()
        self.backward.off()
        return self.fordward

    def move_backward(self):
        self.fordward.off()
        self.backward.on()
        return self.backward
