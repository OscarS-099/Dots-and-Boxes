from abc import ABC, abstractmethod
from Game import Game
from tkinter import Button, Tk, Toplevel, Frame, N,S,E,W,X,Y, LEFT,RIGHT, END, Scrollbar, Text, Message, Grid, StringVar, Label

class Ui(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError

class Gui(Ui):
    def __init__(self):
        self._gameWin = None
        root = Tk()
        root.title('Dots and Boxes')
        frame = Frame(root)
        frame.pack(fill=X)
        Button(frame,text='Help',command=self.helpCallback).pack(fill=X)
        Button(frame,text='Play Game',command=self.playCallback).pack(fill=X)
        Button(frame,text='Quit',command=root.quit).pack(fill=X)
        console = Text(frame, height=4, width=50)
        scroll = Scrollbar(frame)
        scroll.pack(side=RIGHT, fill=Y)
        console.pack(side=LEFT, fill=Y)
        scroll.config(command=console.yview)
        console.config(yscrollcommand=scroll.set)
        self._console = console
        self._root = root

    def helpCallback(self):
        pass

    def playCallback(self):
        if self._gameWin:
            return
        dim = 4
        self._game = Game(dim,'P1','P2')
        self._finished = False
        gameWin = Toplevel(self._root)
        gameWin.title('Game')
        self._gameWin = gameWin
        Grid.rowconfigure(gameWin,0,weight=1)
        Grid.columnconfigure(gameWin,0,weight=1)
        frame = Frame(gameWin)
        frame.grid(row=0,column=0,sticky=N+S+E+W)

        self._rowButtons = [[Game.EMPTY for _ in range(self._game.getDim()-1)] for _ in range(self._game.getDim())]
        self._colButtons = [[Game.EMPTY for _ in range(self._game.getDim())] for _ in range(self._game.getDim()-1)]
        self._boxOwners = [[Game.EMPTY for _ in range(self._game.getDim()-1)] for _ in range(self._game.getDim()-1)]

        for row in range(0,self._game.getDim()*2,2):
            for col in range(0,self._game.getDim()*2,2):
                try:
                    b = StringVar()
                    b.set(self._game.at([col//2,row//2],[col//2,row//2+1]))
                    cmd = lambda r=row//2,c=col//2 : self.playRefresh(r,c,'vtcl')
                    Button(frame,textvariable=b,command=cmd).grid(row=row+1,column=col if col == 0 else col,sticky=N+S+E+W)
                    self._colButtons[row//2][col//2] = b
                except IndexError:
                    pass

                try:
                    b = StringVar()
                    b.set(self._game.at([col//2,row//2],[col//2+1,row//2]))
                    cmd = lambda r=row//2,c=col//2 : self.playRefresh(r,c,'hztl')
                    Button(frame,textvariable=b,command=cmd).grid(row=row,column=col+1,sticky=N+S+E+W)
                    self._rowButtons[row//2][col//2] = b
                except IndexError:
                    pass

                l = Label(frame,text='.')
                l.config(font=('Courier',44))
                l.grid(row=row,column=col,sticky=N+S+E+W)
                
                try:
                    self._boxOwners[row//2][col//2] = StringVar()
                    self._boxOwners[row//2][col//2].set(self._game.boxOwner([row//2,col//2]))
                    l = Label(frame,textvariable=self._boxOwners[row//2][col//2])
                    l.grid(row=row+1,column=col+1,sticky=N+S+E+W)
                except IndexError:
                    pass

        for i in range(self._game.getDim()*2):
            Grid.rowconfigure(frame,i,weight=1)
            Grid.columnconfigure(frame,i,weight=1)

        Button(gameWin, text='Dismiss', command=self._gameClose).grid(row=1,column=0)

    def playRefresh(self,row,col,dir):
        if dir == 'vtcl':
            if not self._game.occupied([col,row],[col,row+1]):
                self._game.play([col,row],[col,row+1])
                text = self._game.at([col,row],[col,row+1])
                self._colButtons[row][col].set(text)
            else:
                self._console.insert(END,'Space already occupied\n')
        else:
            if not self._game.occupied([col,row],[col+1,row]):
                self._game.play([col,row],[col+1,row])
                text = self._game.at([col,row],[col+1,row])
                self._rowButtons[row][col].set(text)
            else:
                self._console.insert(END,'Space already occupied\n')

        for row in range(len(self._boxOwners)):
            for col in range(len(self._boxOwners[row])):
                self._boxOwners[row][col].set(self._game.boxOwner([row,col])) 

        if self._game.winner is not None:
            if self._game.winner == Game.DRAW:
                self._console.insert(END,'The game was a draw\n')
            else:
                self._console.insert(END,f'The winner was {self._game.winner}\n')
        
    def _gameClose(self):
        self._gameWin.destroy()
                
    def run(self):
        self._root.mainloop()

class Terminal(Ui):
    def __init__(self):
        self._p1Score = 0
        self._p2Score = 0

    def run(self):
        again = 'Y'
        while again == 'Y':
            dim = 12
            while dim < 3 or dim > 10:
                #Taking and validating input for dimension is in range
                try:
                    dim = int(input('Enter the dimension of the board (between 3 and 10 inclusive): '))
                except ValueError:
                    print('Input isn\'t an integer')
                    continue
            self._game = Game(dim,'P1','P2')
            while not self._game.winner:
                print(self._game)
                while True:
                    #Inputting line
                    fr = input('Enter line start coordinates in the form col,row: ').split(',')
                    to = input('Enter line end coordinates in the form col,row: ').split(',')
                    #Validating input
                    try:
                        for i in range(2):
                            #Converting input to integers
                            fr[i] = int(fr[i])-1
                            to[i] = int(to[i])-1
                            if fr[i] > self._game.getDim() or fr[i] < 0 or to[i] > self._game.getDim() or to[i] < 0:
                                print('Input is not withing board dimensions')
                                continue
                    except ValueError:
                        print('One or more of the inputs weren\'t integers')
                        continue
                    if abs(fr[0]-to[0]) > 1 or abs(to[1]-fr[1]) > 1:
                        print('The line is too long; it should span between two adjacent dots')
                        continue
                    if self._game.occupied(fr,to):
                        print('There is already a line there')
                        continue
                    break
                self._game.play(fr,to)
            print(self._game)
            #If the game is won, print out the victory message
            if self._game.winner != Game.DRAW:
                print(f'{self._game.winner} won')
                print(f'The score was: {self._game.getP1Name()} - {self._game.getScore(self._game.getP1Name())}, {self._game.getP2Name()} - {self._game.getScore(self._game.getP2Name())}')
                if self._game.winner == self._game.getP1Name():
                    self._p1Score += 1
                else:
                    self._p2Score += 1
                print(f'{self._game.getP1Name()} has won {self._p1Score} games, and {self._game.getP2Name()} has won {self._p2Score} games')
            else:
                print('It\'s a draw')
            while True:
                #Checking if they'd like a rematch
                again = input('Would you like to play again (y/n)? ')
                try:
                    again = again.upper()
                    if again != 'Y' and again != 'N':
                        print('Not y or n')
                        continue
                except:
                    print('Not a letter')
                    continue
                break

if __name__ == '__main__':
    # For unit testing
    ui = Gui()
    ui.run()