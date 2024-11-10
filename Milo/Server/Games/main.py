from tkinter import *
from Engine import *
from games import *





root = Tk()
GameWindow = Engine(master=root, x=0,y=20, gameClass=GettingOverIt)
root.geometry("1200x1200")
root.mainloop()