from tkinter import *
from .mission import MissionCreator, Mission, DelaunayMissionCreator


GAME_TITLE: str = "Shapes And Colors"
GUI_WIDTH: int = 800
GUI_HEIGHT: int = 400
GUI_SIZE: str = f"{GUI_WIDTH}x{GUI_HEIGHT}"


if __name__ == '__main__':
    root: Tk = Tk()
    root.title(GAME_TITLE)
    root.geometry(GUI_SIZE)

    canvas: Canvas = Canvas(root, width=GUI_WIDTH, height=GUI_HEIGHT)
    canvas.pack()

    # Create mission and draw
    mission_creator: MissionCreator = DelaunayMissionCreator()
    mission: Mission = mission_creator.create(canvas)

    # start game
    mission.start()

    root.main_loop()

