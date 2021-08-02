import random
from abc import ABCMeta, abstractmethod
from tkinter import Frame, Canvas, Tk
from delaunay_triangles import DelaunayTriangles
from libs import Color, DEFAULT_COLOR, Point


class Moderator(Frame, metaclass=ABCMeta):
    # I want to have roughly 600 points on a 1600x800 canvas.
    num_points_adjuster = 2048

    master: Tk
    width: int
    height: int
    canvas: Canvas
    delaunay_triangles: DelaunayTriangles

    def __init__(self, master: Tk, width: int, height: int
                 , num_points_adjuster: int = num_points_adjuster):
        super().__init__(master, width=width, height=height)
        self.master = master
        self.width = width
        self.height = height
        self.num_points_adjuster = num_points_adjuster
        self.pack()
        self.initialize_widgets()
        self.create_delaunay_triangles()

    def initialize_widgets(self):
        self.canvas = Canvas(self, width=self.width, height=self.height)
        self.canvas.pack()

    def create_delaunay_triangles(self):
        self.delaunay_triangles = DelaunayTriangles(self.width, self.height)
        num_points = int(self.width * self.height / self.num_points_adjuster)
        points = DelaunayTriangles.create_points_randomly(self.width, self.height, num_points)
        self.delaunay_triangles.triangulation(points)

    @abstractmethod
    def execute(self):
        pass


class DisplayModerator(Moderator):
    def __init__(self, master: Tk, width: int, height: int
                 , num_points_adjuster: int = Moderator.num_points_adjuster):
        super().__init__(master, width, height, num_points_adjuster=num_points_adjuster)

    def execute(self):
        # Fill color in each triangles
        colors = Color.get_all_colors()
        triangles = self.delaunay_triangles.triangles
        for triangle in triangles:
            color = random.choice(colors)
            triangle.color = color

        self.delaunay_triangles.draw(self.canvas)
        self.master.mainloop()


class IncreaseAnimationModerator(Moderator):
    def __init__(self, master: Tk, width: int, height: int
                 , num_points_adjuster: int = Moderator.num_points_adjuster * 2):
        super().__init__(master, width, height, num_points_adjuster=num_points_adjuster)

    triangle_queue: dict
    update_time_ms: int = 1000

    def execute(self):
        self.delaunay_triangles.create_triangle_adjacency_map()

        # Get all colors
        colors = Color.get_all_colors()

        # Find triangle with lowest coordinate
        lowest_triangle = self.delaunay_triangles.find_triangle_has_in_edge(Point(1, 1))
        lowest_triangle.color = random.choice(colors)

        # Initialize queue
        self.triangle_queue = dict()
        self.triangle_queue[lowest_triangle] = [None]

        # Draw and update
        self.delaunay_triangles.draw(self.canvas)
        self.after(self.update_time_ms, self.update)
        self.master.mainloop()

    def update(self):
        new_queue = dict()
        old_queue = self.triangle_queue

        for current_triangle, previous_triangles in old_queue.items():
            adjacent_triangles = self.delaunay_triangles \
                .get_adjacent_triangles(current_triangle)
            for adjacent_triangle in adjacent_triangles:
                if adjacent_triangle in previous_triangles:
                    continue
                adjacent_triangle.color = DEFAULT_COLOR \
                    if adjacent_triangle.color == current_triangle.color \
                    else current_triangle.color
                if adjacent_triangle in new_queue:
                    new_queue[adjacent_triangle].append(current_triangle)
                else:
                    new_queue[adjacent_triangle] = [current_triangle]
            current_triangle.color = DEFAULT_COLOR

        tmp_queue = dict()
        for triangle, previous_triangles in new_queue.items():
            if triangle.color != DEFAULT_COLOR:
                tmp_queue[triangle] = previous_triangles

        new_queue = tmp_queue
        self.triangle_queue = new_queue
        self.delaunay_triangles.draw(self.canvas)
        self.after(self.update_time_ms, self.update)


class MoveAnimationModerator(Moderator):
    num_move_points: int

    def __init__(self, master: Tk, width: int, height: int
                 , num_points_adjuster: int = Moderator.num_points_adjuster * 2
                 , num_move_triangles: int = 1):
        self.num_move_triangles = num_move_triangles
        super().__init__(master, width, height, num_points_adjuster=num_points_adjuster)

    triangle_queue: dict
    update_time_ms: int = 1000

    def execute(self):
        self.delaunay_triangles.create_triangle_adjacency_map()

        # Get all colors
        colors = Color.get_all_colors()

        # Initialize queue
        self.triangle_queue = dict()

        # Choose triangle randomly and enqueue
        triangles = self.delaunay_triangles.triangles
        for i in range(self.num_move_triangles):
            triangle = random.choice(triangles)
            triangle.color = random.choice(colors)
            self.triangle_queue[triangle] = None

        # Draw and update
        self.delaunay_triangles.draw(self.canvas)
        self.after(self.update_time_ms, self.update)
        self.master.mainloop()

    def update(self):
        new_queue = dict()
        old_queue = self.triangle_queue

        for current_triangle, previous in old_queue.items():
            adjacent_triangles = list(self.delaunay_triangles \
                                      .get_adjacent_triangles(current_triangle))
            if previous in adjacent_triangles:
                adjacent_triangles.remove(previous)

            iterator = list(adjacent_triangles)
            for adjacent_triangle in iterator:
                if adjacent_triangle.color != DEFAULT_COLOR:
                    adjacent_triangles.remove(adjacent_triangle)

            if len(adjacent_triangles) == 0:
                continue

            next_move = random.choice(adjacent_triangles)
            next_move.color = current_triangle.color
            new_queue[next_move] = current_triangle

        self.triangle_queue = new_queue
        self.delaunay_triangles.draw(self.canvas)
        self.after(self.update_time_ms, self.update)
