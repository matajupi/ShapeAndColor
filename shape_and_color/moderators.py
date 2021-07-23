import random
from abc import *
from tkinter import *
from delaunay_triangles import *
from libs import *


class Moderator(Frame, metaclass=ABCMeta):
    COLOR_BEGIN = (64, 64, 64)
    COLOR_DELTA = 15
    # I want to have roughly 600 points on a 1600x800 canvas.
    NUM_POINTS_ADJUSTER = 2048

    master: Tk
    width: int
    height: int
    update_time: int

    def __init__(self, master: Tk, width: int, height: int):
        super().__init__(master, width=width, height=height)
        self.master = master
        self.width = width
        self.height = height
        self.initialize_widgets()
        self.pack()

    @abstractmethod
    def initialize_widgets(self):
        pass

    def execute(self):
        self.initialize()
        self.after(self.update_time, self.update)
        self.master.mainloop()

    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def update(self):
        pass

    def create_color_list(self, color_begin: tuple, delta: int) -> list:
        colors = list()
        for r in range(color_begin[0], 256, delta):
            for g in range(color_begin[1], 256, delta):
                for b in range(color_begin[2], 256, delta):
                    color = Color(r, g, b)
                    colors.append(color)
        return colors


class DisplayModerator(Moderator):
    canvas: Canvas
    delaunay_triangles: DelaunayTriangles

    def __init__(self, master: Tk, width: int, height: int):
        super().__init__(master, width, height)
        self.update_time = 0

    def initialize_widgets(self):
        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

    def initialize(self):
        # Create delaunay triangles
        self.delaunay_triangles = DelaunayTriangles(self.width, self.height)
        num_points = int((self.width * self.height) / self.NUM_POINTS_ADJUSTER)
        points = DelaunayTriangles.create_points_randomly(self.width, self.height, num_points)
        self.delaunay_triangles.triangulation(points)

        # Fill color in each triangles
        colors = self.create_color_list(self.COLOR_BEGIN, self.COLOR_DELTA)
        triangles = self.delaunay_triangles.triangles
        for triangle in triangles:
            color = random.choice(colors)
            triangle.color = color

        # Display
        self.delaunay_triangles.draw(self.canvas)

    def update(self):
        pass


class AnimationModerator(Moderator):
    def __init__(self, master: Tk, width: int, height: int):
        super().__init__(master, width, height)
        self.update_time = 500

    def initialize_widgets(self):
        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

    def initialize(self):
        # Create delaunay triangles
        self.delaunay_triangles = DelaunayTriangles(self.width, self.height)
        num_points = int((self.width * self.height) / self.NUM_POINTS_ADJUSTER)
        points = DelaunayTriangles.create_points_randomly(self.width, self.height, num_points)
        self.delaunay_triangles.triangulation(points)

    def update(self):
        pass

