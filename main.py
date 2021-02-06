from UI import Gui, Terminal
#Skill A -> Files organised for direct access
from sys import argv

def usage():
    #When calling the program, g or t is inputted alongside the program call
    print(f"""
Usage: {argv[0]} [g | t]
g : play with the GUI
t : play with the Terminal""")
    quit()

if __name__ == "__main__":
    if len(argv) != 2:
        usage()
    elif argv[1] == 'g':
        ui = Gui()
    elif argv[1] == 't':
        ui = Terminal()
    else:
        usage()

    ui.run()
