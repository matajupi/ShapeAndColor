"""
Libraries for creating a mission.
"""

import math
from abc import ABC, abstractmethod
from tkinter import Canvas


class Drawable(ABC):
    @abstractmethod
    def draw(self, canvas: Canvas):
        pass


class Color:
    COLOR_BEGIN = (64, 64, 64)
    COLOR_DELTA = 15

    __red: int
    __green: int
    __blue: int

    @property
    def red(self):
        return self.__red

    @property
    def green(self):
        return self.__green

    @property
    def blue(self):
        return self.__blue

    @property
    def hex(self):
        color_hex = "#"
        color_hex += hex(self.red)[2:]
        color_hex += hex(self.green)[2:]
        color_hex += hex(self.blue)[2:]
        return color_hex

    def __init__(self, red: int, green: int, blue: int):
        red = max(red, 0)
        red = min(red, 255)
        self.__red = red

        green = max(green, 0)
        green = min(green, 255)
        self.__green = green

        blue = max(blue, 0)
        blue = min(blue, 255)
        self.__blue = blue

    def __eq__(self, other):
        return self.red == other.red and self.green == other.green and self.blue == other.blue

    _all_colors: list = list()

    @classmethod
    def get_all_colors(cls) -> list:
        if cls._all_colors:
            return cls._all_colors
        color_begin = Color.COLOR_BEGIN
        color_delta = Color.COLOR_DELTA
        colors = list()
        for r in range(color_begin[0], 256, color_delta):
            for g in range(color_begin[1], 256, color_delta):
                for b in range(color_begin[2], 256, color_delta):
                    color = Color(r, g, b)
                    colors.append(color)
        cls._all_colors = colors
        return colors


DEFAULT_COLOR = Color(0xff, 0xff, 0xff)


class Point:
    __x: float
    __y: float

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    def __eq__(self, other):
        # "isinstance" of "type" function is very heavy.
        # if type(other) == Point:
        #     return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
        # return False
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((round(self.x), round(self.y)))

    def distance(self, other) -> float:
        """ Compute euclidean distance between 2 points """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class Triangle(Drawable):
    __points: list
    __color: Color

    @property
    def points(self):
        return self.__points

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color: Color):
        self.__color = color

    def __init__(self, p1: Point, p2: Point, p3: Point, color: Color = DEFAULT_COLOR):
        self.__points = [p1, p2, p3]
        self.__color = color

    def __eq__(self, other):
        # "isinstance" of "type" function is very heavy.
        # if type(other) != Point:
        #     return False

        if other is None:
            return False

        other_points = list(other.points)
        for point in self.points:
            if point in other_points:
                other_points.remove(point)
                continue
            return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        """
        Sort the hash values of all points and pass them to the hash fuction.
        """
        hashes = list()
        for point in self.points:
            hashes.append(point.__hash__())
        hashes.sort()
        return hash(tuple(hashes))

    def has_common_sides(self, triangle) -> bool:
        common_point_count = 0
        for point in self.points:
            if point in triangle.points:
                common_point_count += 1
        if common_point_count >= 2:
            return True
        return False

    def has_common_points(self, triangle) -> bool:
        for point in self.points:
            if point in triangle.points:
                return True
        return False

    def draw(self, canvas: Canvas):
        points = []
        for point in self.points:
            points.append(point.x)
            points.append(point.y)

        color_hex = self.color.hex
        canvas.create_polygon(points, fill=color_hex, outline="#000")


class Circle(Drawable):
    __center: Point
    __radius: float
    __color: Color

    @property
    def center(self):
        return self.__center

    @property
    def radius(self):
        return self.__radius

    @property
    def color(self):
        return self.__color

    def __init__(self, center: Point, radius: float, color: Color = DEFAULT_COLOR):
        self.__center = center
        self.__radius = radius
        self.__color = color

    def draw(self, canvas: Canvas):
        """
        Coordinates of the upper left vertex of a square
        circumscribing a circle.
        """
        x1 = self.center.x - self.radius
        y1 = self.center.y - self.radius
        """
        Coordinates of the upper right vertex of a square
        circumscribing a circle.
        """
        x2 = self.center.x + self.radius
        y2 = self.center.y + self.radius

        color_hex = self.color.hex
        canvas.create_oval(x1, y1, x2, y2, fill=color_hex, outline="#000")
