import sys
sys.path.append("../")
from tkinter import *
from moderators import DisplayModerator


GUI_WIDTH = 1600
GUI_HEIGHT = 800
GUI_TITLE = "Delaunay triangles"


if __name__ == "__main__":
    root = Tk()
    root.title(GUI_TITLE)
    moderator = DisplayModerator(root, GUI_WIDTH, GUI_HEIGHT)
    moderator.execute()

