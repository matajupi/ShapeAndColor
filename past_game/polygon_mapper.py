import numpy as np
from libs import *
import sys

sys.setrecursionlimit(10 ** 9)

class PolygonMapper:
    polygon_map: list
    polygons: list
    SEPARATE_IDENTIFIER = 1
    width: int
    height: int

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def map(self, polygons: list) -> list:
        self.polygons = polygons
        self.polygon_map = [[None] * self.width for i in range(self.height)]

        self.create_separator()
        # TODO: I can't understand why it doesn't work.
        self.fill_polygons()

        return self.polygon_map

    def fill_polygons(self):
        for polygon in self.polygons:
            point = polygon.contains_point
            self.fill_polygons_helper(int(point.y), int(point.x), polygon)

    counter = 0

    def fill_polygons_helper(self, row: int, column: int, polygon: Polygon):
        self.counter += 1
        print(self.counter)
        self.polygon_map[row][column] = polygon
        next_rows = [1, 0, -1, 0]
        next_columns = [0, 1, 0, -1]
        for i in range(4):
            next_row = row + next_rows[i]
            next_column = column + next_columns[i]

            is_range_out = next_row < 0 or next_row >= self.height or next_column < 0 or next_column >= self.width
            if is_range_out or isinstance(self.polygon_map[next_row][next_column], int) or isinstance(self.polygon_map[next_row][next_column], Polygon):
                continue

            self.fill_polygons_helper(next_row, next_column, polygon)

    def create_separator(self):
        for polygon in self.polygons:
            sides = polygon.sides
            for side in sides:
                v1 = side.point1
                v2 = side.point2

                dx = abs(v1.x - v2.x)
                dy = abs(v1.y - v2.y)

                f = self.function_creator(dx, dy, v1.x, v1.y)

                sx = min(v1.x, v2.x)
                gx = min(v1.x, v2.x)

                for x in range(sx, gx + 1):
                    y = f(x)
                    if y < 0 or y >= self.height:
                        continue
                    self.polygon_map[int(y)][int(x)] = self.SEPARATE_IDENTIFIER

                f = self.function_creator(dx, dy, v1.x, v1.y, inverse=True)

                sy = min(v1.y, v2.y)
                gy = max(v1.y, v2.y)

                for y in range(sy, gy + 1):
                    x = f(y)
                    if x < 0 or x >= self.width:
                        continue
                    self.polygon_map[int(y)][int(x)] = self.SEPARATE_IDENTIFIER

    def function_creator(self, dx: int, dy: int, x1: int, y1: int, inverse=False):
        if inverse:
            if dy == 0:
                return lambda y: -1
            return lambda y: (dx / dy) * (y - y1) + x1
        if dx == 0:
            return lambda x: -1
        return lambda x: (dy / dx) * (x - x1) + y1

