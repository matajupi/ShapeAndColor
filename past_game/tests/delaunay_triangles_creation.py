from tkinter import *
import sys
sys.path.append("..")
from delaunay_triangles import *


GUI_TITLE = "Test delaunay triangles"
GUI_WIDTH = 1200
GUI_HEIGHT = 600
GUI_SIZE = f"{GUI_WIDTH}x{GUI_HEIGHT}"

NUM_OF_POINTS = 300


def test_comprehensive(canvas: Canvas):
    delaunay = DelaunayTriangles(GUI_WIDTH, GUI_HEIGHT)
    points = create_points_randomly(GUI_WIDTH, GUI_HEIGHT, NUM_OF_POINTS)
    delaunay.triangulation(points)
    delaunay.draw(canvas)


if __name__ == "__main__":
    root = Tk()
    root.title(GUI_TITLE)
    root.geometry(GUI_SIZE)

    main_canvas = Canvas(master=root, width=GUI_WIDTH, height=GUI_HEIGHT)
    main_canvas.pack()

    # test_get_circumscribed_circle_of_triangle(main_canvas)
    test_comprehensive(main_canvas)

    root.mainloop()
