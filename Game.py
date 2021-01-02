from enum import auto

class Game:

    #Constants
    EMPTY = ' '
    DRAW = auto()
    #Using enum.auto() allows me to generate an inconsequential value for a draw
    VTCL = '|'
    HZTL = '--'

    def __init__(self,dim,P1,P2):
        self._P1 = P1
        self._P2 = P2
        self._dim = dim
        self._rowLines = [[Game.EMPTY for _ in range(self._dim-1)] for _ in range(self._dim)]
        self._colLines = [[Game.EMPTY for _ in range(self._dim)] for _ in range(self._dim-1)]
        #Using seperate 2D arrays for row and column lines allows clearer indexing for lines
        self._boxes = [[Game.EMPTY for _ in range(self._dim-1)] for _ in range(self._dim-1)]
        self._player = self._P1
        self._points = {self._P1:0, self._P2:0}
        #Using a dictionary for points makes referencing easier than two separate variables

    def getP1Name(self):
        return self._P1

    def getP2Name(self):
        return self._P2

    def __repr__(self):
        #This is where the program constructs the printable game board
        printable = '\n  '
        for i in range(self._dim):
            printable += str(i+1) + '  '
        for i in range(self._dim):
            printable += f'\n{i+1} '
            for p in self._rowLines[i]:
                printable += '.' + p.rjust(2)
            printable += '.\n  '
            try:
                for p in range(len(self._colLines[i])):
                    printable += self._colLines[i][p]
                    printable += self._boxes[i][p].rjust(2)
            except IndexError:
                pass
        if not self.winner:
            printable += f'\n{self._player} it\'s your turn\n'
        return printable

    def play(self, fr, to):
        #This is where lines are placed after being validated in UI class
        row = min(fr[1],to[1])
        col = min(fr[0],to[0])
        sides = []
        if fr[0] == to[0]:
            self._colLines[row][col] = Game.VTCL
            if col < self._dim-1:
                sides.append('r')
            if col > 0:
                sides.append('l')
        elif fr[1] == to[1]:
            self._rowLines[row][col] = Game.HZTL
            if row < self._dim-1:
                sides.append('d')
            if row > 0:
                sides.append('u')
        self.checkBox(row, col, sides)

    def checkBox(self, row, col, sides):
        #This is where whether a placed line forms a square
        switch = []
        for side in sides:
            if side == 'r' or side == 'd':
                if self._colLines[row][col] != Game.EMPTY and self._colLines[row][col+1] != Game.EMPTY and self._rowLines[row][col] != Game.EMPTY and self._rowLines[row+1][col] != Game.EMPTY:
                    self._boxes[row][col] = self._player
                    self._points[self._player] += 1
                    switch.append(False)
                else:
                    switch.append(True)
            elif side == 'l':
                if self._colLines[row][col] != Game.EMPTY and self._colLines[row][col-1] != Game.EMPTY and self._rowLines[row][col-1] != Game.EMPTY and self._rowLines[row+1][col-1] != Game.EMPTY:
                    self._boxes[row][col-1] = self._player
                    self._points[self._player] += 1
                    switch.append(False)
                else:
                    switch.append(True)
            elif side == 'u':
                if self._colLines[row-1][col] != Game.EMPTY and self._colLines[row-1][col+1] != Game.EMPTY and self._rowLines[row][col] != Game.EMPTY and self._rowLines[row-1][col] != Game.EMPTY:
                    self._boxes[row-1][col] = self._player
                    self._points[self._player] += 1
                    switch.append(False)
                else:
                    switch.append(True)
        #Deciding whether to switch whose turn it is or not
        if len(switch) == 1:
            if switch[0]:
                self._player = self._P1 if self._player == self._P2 else self._P2
        else:
            if switch[0] and switch[1]:
                self._player = self._P1 if self._player == self._P2 else self._P2

    def getScore(self, player):
        return self._points[player]

    def getDim(self):
        return self._dim

    def occupied(self, fr, to):
        #This is where the UI class can check if a space is free
        row = min(to[1], fr[1])
        col = min(to[0], fr[0])
        if fr[0] == to[0]:
            return not self._colLines[row][col] == Game.EMPTY
        else:
            return not self._rowLines[row][col] == Game.EMPTY

    def at(self, fr, to):
        #This is where the GUI class can display whether there is a line present at a given loaction
        row = min(to[1], fr[1])
        col = min(to[0], fr[0])
        if fr[0] == to[0]:
            return self._colLines[row][col]
        else:
            return self._rowLines[row][col]

    def boxOwner(self,coord):
        #This is where the GUI class can check who has captured a box
        print(coord[0],coord[1],self._boxes[coord[0]][coord[1]])
        return self._boxes[coord[0]][coord[1]]

    @property
    def winner(self):
        #This is where the program decides if there is a winner yet
        for i in range(self._dim):
            #Checking if all posible lines have been played
            try:
                for line in self._rowLines[i]:
                    if line == Game.EMPTY:
                        return None
            except IndexError:
                pass
            try:
                for line in self._colLines[i]:
                    if line == Game.EMPTY:
                        return None
            except IndexError:
                pass
        #Deciding the winner
        if self._points[self._P1] > self._points[self._P2]:
            return self._P1
        elif self._points[self._P1] < self._points[self._P2]:
            return self._P2
        return Game.DRAW

if __name__ == '__main__':
    # For unit testing
    pass
