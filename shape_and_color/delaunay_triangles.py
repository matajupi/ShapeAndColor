"""
Module for delaunay triangle generation.
"""

import random
from .libs import *


class DelaunayTriangles:
    """
    From http://tercel-sakuragaoka.blogspot.com/2011/06/processingdelaunay.html
    """

    triangle_set: set = set()
    width: int
    height: int

    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

    def triangulation(self, point_list: list):
        """
        Perform a Delaunay split based on "point_list".
        """
        # Add huge triangle to set
        huge_triangle = self.get_huge_triangle()
        self.triangle_set.add(huge_triangle)

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
            tmp_triangle_set = dict()

            """
            Take elements one by one from the current triangle list and
            determine if a given point is included in the circumscribed
            circle of each triangle.
            """
            it = set(self.triangle_set)
            for triangle in it:
                circumscribed_circle = self.get_circumscribed_circle_of_triangle(triangle)

                """
                If the added point exists inside the circumscribed circle,
                remove the triangle with the circumscribed circle from the
                list and divide it again.
                """
                if circumscribed_circle.center.distance(point) <= circumscribed_circle.radius:
                    vertices = triangle.vertices
                    vertex1 = vertices[0]
                    vertex2 = vertices[1]
                    vertex3 = vertices[2]

                    # Divide the triangle into three around point
                    self.add_element_to_redundancies_map(tmp_triangle_set,
                                                         Polygon((point, vertex1, vertex2)))
                    self.add_element_to_redundancies_map(tmp_triangle_set,
                                                         Polygon((point, vertex2, vertex3)))
                    self.add_element_to_redundancies_map(tmp_triangle_set,
                                                         Polygon((point, vertex3, vertex1)))

                    self.triangle_set.remove(triangle)

            # Add unique temporary hashes to the triangle list
            for triangle in tmp_triangle_set:
                if tmp_triangle_set[triangle]:
                    self.triangle_set.add(triangle)

        # Remove the vertices of the outer triangle
        it = set(self.triangle_set)
        for triangle in it:
            if huge_triangle.has_common_vertices(triangle):
                self.triangle_set.remove(triangle)

    def get_huge_triangle(self) -> Polygon:
        """
        Find an equilateral triangle that covers the entire screen.
        """
        rectangle = Polygon((Point(0, 0),
                            Point(self.width, 0),
                            Point(0, self.height),
                            Point(self.width, self.height)))
        return self.get_equilateral_triangle_contains_rectangle(rectangle)

    @staticmethod
    def get_equilateral_triangle_contains_rectangle(rectangle: Polygon) -> Polygon:
        """
        Find an equilateral triangle that includes an arbitrary rectangle.
        """
        # Find upper left coordinate and lower right coordinate
        def compare_vertex(point: Point) -> float:
            return point.x + point.y

        start = min(rectangle.vertices, key=compare_vertex)
        end = max(rectangle.vertices, key=compare_vertex)

        """
        Find the circle that contains the give rectangle.
        Center of circle c = Center of rectangle
        Circle radius r = |p - c| + ρ
        However, p is any vertex of the given rectangle and
        ρ is any positive number.
        """
        center = Point(abs(end.x - start.x) / 2,
                       abs(end.y - start.y) / 2)
        radius = center.distance(start) + 1.0

        """
        Find the equilateral triangle that circumscribes the circle.
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

        return Polygon((p1, p2, p3))

    @staticmethod
    def get_circumscribed_circle_of_triangle(triangle: Polygon) -> Circle:
        """
        Give a triangle and find its circumscribed circle.
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
        p1 = triangle.vertices[0]
        p2 = triangle.vertices[1]
        p3 = triangle.vertices[2]

        x1 = p1.x
        y1 = p1.y
        x2 = p2.x
        y2 = p2.y
        x3 = p3.x
        y3 = p3.y

        c = 2.0 * ((x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1))
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
    def add_element_to_redundancies_map(hash_map: dict, triangle: Polygon):
        """
        Add triangle to temporary hash.
        """
        if triangle in hash_map.keys():
            hash_map[triangle] = False
        else:
            hash_map[triangle] = True

    def draw(self, canvas: Canvas):
        """
        For debugging
        """
        for triangle in self.triangle_set:
            triangle.draw(canvas)


def create_points_randomly(max_width: int, max_height: int, num_of_points: int) -> list:
    points = list()
    for i in range(num_of_points):
        x = random.randint(0, max_width)
        y = random.randint(0, max_height)
        points.append(Point(x, y))
    return points
