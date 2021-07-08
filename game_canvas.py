from tkinter import *
from tkinter.ttk import *
from libs import *


# compute, store data, draw canvas
class GameCanvas(Canvas):
    # create()
    # clicked()
    # isComplete()
    # serialize
    # deserialize
    # update screen

    def __init__(self, master = None, difficulty = None, *args, **kwargs):
        super().__init__(master, background="green", *args, **kwargs)
        self.bind("<ButtonPress-1>", self.on_click)

    def on_click(self, event):
        x = event.x
        y = event.y
        pass

    def create_mission(self):
        pass

