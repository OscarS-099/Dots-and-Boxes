from enum import auto
from random import randint

class Game:

    #Constants
    EMPTY = ' '
    DRAW = auto()
    #Using enum.auto() allows me to generate an inconsequential value for a draw
    VTCL = '|'
    HZTL = '--'
    AI = 'AI'
    EASY = 1
    MED = 3
    HARD = 5
    #These code constants (EASY-PFCT) are for the AI difficulty; how many layers (or plies) deep does the minimax algorithm go
    LEFT = 'l'
    RIGHT = 'r'
    UP = 'u'
    DOWN = 'd'
    # These last few code constants are used instead of literal constants wen checking box capture

    def __init__(self,dim,P1,P2,difficulty=None):
        self._P1 = P1
        self._P2 = P2
        self._dim = dim
        self._rowLines = [[Game.EMPTY for _ in range(self._dim-1)] for _ in range(self._dim)]
        self._colLines = [[Game.EMPTY for _ in range(self._dim)] for _ in range(self._dim-1)]
        #Using seperate 2D arrays for row and column lines allows clearer indexing for lines
        self._boxes = [[Game.EMPTY for _ in range(self._dim-1)] for _ in range(self._dim-1)]
        #Skill B -> Multi-dimensional arrays
        self._player = self._P1
        self._points = {self._P1:0, self._P2:0}
        #Skill B -> Dictionaries
        #Using a dictionary for points makes referencing easier than two separate variables
        self._difficulty = difficulty

    def getP1Name(self):
        return self._P1

    def getP2Name(self):
        return self._P2
    #The two above subroutines are getters for the names of the players

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
                sides.append(Game.RIGHT)
            if col > 0:
                sides.append(Game.LEFT)
        elif fr[1] == to[1]:
            self._rowLines[row][col] = Game.HZTL
            if row < self._dim-1:
                sides.append(Game.DOWN)
            if row > 0:
                sides.append(Game.UP)
        if len(sides) > 0:
            self.checkBox(row, col, sides)

    def checkBox(self, row, col, sides):
        #This is where whether a placed line forms a square
        switch = []
        for side in sides:
            if side == Game.RIGHT or side == Game.DOWN:
                if self._colLines[row][col] != Game.EMPTY and self._colLines[row][col+1] != Game.EMPTY and self._rowLines[row][col] != Game.EMPTY and self._rowLines[row+1][col] != Game.EMPTY:
                    #It checks if the required lines are filled
                    self._boxes[row][col] = self._player
                    self._points[self._player] += 1
                    switch.append(False)
                else:
                    switch.append(True)
            elif side == Game.LEFT:
                if self._colLines[row][col] != Game.EMPTY and self._colLines[row][col-1] != Game.EMPTY and self._rowLines[row][col-1] != Game.EMPTY and self._rowLines[row+1][col-1] != Game.EMPTY:
                    self._boxes[row][col-1] = self._player
                    self._points[self._player] += 1
                    switch.append(False)
                else:
                    switch.append(True)
            elif side == Game.UP:
                if self._colLines[row-1][col] != Game.EMPTY and self._colLines[row-1][col+1] != Game.EMPTY and self._rowLines[row][col] != Game.EMPTY and self._rowLines[row-1][col] != Game.EMPTY:
                    self._boxes[row-1][col] = self._player
                    self._points[self._player] += 1
                    switch.append(False)
                else:
                    switch.append(True)
        #Deciding whether to switch whose turn it is or not
        if len(switch) == 1:
            if switch[0]:
                self.switchTurn()
        else:
            if switch[0] and switch[-1]:
                self.switchTurn()

    def getScore(self, player):
        return self._points[player]

    def getDim(self):
        return self._dim

    def getPlayer(self):
        return self._player
    #The above 3 subroutines are getters for the specified value

    def isValid(self, fr, to):
        #To check if a move is valid for the AI
        try:
            return not self.occupied(fr,to)
        except IndexError:
            return False

    def occupied(self, fr, to):
        #This is where the UI class can check if a space is free
        try:
            row = min(to[1], fr[1])
            col = min(to[0], fr[0])
            if fr[0] == to[0]:
                return not self._colLines[row][col] == Game.EMPTY
            else:
                return not self._rowLines[row][col] == Game.EMPTY
        except IndexError:
            return True

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
        return self._boxes[coord[0]][coord[1]]

    def switchTurn(self):
        #Switching turns is used by many different classes and so I deemed it needed its own subroutine
        self._player = self._P1 if self._player == self._P2 else self._P2

    def getInfo(self):
        return [[list(i) for i in self._rowLines],[list(i) for i in self._colLines],self._player,{k:v for (k,v) in self._points.items()},self._dim,self._P1,self._P2]
        #Skill A -> List operations

    def ai(self):
        #The AI works out what to do
        if self._difficulty == Game.EASY:
            fr = [50,50]
            to = [50,50]
            while not self.isValid(fr,to):
                row = randint(0,self._dim)
                col = randint(0,self._dim)
                fr = [row,col]
                orientation = randint(1,2)
                if orientation == 1:
                    to = [row+1,col]
                else:
                    to = [row,col+1]
            return fr,to
        else:
            val, fr, to = self.__max(0,-100,100,self.getInfo())
            return fr,to

    def __max(self,plies,alpha,beta,info):
        #Trying to maximise the ai's score
        #Skill A -> Complex user-defined algorithms - minimax
        tG = tempGame(info)

        maxv = -100
        minv = 100
        pFr = None
        pTo = None

        if plies == self._difficulty:
            return tG.getScore(), 0, 0

        for row in range(self._dim):
            for col in range(self._dim):
                for orientation in [Game.VTCL,Game.HZTL]:
                    fr = [row,col]
                    to = [row+1,col] if orientation == Game.VTCL else [row,col+1]
                    if tG.isValid(fr,to):
                        tG.play(fr,to)
                        if tG.getPlayer() == Game.AI:
                            m, minFr, minTo = self.__max(plies+1,alpha,beta,tG.getInfo())
                            #Skill A -> Recursive algorithms
                            if m < minv:
                                minv = m
                                pFr = fr
                                pTo = to
                            if minv <= alpha:     
                                return minv, pFr, pTo

                            if minv < beta:
                                beta = minv
                        else:
                            m, minFr, minTo = self.__min(plies+1,alpha,beta,tG.getInfo())
                            if m > maxv:
                                maxv = m
                                pFr = fr
                                pTo = to

                            if maxv >= beta:
                                return maxv, pFr, pTo

                            if maxv > alpha:
                                alpha = maxv

        return maxv, pFr, pTo

    def __min(self,plies,alpha,beta,info):
        #Trying to minimise the player's score
        #Skill A -> Complex user-defined algorithms - minimax
        tG = tempGame(info)

        minv = 100
        maxv = -100
        qFr = None
        qTo = None

        if plies == self._difficulty:
            return tG.getScore(), 0, 0

        for row in range(self._dim):
            for col in range(self._dim):
                for orientation in [Game.VTCL,Game.HZTL]:
                    fr = [row,col]
                    to = [row+1,col] if orientation == Game.VTCL else [row,col+1]
                    if tG.isValid(fr,to):
                        tG.play(fr,to)
                        if tG.getPlayer() != Game.AI:
                            m, maxFr, maxTo = self.__min(plies+1,alpha,beta,tG.getInfo())
                            #Skill A -> Recursive algorithms
                            if m > maxv:
                                maxv = m
                                qFr = fr
                                qTo = to

                            if maxv >= beta:
                                return maxv, qFr, qTo

                            if maxv > alpha:
                                alpha = maxv
                        else:
                            m, maxFr, maxTo = self.__max(plies+1,alpha,beta,tG.getInfo())
                            if m < minv:
                                minv = m
                                qFr = fr
                                qTo = to
                            if minv <= alpha:     
                                return minv, qFr, qTo

                            if minv < beta:
                                beta = minv

        return minv, qFr, qTo


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


class tempGame(Game):
    #Skill A -> Complex use of OOP - inheritance
    MIN = 'min'
    MAX = 'max'

    def __init__(self, info):
        super(tempGame, self).__init__(info[4], info[5], info[6])
        #Skill A -> Complex use of OOP - composition
        self._rowLines = info[0]
        self._colLines = info[1]
        self._player = info[2]
        self._points = info[3]

    def getScore(self):
        return self._points[Game.AI] - self._points[self._P1] if self._player == self._P2 else self._points[Game.AI] - self._points[self._P2]
