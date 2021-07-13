from tkinter import *
from shape_and_color.delaunay_triangles import *


GUI_TITLE = "Test delaunay triangles"
GUI_WIDTH = 800
GUI_HEIGHT = 400
GUI_SIZE = f"{GUI_WIDTH}x{GUI_HEIGHT}"

NUM_OF_POINTS = 300


def test_get_huge_triangle(canvas: Canvas):
    delaunay = DelaunayTriangles(100, 100)
    huge_triangle = delaunay.get_huge_triangle()
    for i in range(len(huge_triangle.vertices)):
        vertex = huge_triangle.vertices[i]
        new_vertex = Point(vertex.x + 100, vertex.y + 100)
        huge_triangle.vertices[i] = new_vertex
    huge_triangle.draw(canvas)
    return delaunay, huge_triangle


def test_get_circumscribed_circle_of_triangle(canvas: Canvas):
    delaunay, huge_triangle = test_get_huge_triangle(canvas)
    circle = delaunay.get_circumscribed_circle_of_triangle(huge_triangle)
    circle.draw(canvas)


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
