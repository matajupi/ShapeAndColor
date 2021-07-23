import sys
sys.path.append("../")
from tkinter import *
from delaunay_triangles import *


WIDTH = 1600
HEIGHT = 800
NUM_POINTS = 600


if __name__ == "__main__":
    root = Tk()
    root.geometry(f"{WIDTH}x{HEIGHT}")
    root.title("Delaunay triangles")

    canvas = Canvas(root, width=WIDTH, height=HEIGHT)
    canvas.pack()
    delaunay_triangles = DelaunayTriangles(WIDTH, HEIGHT)
    points = DelaunayTriangles \
    .create_points_randomly(WIDTH, HEIGHT, NUM_POINTS)
    delaunay_triangles.triangulation(points)
    delaunay_triangles.draw(canvas)

    root.mainloop()

