from abc import ABC, abstractmethod
from Game import Game
#Skill A -> Files organised for direct access
from tkinter import Button, Tk, Toplevel, Frame, N,S,E,W,X,Y, LEFT,RIGHT, END, Scrollbar, Text, Message, Grid, StringVar, Label, OptionMenu

class Ui(ABC):
    @abstractmethod
    def run(self):
        raise NotImplementedError

class Gui(Ui):
    #Skill A -> Complex use of OOP - inheritance

    GUI = 'GUI'

    def __init__(self):
        #Setting up the main window
        self._gameWin = None
        root = Tk()
        root.title('Dots and Boxes')
        frame = Frame(root)
        frame.pack(fill=X)
        Button(frame,text='Help',command=self.helpCallback).pack(fill=X)
        Button(frame,text='Play Game',command=self.optionsWinSetup).pack(fill=X)
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
        #What happens when the help button is pressed
        helpWin = Toplevel(self._root)
        helpWin.title('Help')
        self._helpWin = helpWin
        Grid.rowconfigure(helpWin,0,weight=1)
        Grid.columnconfigure(helpWin,0,weight=1)
        frame = Frame(helpWin)
        frame.grid(row=0,column=0,sticky=N+S+E+W)

        l = Label(frame,text='Dots and Boxes is a two player game in which players take it in turns to play lines on a grid to make boxes.\nWhoever has captured the most boxes when all of the lines have been played is the winner.\n\nPress on the buttons between the dots to play a line.\nIf you capture a box, you get another turn.')
        l.grid(row=0,column=0,sticky=N+S+E+W)
        Grid.rowconfigure(frame,0,weight=1)
        Grid.columnconfigure(frame,0,weight=1)

        Button(helpWin, text='Dismiss', command=self._helpClose).grid(row=1,column=0)

    def optionsWinSetup(self):
        #Setting up the options window
        if self._gameWin:
            return
        optionsWin = Toplevel(self._root)
        optionsWin.title('Options')
        self._optionsWin = optionsWin
        Grid.rowconfigure(optionsWin,0,weight=1)
        Grid.columnconfigure(optionsWin,0,weight=1)
        frame = Frame(optionsWin)
        frame.grid(row=0,column=0,sticky=N+S+E+W)

        dims = [3,4,5,6,7,8,9]
        dim = StringVar()
        dim.set(dims[1])
        m = OptionMenu(frame, dim, *dims)
        m.grid(row=0,column=1,sticky=N+S+E+W)
        
        ais = ['None','Player 1', 'Player 2']
        ai = StringVar()
        ai.set(ais[0])
        m = OptionMenu(frame, ai, *ais)
        m.grid(row=1,column=1,sticky=N+S+E+W)

        Label(frame,text='Board dimension: ').grid(row=0,column=0,sticky=N+S+E+W)
        Label(frame,text='AI: ').grid(row=1,column=0,sticky=N+S+E+W)

        cmd = lambda : self.closeOptions(dim,ai)
        Button(optionsWin, text='Play', command=cmd).grid(row=2,column=0)
        Grid.rowconfigure(frame,0,weight=1)
        Grid.columnconfigure(frame,0,weight=1)

    def closeOptions(self,dim,ai):
        self._dim = int(dim.get())
        self._ai = ai.get()
        self._optionsWin.destroy()
        self.playCallback()


    def playCallback(self):
        #What happens when the play button is pressed
        if self._ai == 'None':
            self._game = Game(self._dim,'P1','P2')
        elif self._ai == 'Player 1':
            self._game = Game(self._dim,Game.AI,'P2')
        else:
            self._game = Game(self._dim,'P1',Game.AI)

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
        #Skill B -> multi-dimensional arrays


        for row in range(0,self._game.getDim()*2,2):
            for col in range(0,self._game.getDim()*2,2):
                #Putting all of the buttons and labels into the window
                try:
                    cmd = lambda r=row//2,c=col//2 : self.playRefresh(r,c,Game.VTCL)
                    self._colButtons[row//2][col//2] = Button(frame,command=cmd,height=10,width=5)
                    self._colButtons[row//2][col//2].grid(row=row+1,column=col if col == 0 else col,sticky=N+S+E+W)
                except IndexError:
                    pass

                try:
                    cmd = lambda r=row//2,c=col//2 : self.playRefresh(r,c,Game.HZTL)
                    self._rowButtons[row//2][col//2] = Button(frame,command=cmd,height=1,width=20)
                    self._rowButtons[row//2][col//2].grid(row=row,column=col+1,sticky=N+S+E+W)
                except IndexError:
                    pass

                l = Label(frame,text='.')
                l.config(font=('Courier',37))
                l.grid(row=row,column=col,sticky=N+S+E+W)
                
                try:
                    self._boxOwners[row//2][col//2] = StringVar()
                    self._boxOwners[row//2][col//2].set(self._game.boxOwner([row//2,col//2]))
                    l = Label(frame,textvariable=self._boxOwners[row//2][col//2])
                    l.config(font=('Courier',40))
                    l.grid(row=row+1,column=col+1,sticky=N+S+E+W)
                except IndexError:
                    pass

        for i in range(self._game.getDim()*2):
            Grid.rowconfigure(frame,i,weight=1)
            Grid.columnconfigure(frame,i,weight=1)

        Button(gameWin, text='Dismiss', command=self._gameClose).grid(row=1,column=0)

        self.pointWinSetup()

        if self._game.getPlayer() == Game.AI:
            self._console.insert(END,'AI\'s turn\nThinking...\n')
            fr, to = self._game.ai()
            if fr[0] == to[0]:
                self.playRefresh(fr[0],fr[1],Game.VTCL)
            else:
                self.playRefresh(fr[0],fr[1],Game.HZTL)


    def pointWinSetup(self):
        #Setting up the running total of points window
        pointsWin = Toplevel(self._root)
        pointsWin.title('Score')
        self._pointsWin = pointsWin
        Grid.rowconfigure(pointsWin,0,weight=1)
        Grid.columnconfigure(pointsWin,0,weight=1)
        frame = Frame(pointsWin)
        frame.grid(row=0,column=0,sticky=N+S+E+W)

        self._points = [None,None]

        self._points[0] = StringVar()
        self._points[0].set(f'{self._game.getP1Name()}: {self._game.getScore(self._game.getP1Name())}')
        self._points[1] = StringVar()
        self._points[1].set(f'{self._game.getP2Name()}: {self._game.getScore(self._game.getP2Name())}')
        l = Label(frame,textvariable=self._points[0])
        l.grid(row=1,column=0,sticky=N+S+E+W)
        l = Label(frame,textvariable=self._points[1])
        l.grid(row=2,column=0,sticky=N+S+E+W)

        self._turn = StringVar()
        self._turn.set(f'{self._game.getPlayer()}\'s turn')
        l = Label(frame,textvariable=self._turn)
        l.grid(row=0,column=0,sticky=N+S+E+W)

        

    def playRefresh(self,row,col,dir):
        #What happens when a line button is pressed
        if dir == Game.VTCL:
            if not self._game.occupied([col,row],[col,row+1]):
                self._game.play([col,row],[col,row+1])
                self._colButtons[row][col].configure(bg='black')
            else:
                self._console.insert(END,'Space already occupied, turn forfeited\n')
                self._game.switchTurn()
        else:
            if not self._game.occupied([col,row],[col+1,row]):
                self._game.play([col,row],[col+1,row])
                self._rowButtons[row][col].configure(bg='black')
            else:
                self._console.insert(END,'Space already occupied, turn forfeited\n')
                self._game.switchTurn()

        self._turn.set(f'{self._game.getPlayer()}\'s turn')
        self._points[0].set(f'{self._game.getP1Name()}: {self._game.getScore(self._game.getP1Name())}')
        self._points[1].set(f'{self._game.getP2Name()}: {self._game.getScore(self._game.getP2Name())}')

        for row in range(len(self._boxOwners)):
            for col in range(len(self._boxOwners[row])):
                self._boxOwners[row][col].set(self._game.boxOwner([row,col])) 

        if self._game.winner is not None:
            if self._game.winner == Game.DRAW:
                self._console.insert(END,'The game was a draw\n')
            else:
                self._console.insert(END,f'The winner was {self._game.winner}\n')
        
        if self._game.getPlayer() == Game.AI:
            self._console.insert(END,'AI\'s turn\nThinking...\n')
            fr, to = self._game.ai()
            if fr[0] == to[0]:
                self.playRefresh(fr[0],fr[1],Game.VTCL)
            else:
                self.playRefresh(fr[0],fr[1],Game.HZTL)
        
    def _gameClose(self):
        self._gameWin.destroy()
        self._pointsWin.destroy()

    def _helpClose(self):
        self._helpWin.destroy()

    #The above two subroutines are for closing windows when the dismiss button is pressed
                
    def run(self):
        self._root.mainloop()

class Terminal(Ui):
    #Skill A -> Complex use of OOP - inheritance

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
            while True:
                ai = input('Would you like an ai opponent (y/n)?: ').upper()
                if ai in ['Y','N']:
                    break
                print('Not y or n')
            if ai == 'Y':
                while True:
                    try:
                        choice = int(input('Would you like the AI to play player 1 or 2?: '))
                        if choice not in [1,2]:
                            print(f'There is no player {choice}')
                            continue
                        else:
                            if choice == 1:
                                self._game = Game(dim,'AI', 'P1', Game.HARD)
                            else:
                                self._game = Game(dim,'P1','AI', Game.HARD)
                            break
                    except ValueError:
                        print('Not a number')
                        continue
            else:
                self._game = Game(dim,'P1','P2')
            while not self._game.winner:
                print(self._game)
                if self._game.getPlayer() == Game.AI:
                    fr, to = self._game.ai()
                    self._game.play(fr,to)
                else:
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
