from src.cl.rockstar.Engine import Engine


def move_fordward():
    pass


def move_backward():
    pass


class Emotor(Engine):

    def __init__(self, fordward, backward):
        self.fordward = fordward
        self.backward = backward
