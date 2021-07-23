import random
from tkinter import *
from libs import *
from polygon_mapper import *


# "MissionCreator" that creates the mission and "Mission" that represents the mission are separated.
# "Mission" also holds run-time information.
class Mission:
    canvas: Canvas

    width: int
    height: int

    polygon_map: list
    polygons: list

    polygon_color_table: dict

    time: int = 0

    COLOR_BEGIN = (64, 64, 64)
    COLOR_DELTA = 32

    def __init__(self, canvas: Canvas, polygons: list, width: int, height: int):
        self.canvas: Canvas = canvas
        self.initialize_canvas()

        self.polygons = polygons
        self.width = width
        self.height = height

        # self.polygon_map = self.create_polygon_map(polygons, width, height)

        colors = self.create_color_list(self.COLOR_BEGIN, self.COLOR_DELTA)
        self.polygon_color_table = self.create_polygon_color_table(self.polygons, colors)

    def initialize_canvas(self):
        self.canvas.bind("<ButtonRelease-1>", self.on_left_button_click)

    def on_left_button_click(self, event):
        # debug
        print(event.x, event.y)
        # TODO: Implement

    def create_polygon_map(self, polygons: list, width: int, height: int) -> list:
        mapper = PolygonMapper(width, height)
        polygon_map = mapper.map(polygons)
        return polygon_map

    def create_polygon_color_table(self, polygons: list, colors: set) -> dict:
        table = dict()
        for polygon in polygons:
            color = random.choice(list(colors))
            # colors.remove(color)
            table[polygon] = color
        return table

    def create_color_list(self, begin: tuple, delta: int) -> set:
        colors = set()
        for r in range(begin[0], 256, delta):
            for g in range(begin[1], 256, delta):
                for b in range(begin[2], 256, delta):
                    color = (r, g, b)
                    colors.add(color)
        return colors

    def start(self):
        self.draw()
        # TODO: Implement

    def draw(self):
        for polygon in self.polygons:
            color = self.polygon_color_table[polygon]
            hex_color = f"#{format(color[0], 'x')}{format(color[1], 'x')}{format(color[2], 'x')}"
            vertices = self.get_sorted_vertices(polygon)
            self.canvas.create_polygon(*vertices, fill=hex_color)

    def get_sorted_vertices(self, polygon: Polygon) -> list:
        sides = polygon.sides
        point_map = dict()
        for side in sides:
            if side.point1 in point_map:
                point_map[side.point1].append(side)
            else:
                point_map[side.point1] = [side]
            if side.point2 in point_map:
                point_map[side.point2].append(side)
            else:
                point_map[side.point2] = [side]

        vertices = list()
        vertices_set = set(polygon.vertices)
        side = sides[0]
        while True:
            if side.point1 in vertices_set:
                vertices.append(side.point1.x)
                vertices.append(side.point1.y)
                vertices_set.remove(side.point1)
            if side.point2 in vertices_set:
                vertices.append(side.point2.x)
                vertices.append(side.point2.y)
                vertices_set.remove(side.point2)

            point_map[side.point1].remove(side)
            point_map[side.point2].remove(side)

            if len(point_map[side.point2]) > 0:
                side = point_map[side.point2][0]
            else:
                break

        return vertices

