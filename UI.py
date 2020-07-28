from abc import ABC, abstractmethod
from Game import Game

class Ui(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError

class Gui(Ui):
    def __init__(self):
        # Has-a Game
        pass

    def run(self):
        pass

class Terminal(Ui):
    def __init__(self):
        # Has-a Game
        pass

    def run(self):
        pass

if __name__ == "__main__":
    # For unit testing
    pass
