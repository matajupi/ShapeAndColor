"""
Module for delaunay triangle generation.
"""

import random
import math
from tkinter import Canvas
from libs import Point, Triangle, Circle, Drawable


class DelaunayTriangles(Drawable):
    """
    From http://tercel-sakuragaoka.blogspot.com/2011/06/processingdelaunay.html
    """

    __triangle_set: set = set()
    __triangle_adjacency_map: dict
    __width: int
    __height: int

    @property
    def triangles(self):
        return list(self.__triangle_set)

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def __init__(self, width: int, height: int):
        self.__width = width
        self.__height = height

    def triangulation(self, point_list: list):
        """
        Perform a Delaunay split based on "point_list".
        """
        # Add huge triangle to set
        huge_triangle = self.get_huge_triangle()
        self.__triangle_set.add(huge_triangle)

        # Add points sequentially and repeat triangulation
        for point in point_list:
            """
            Temporary hash holding additional candidate triangles.

            Of the triangles that can be added, "only those that do
            not overlap" are newly added to the triangle list.

            tmp_triangle_set
             -key   : Triangles(Polygon)
             -value : Whether it is duplicated.
                      - Non-duplicate : True
                      - Duplicate     : False
            """
            tmp_triangle_map = dict()

            """
            Take elements one by one from the current triangle list and
            determine if a given point is included in the circumscribed
            circle of each triangle.
            """
            iterator = set(self.__triangle_set)
            for triangle in iterator:
                circumscribed_circle = self.get_circumscribed_circle_of_triangle(triangle)

                """
                If the added point exists inside the circumscribed circle,
                remove the triangle with the circumscribed circle from the
                list and divide it again.
                """
                if circumscribed_circle.center.distance(point) <= circumscribed_circle.radius:
                    # Divide the triangle into three around point
                    points = triangle.points
                    point1 = points[0]
                    point2 = points[1]
                    point3 = points[2]

                    self.add_element_to_redundancies_map(tmp_triangle_map,
                                                         Triangle(point, point1, point2))
                    self.add_element_to_redundancies_map(tmp_triangle_map,
                                                         Triangle(point, point2, point3))
                    self.add_element_to_redundancies_map(tmp_triangle_map,
                                                         Triangle(point, point3, point1))

                    self.__triangle_set.remove(triangle)

            # Add unique temporary hashes to the triangle list
            for triangle, is_unique in tmp_triangle_map.items():
                if is_unique:
                    self.__triangle_set.add(triangle)

        # Remove the vertices of the outer triangle
        iterator = set(self.__triangle_set)
        for triangle in iterator:
            if huge_triangle.has_common_points(triangle):
                self.__triangle_set.remove(triangle)

    def get_huge_triangle(self) -> Triangle:
        """
        Find an equilateral triangle that covers the entire screen.
        """
        begin = Point(0, 0)
        end = Point(self.width, self.height)
        return self.get_equilateral_triangle_contains_rectangle(begin, end)

    def find_triangle_has_in_edge(self, compare_vector: Point) -> Triangle:
        # This algorithm is using cosine adjacency
        point_dict = dict()
        point_list = list()
        for triangle in self.triangles:
            for point in triangle.points:
                point_dict[point] = triangle
                point_list.append(point)
        point_list.sort(key=lambda p: (p.x * compare_vector.x + p.y * compare_vector.y) / (math.sqrt(p.x ** 2 + p.y ** 2) * math.sqrt(compare_vector.x ** 2 + compare_vector.y ** 2)))
        point = point_list[0]
        return point_dict[point]

    def create_triangle_adjacency_map(self):
        # Warning: Very heavy
        self.__triangle_adjacency_map = dict()
        for triangle in self.triangles:
            adjacent_triangles = self.find_adjacent_triangles(triangle)
            self.__triangle_adjacency_map[triangle] = adjacent_triangles

    def find_adjacent_triangles(self, triangle: Triangle) -> list:
        adjacent_triangles = list()
        for compare_triangle in self.triangles:
            if compare_triangle == triangle:
                continue
            if triangle.has_common_sides(compare_triangle):
                adjacent_triangles.append(compare_triangle)
        return adjacent_triangles

    def get_adjacent_triangles(self, triangle: Triangle) -> list:
        " This method must be O(1). """
        return self.__triangle_adjacency_map[triangle]

    @staticmethod
    def get_equilateral_triangle_contains_rectangle(p1: Point, p2: Point) -> Triangle:
        """
        Compute an equilateral triangle that includes an arbitrary rectangle.
        """
        """
        Compute the circle that contains the give rectangle.
        Center of circle c = Center of rectangle (width / 2, height / 2)
        Circle radius r = |p - c| + ρ
        However, p is any vertex of the given rectangle and
        ρ is any positive number.
        """
        if p1.x > p2.x:
            p1, p2 = p2, p1
        delta_x = p2.x - p1.x
        if p1.y > p2.y:
            p1, p2 = p2, p1
        delta_y = p2.y - p1.y

        center = Point(delta_x / 2, delta_y / 2)
        radius = center.distance(p1) + 1.0

        """
        Compute the equilateral triangle that circumscribes the circle.
        The center of gravity is equal to the center of circle.
        The length of one side is 2 * math.sqrt(3) * radius.
        """
        x1 = center.x - math.sqrt(3) * radius
        y1 = center.y - radius
        p1 = Point(x1, y1)

        x2 = center.x + math.sqrt(3) * radius
        y2 = center.y - radius
        p2 = Point(x2, y2)

        x3 = center.x
        y3 = center.y + 2 * radius
        p3 = Point(x3, y3)

        return Triangle(p1, p2, p3)

    @staticmethod
    def get_circumscribed_circle_of_triangle(triangle: Triangle) -> Circle:
        """
        Give a triangle and compute its circumscribed circle.
        """
        """
        Let the coordinates of each vertex of the triangle be (x1, y1), (x2, y2), (x3, y3) and
        the center coordinates of the circumscribed circle be (x, y).
          (x - x1) ^ 2 + (y - y1) ^ 2
        = (x - x2) ^ 2 + (y - y2) ^ 2
        = (x - x3) ^ 2 + (y - y3) ^ 2

        Therefore, the following formula holds.
        x = { (y3 - y1) * (x2 ^ 2 - x1 ^ 2 + y2 ^ 2 - y1 ^ 2)
            + (y1 - y2) * (x3 ^ 2 - x1 ^ 2 + y3 ^ 2 - y1 ^ 2) } / c

        y = { (x1 - x3) * (x2 ^ 2 - x1 ^ 2 + y2 ^ 2 - y1 ^ 2)
            + (x2 - x1) * (x3 ^ 2 - x1 ^ 2 + y3 ^ 2 - y1 ^ 2) } / c

        However
        c = 2 * { (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1) }
        """
        p1 = triangle.points[0]
        p2 = triangle.points[1]
        p3 = triangle.points[2]

        x1 = p1.x
        y1 = p1.y
        x2 = p2.x
        y2 = p2.y
        x3 = p3.x
        y3 = p3.y

        c = 2 * ((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))
        mul1 = (x2 ** 2 - x1 ** 2 + y2 ** 2 - y1 ** 2)
        mul2 = (x3 ** 2 - x1 ** 2 + y3 ** 2 - y1 ** 2)
        x = ((y3 - y1) * mul1
           + (y1 - y2) * mul2) / c
        y = ((x1 - x3) * mul1
           + (x2 - x1) * mul2) / c

        center = Point(x, y)
        radius = center.distance(p1)

        return Circle(center, radius)

    @staticmethod
    def add_element_to_redundancies_map(hash_map: dict, triangle: Triangle):
        """
        Add triangle to temporary hash.
        """
        if triangle in hash_map:
            hash_map[triangle] = False
        else:
            hash_map[triangle] = True

    def draw(self, canvas: Canvas):
        """
        For debugging
        """
        for triangle in self.triangles:
            triangle.draw(canvas)

    MIN_DISTANCE = 30

    @staticmethod
    def create_points_randomly(width: int, height: int, num_points: int) -> list:
        points = list()
        for i in range(num_points):
            flag = True
            point: Point
            while flag:
                flag = False
                x = random.randint(10, width - 10)
                y = random.randint(10, height - 10)
                point = Point(x, y)
                for other in points:
                    flag = flag or point.distance(other) < DelaunayTriangles.MIN_DISTANCE
            points.append(point)
        return points

