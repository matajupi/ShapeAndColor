import sys
from tkinter import Tk
from moderators import Moderator, IncreaseAnimationModerator, DisplayModerator, MoveAnimationModerator


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
    if len(args) >= 2:
        moderator_type = args[1]
        if moderator_type == "increase":
            moderator = IncreaseAnimationModerator(root, GUI_WIDTH, GUI_HEIGHT)
        elif moderator_type == "move":
            num_move_triangles = int(args[2]) if len(args) >= 3 else 1
            moderator = MoveAnimationModerator(root, GUI_WIDTH, GUI_HEIGHT
                                               , num_move_triangles=num_move_triangles)
        elif moderator_type == "display":
            moderator = DisplayModerator(root, GUI_WIDTH, GUI_HEIGHT)
        else:
            print("Command line arguments: [increase | move | display]? [num_move_triangles: int]?")
            exit(0)
    else:
        moderator = DisplayModerator(root, GUI_WIDTH, GUI_HEIGHT)

    # Execute
    moderator.execute()

