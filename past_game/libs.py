"""
Libraries for creating a mission.
"""

import math
from tkinter import Canvas


# order: constant_variable(static) field property constructor destructor abstract override method static_variable static_method
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
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((round(self.x), round(self.y)))

    def distance(self, other) -> float:
        """ Compute distance between 2 points """
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)


class UndirectedLineSegment:
    __point1: Point
    __point2: Point

    @property
    def points(self):
        return [self.__point1, self.__point2]

    @property
    def point1(self):
        return self.__point1

    @property
    def point2(self):
        return self.__point2

    @property
    def length(self):
        return self.point1.distance(self.point2)

    def __init__(self, point1, point2):
        self.__point1 = point1
        self.__point2 = point2

    def __eq__(self, other):
        # Points must be strored in list because of duplicate
        points = [self.point1, self.point2]
        other_points = [other.point1, other.point2]
        for point in other_points:
            if point in points:
                points.remove(point)
            else:
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        hashes = [self.point1.__hash__(), self.point2.__hash__()]
        hashes.sort()
        return hash(tuple(hashes))


class Polygon:
    # Store in the order of the points of the figure.
    __sides: tuple
    __vertices: tuple
    __area: float
    __contains_point: Point

    @property
    def sides(self):
        return self.__sides

    @property
    def vertices(self):
        return self.__vertices

    @property
    def vertex_quantity(self):
        return len(self.sides)

    @property
    def area(self):
        return self.__area

    @property
    def contains_point(self):
        return self.__contains_point

    def __init__(self, sides: tuple, area: int=-1, contains_point: Point=Point(-1, -1)):
        self.__sides = sides

        vertices_set = set()
        for side in sides:
            vertices_set.add(side.point1)
            vertices_set.add(side.point2)
        self.__vertices = tuple(vertices_set)

        if area < 0 and self.vertex_quantity == 3:
            area = self.compute_triangle_area(self.sides)
        self.__area = area

        if contains_point == Point(-1, -1) and self.vertex_quantity == 3:
            contains_point = self.compute_triangle_gravity_center(self.vertices)
        self.__contains_point = contains_point

    def __eq__(self, other):
        """ Since hash table is used, the amount of computation is O(n). """
        if type(other) != Polygon:
            return False
        dictionary = dict()
        for side in self.sides:
            if side in dictionary:
                dictionary[side] += 1
            else:
                dictionary[side] = 1

        for side in other.sides:
            if side in dictionary:
                dictionary[side] -= 1
            else:
                return False

        for k in dictionary:
            if dictionary[k] != 0:
                return False

        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        """  """
        """ 
        Algorithm:
        Sorted Hash values for all sides and passed through the Hash function.
        """
        hashes = list()
        for side in self.sides:
            hashes.append(side.__hash__())
        hashes.sort()
        return hash(tuple(hashes))

    def get_common_sides(self, other) -> list:
        """ Since set is used, the amount of computation is O(n). """
        common_sides = list()
        sides_set = set(self.sides)
        for side in other.sides:
            if side in sides_set:
                common_sides.append(side)

        return common_sides

    def get_common_vertices(self, other) -> list:
        """ Since set is used, the amount of computation is O(n). """
        common_vertices = list()
        vertices_set = set(self.vertices)
        for vertex in other.vertices:
            if vertex in vertices_set:
                common_vertices.append(vertex)

        return common_vertices

    def combine(self, other):
        """ Combine two polygons """
        common_sides = self.get_common_sides(other)
        combined_polygon_sides = set(list(self.sides) + list(other.sides))
        for common_side in common_sides:
            combined_polygon_sides.remove(common_side)

        combined_polygon_area = self.area + other.area

        new_polygon = Polygon(tuple(combined_polygon_sides),
                area=combined_polygon_area,
                contains_point=self.contains_point)

        return new_polygon

    def draw(self, canvas: Canvas):
        for side in self.sides:
            begin = side.point1
            end = side.point2
            canvas.create_line(begin.x, begin.y, end.x, end.y)

    @staticmethod
    def compute_triangle_area(sides: tuple) -> float:
        """
        Compute the area from Heron's formula.

        Heron's formula:
        a, b, c : Length of each side
        s : Semiperimeter
        S : Area

        s = (a + b + c) / 2
        S = math.sqrt(s * (s - a) * (s - b) * (s - c))
        """
        if len(sides) != 3:
            return -1

        a = sides[0].length
        b = sides[1].length
        c = sides[2].length

        s = (a + b + c) / 2
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))

        return area

    @staticmethod
    def compute_triangle_gravity_center(vertices: tuple) -> Point:
        """
        Compute the triangle's center of gravity.

        Formula:
        vertices : (x1, y1), (x2, y2), (x3, y3)
        center of gravity : ((x1 + x2 + x3) / 3, (y1 + y2 + y3) / 3) 
        """
        v1, v2, v3 = vertices
        x = (v1.x + v2.x + v3.x) / 3
        y = (v1.y + v2.y + v3.y) / 3
        return Point(x, y)


class Circle:
    __center: Point
    __radius: float

    @property
    def center(self):
        return self.__center

    @property
    def radius(self):
        return self.__radius

    def __init__(self, center, radius):
        self.__center = center
        self.__radius = radius

    def draw(self, canvas: Canvas):
        """ For debugging """

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

        canvas.create_oval(x1, y1, x2, y2)

