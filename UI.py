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
        self._game = Game(4)

    def run(self):
        while not self._game.winner:
            print(self._game)
            fr = input("Enter line start coordinates in the form x,y: ").split(",")
            to = input("Enter line end coordinates in the form x,y: ").split(",")
            for i in range(2):
                fr[i] = int(fr[i])-1
                to[i] = int(to[i])-1
            self._game.play(fr,to)
        print(self._game)
        if self._game.winner != Game.DRAW:
            print(f"{self._game.winner} won")
        else:
            print("It's a draw")

if __name__ == "__main__":
    # For unit testing
    pass
