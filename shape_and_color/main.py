import sys
from tkinter import *
from moderators import *


GUI_WIDTH = 1600
GUI_HEIGHT = 800
GUI_TITLE = "Delaunay triangles"


if __name__ == "__main__":
    # Create window
    root = Tk()
    root.title(GUI_TITLE)

    # Pause commandline arguments and create moderator
    moderator: Moderator
    args = sys.argv
    if len(args) == 2 and args[1] == "animation":
        moderator = AnimationModerator(root, GUI_WIDTH, GUI_HEIGHT)
    else:
        moderator = DisplayModerator(root, GUI_WIDTH, GUI_HEIGHT)

    # Execute
    moderator.execute()

