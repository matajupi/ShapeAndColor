"""
Libraries for creating a mission.
"""

import math
from abc import *
from tkinter import Canvas


class Drawable(ABC):
    @abstractmethod
    def draw(self, canvas: Canvas):
        pass


class Color:
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
        # "isinstance" of "type" function is very hevy.
        #if type(other) == Point:
        #    return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
        #return False
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

    @points.setter
    def points(self, points: list):
        if len(points) != 3:
            raise Exception("List length must be 3.")
        # "isinstance" of "type" function is very hevy.
        #for point in points:
        #    if type(point) == Point:
        #        continue
        #    raise TypeError("List items must be type of Point.")
        self.__points = points

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color: Color):
        self.__color = color

    def __init__(self, p1: Point, p2: Point, p3: Point, color: Color=Color(0xff, 0xff, 0xff)):
        self.points = [p1, p2, p3]
        self.__color = color

    def __eq__(self, other):
        # "isinstance" of "type" function is very hevy.
        #if type(other) != Point:
        #    return False

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

    def __init__(self, center: Point, radius: float, color: Color=Color(0xff, 0xff, 0xff)):
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

