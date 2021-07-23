from tkinter import *
from mission import *
from mission_creator import *


GAME_TITLE: str = "Shapes And Colors"
GUI_WIDTH: int = 1600
GUI_HEIGHT: int = 800
GUI_SIZE: str = f"{GUI_WIDTH}x{GUI_HEIGHT}"
NUM_OF_POINTS: int = 600


if __name__ == '__main__':
    root: Tk = Tk()
    root.title(GAME_TITLE)
    root.geometry(GUI_SIZE)

    canvas: Canvas = Canvas(root, width=GUI_WIDTH, height=GUI_HEIGHT)
    canvas.pack()

    # Create mission and draw
    mission_creator: MissionCreator = DelaunayMissionCreator()
    mission: Mission = mission_creator.create(canvas, GUI_WIDTH, GUI_HEIGHT, NUM_OF_POINTS)

    # start game
    mission.start()

    root.mainloop()

