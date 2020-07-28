from enum import auto

class Game:

    #Constants
    P1 = 'P1'
    P2 = 'P2'
    EMPTY = " "
    DRAW = auto()

    def __init__(self,dim):
        self._dim = dim
        self._rowLines = [[self.EMPTY for _ in range(self._dim - 1)] for _ in range(self._dim)]
        self._colLines = [[self.EMPTY for _ in range(self._dim)] for _ in range(self._dim - 1)]
        self._boxes = [[self.EMPTY for _ in range(self._dim - 1)] for _ in range(self._dim - 1)]
        self._player = self.P1

    def __repr__(self):
        printable = "\n  "
        for i in range(self._dim):
            printable += str(i+1) + "  "
        for i in range(self._dim):
            printable += f"\n{i+1} "
            for p in self._rowLines[i]:
                printable += "." + p.rjust(2)
            printable += ".\n  "
            try:
                for p in range(len(self._colLines[i])):
                    printable += self._colLines[i][p] + self._boxes[i][p].rjust(2)
            except IndexError:
                pass
        return printable

    def play(self, fr, to):
        pass

    @property
    def winner(self):
        pass

if __name__ == "__main__":
    # For unit testing
    pass
