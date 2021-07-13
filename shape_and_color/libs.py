"""
Libraries for creating a mission.
"""

import math
from tkinter import Canvas


class Point:
    __x: float
    __y: float

    def __init__(self, x: int, y: int):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

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

    def __init__(self, point1, point2):
        self.__point1 = point1
        self.__point2 = point2

    @property
    def point1(self):
        return self.__point1

    @property
    def point2(self):
        return self.__point2

    def __eq__(self, other):
        point_set = {self.point1, self.point2}
        other_points = [other.point1, other.point2]
        flag = True
        for point in other_points:
            flag = flag and point in point_set
        return flag

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        x_list = [self.point1.x, self.point2.x]
        y_list = [self.point1.y, self.point2.y]
        x_list.sort()
        y_list.sort()
        return hash(tuple(x_list + y_list))


class Polygon:
    # Store in the order of the points of the figure.
    __vertices: tuple
    __num_of_vertices: int
    __area: float

    def __init__(self, vertices: tuple, area=-1):
        for point in vertices:
            if not isinstance(point, Point):
                raise TypeError("All arguments must be of type point.")
        self.__vertices = vertices
        self.__num_of_vertices = len(vertices)

        if area < 0 and self.num_of_vertices == 3:
            area = self.compute_triangle_area(self.vertices)
        self.__area = area

    @property
    def vertices(self):
        return self.__vertices

    @property
    def num_of_vertices(self):
        return self.__num_of_vertices

    @property
    def area(self):
        return self.__area

    @staticmethod
    def compute_triangle_area(vertices: tuple) -> float:
        """
        Compute the area from Heron's formula.

        Heron's formula:
        a, b, c : Length of each side
        s : Semiperimeter
        S : Area

        s = (a + b + c) / 2
        S = math.sqrt(s * (s - a) * (s - b) * (s - c))
        """
        a = vertices[0].distance(vertices[1])
        b = vertices[1].distance(vertices[2])
        c = vertices[2].distance(vertices[0])

        s = (a + b + c) / 2
        area = math.sqrt(s * (s - a) * (s - b) * (s - c))

        return area

    def has_common_vertices(self, other) -> bool:
        """ Since set is used, the amount of computation is O(n). """
        vertices_set = set(self.vertices)
        for vertex in other.vertices:
            if vertex in vertices_set:
                return True
        return False

    def get_common_vertices(self, other) -> list:
        """ Since set is used, the amount of computation is O(n). """
        common_vertices = []
        vertices_set = set(self.vertices)
        for vertex in other.vertices:
            if vertex in vertices_set:
                common_vertices.append(vertex)
        return common_vertices

    def combine(self, other):
        # 普通はN角形とM角形を結合するとN＋M-2角形が生成される。しかしこれにはコーナーケースがある。
        # 例えば1頂点がくぼんだ形の5角形のくぼみの部分に4角形がはまっている状況を考える。
        # 結合すると5角形になる
        # つまりN角形とM角形を結合したとき共有している辺がS本あったとすると結合後は
        # N + M - 2 * S角形となる
        # TODO: Implement
        new_polygon = Polygon()
        return new_polygon

    def __eq__(self, other):
        """ Since set is used, the amount of computation is O(n). """
        if self.num_of_vertices == other.num_of_vertices:
            vertices_set = set(self.vertices)
            for vertex in other.vertices:
                vertices_set.add(vertex)
            return len(vertices_set) == self.num_of_vertices
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        """  """
        """ 
        Algorithm:
        Let XList be a list that sorts the Xs of all vertices in ascending order.
        Let YList be a list that sorts the Ys of all vertices in ascending order.
        Combine two lists in the order of XList, YList.
        Let the value obtained by passing the combined list trough the hash function
        as the hash value.
        """
        x_list = []
        y_list = []
        for vertex in self.vertices:
            x_list.append(vertex.x)
            y_list.append(vertex.y)
        x_list.sort()
        y_list.sort()
        combined_list = x_list + y_list
        return hash(tuple(combined_list))

    def draw(self, canvas: Canvas):
        for i in range(self.num_of_vertices):
            begin = self.vertices[i]
            end = self.vertices[(i + 1) % self.num_of_vertices]
            canvas.create_line(begin.x, begin.y, end.x, end.y)


class Circle:
    __center: Point
    __radius: float

    def __init__(self, center, radius):
        self.__center = center
        self.__radius = radius

    @property
    def center(self):
        return self.__center

    @property
    def radius(self):
        return self.__radius

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
