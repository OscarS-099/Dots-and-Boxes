from enum import auto

class Game:

    #Constants
    P1 = 'P1'
    P2 = 'P2'
    EMPTY = " "
    DRAW = auto()
    VTCL = "|"
    HZTL = "--"

    def __init__(self,dim):
        self._dim = dim
        self._rowLines = [[self.EMPTY for _ in range(self._dim-1)] for _ in range(self._dim)]
        self._colLines = [[self.EMPTY for _ in range(self._dim)] for _ in range(self._dim-1)]
        self._boxes = [[self.EMPTY for _ in range(self._dim-1)] for _ in range(self._dim-1)]
        self._player = self.P1
        self._points = {self.P1:0, self.P2:0}

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
                    printable += self._colLines[i][p]
                    printable += self._boxes[i][p].rjust(2)
            except IndexError:
                pass
        printable += f"\n{self._player} it's your turn\n"
        return printable

    def play(self, fr, to):
        row = min(fr[1],to[1])
        col = min(fr[0],to[0])
        sides = []
        if fr[0] == to[0]:
            self._colLines[row][col] = self.VTCL
            if col < self._dim-1:
                sides.append("r")
            if col > 0:
                sides.append("l")
        elif fr[1] == to[1]:
            self._rowLines[row][col] = self.HZTL
            if row < self._dim-1:
                sides.append("d")
            if row > 0:
                sides.append("u")
        self.checkBox(row, col, sides)

    def checkBox(self, row, col, sides):
        switch = []
        for side in sides:
            if side == "r" or side == "d":
                if self._colLines[row][col] != self.EMPTY and self._colLines[row][col+1] != self.EMPTY and self._rowLines[row][col] != self.EMPTY and self._rowLines[row+1][col] != self.EMPTY:
                    self._boxes[row][col] = self._player
                    self._points[self._player] += 1
                    switch.append(False)
                else:
                    switch.append(True)
            elif side == "l":
                if self._colLines[row][col] != self.EMPTY and self._colLines[row][col-1] != self.EMPTY and self._rowLines[row][col-1] != self.EMPTY and self._rowLines[row+1][col-1] != self.EMPTY:
                    self._boxes[row][col-1] = self._player
                    self._points[self._player] += 1
                    switch.append(False)
                else:
                    switch.append(True)
            elif side == "u":
                if self._colLines[row-1][col] != self.EMPTY and self._colLines[row-1][col+1] != self.EMPTY and self._rowLines[row][col] != self.EMPTY and self._rowLines[row-1][col] != self.EMPTY:
                    self._boxes[row-1][col] = self._player
                    self._points[self._player] += 1
                    switch.append(False)
                else:
                    switch.append(True)
        if len(switch) == 1:
            if switch[0]:
                self._player = self.P1 if self._player == self.P2 else self.P2
        else:
            if switch[0] and switch[1]:
                self._player = self.P1 if self._player == self.P2 else self.P2

    @property
    def winner(self):
        for i in range(self._dim):
            try:
                for line in self._rowLines[i]:
                    if line == self.EMPTY:
                        return None
            except IndexError:
                pass
            try:
                for line in self._colLines[i]:
                    if line == self.EMPTY:
                        return None
            except IndexError:
                pass
        if self._points[self.P1] > self._points[self.P2]:
            return self.P1
        elif self._points[self.P1] < self._points[self.P2]:
            return self.P2
        return self.DRAW

if __name__ == "__main__":
    # For unit testing
    pass
