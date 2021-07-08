from tkinter import *
from tkinter.ttk import *
from main import game_frame

class MainFrame(Frame):
    def __init__(self, master: Tk = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        pass


class GameFrame(Frame):
    # property GameBoard
    # event click
    # update time
    # serialize
    # past_result
    # deserialize
    # choose difficulty
    # save
    # restart


    def __init__(self, master: Tk = None):
        super().__init__(master)
        self.master = master
        self.master.title(self.GAME_TITLE)
        self.pack()

    def start(self):
        self.create_main_widgets()


    def create_main_widgets(self):
        pass

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()
