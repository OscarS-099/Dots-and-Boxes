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
        dim = 12
        while dim < 3 or dim > 10:
            try:
                dim = int(input("Enter the dimension of the board (between 3 and 10 inclusive): "))
            except ValueError:
                print("Input isn't an integer")
                continue
        self._game = Game(dim)

    def run(self):
        while not self._game.winner:
            print(self._game)
            while True:
                fr = input("Enter line start coordinates in the form x,y: ").split(",")
                to = input("Enter line end coordinates in the form x,y: ").split(",")
                try:
                    for i in range(2):
                        fr[i] = int(fr[i])-1
                        to[i] = int(to[i])-1
                        if fr[i] > self._game.getDim() or fr[i] < 0 or to[i] > self._game.getDim() or to[i] < 0:
                            print("Input is not withing board dimensions")
                            continue
                except ValueError:
                    print("One or more of the inputs weren't integers")
                    continue
                if abs(fr[0]-fr[1]) > 1 or abs(to[0]-to[1]) > 1:
                    print("The line is too long; it should span between two adjacent dots")
                    continue
                if not self._game.occupied(fr,to):
                    print("There is already a line there")
                    continue
                break
            self._game.play(fr,to)
        print(self._game)
        if self._game.winner != Game.DRAW:
            print(f"{self._game.winner} won")
            print(f"The score was: {Game.P1} - {self._game.getScore(Game.P1)}, {Game.P2} - {self._game.getScore(Game.P2)}")
        else:
            print("It's a draw")

if __name__ == "__main__":
    # For unit testing
    pass
