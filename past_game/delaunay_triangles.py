"""
Module for delaunay triangle generation.
"""

import random
from libs import *


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

    def triangulation(self, point_list: list) -> list:
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
            tmp_triangle_map = dict()

            """
            Take elements one by one from the current triangle list and
            determine if a given point is included in the circumscribed
            circle of each triangle.
            """
            iterator = set(self.triangle_set)
            for triangle in iterator:
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
                    side1 = UndirectedLineSegment(point, vertex1)
                    side2 = UndirectedLineSegment(vertex1, vertex2)
                    side3 = UndirectedLineSegment(vertex2, point)
                    side4 = UndirectedLineSegment(vertex2, vertex3)
                    side5 = UndirectedLineSegment(vertex3, point)
                    side6 = UndirectedLineSegment(vertex3, vertex1)

                    self.add_element_to_redundancies_map(tmp_triangle_map,
                                                         Polygon((side1, side2, side3)))
                    self.add_element_to_redundancies_map(tmp_triangle_map,
                                                         Polygon((side3, side4, side5)))
                    self.add_element_to_redundancies_map(tmp_triangle_map,
                                                         Polygon((side5, side6, side1)))

                    self.triangle_set.remove(triangle)

            # Add unique temporary hashes to the triangle list
            for triangle in tmp_triangle_map:
                if tmp_triangle_map[triangle]:
                    self.triangle_set.add(triangle)

        # Remove the vertices of the outer triangle
        iterator = set(self.triangle_set)
        for triangle in iterator:
            if huge_triangle.get_common_vertices(triangle):
                self.triangle_set.remove(triangle)

        return list(self.triangle_set)

    def get_huge_triangle(self) -> Polygon:
        """
        Find an equilateral triangle that covers the entire screen.
        """
        rect_side1 = UndirectedLineSegment(Point(0, 0), Point(self.width, 0))
        rect_side2 = UndirectedLineSegment(Point(self.width, 0), Point(self.width, self.height))
        rect_side3 = UndirectedLineSegment(Point(self.width, self.height), Point(0, self.height))
        rect_side4 = UndirectedLineSegment(Point(0, self.height), Point(0, 0))

        rectangle = Polygon((rect_side1, rect_side2, rect_side3, rect_side4))
        return self.get_equilateral_triangle_contains_rectangle(rectangle)

    @staticmethod
    def get_equilateral_triangle_contains_rectangle(rectangle: Polygon) -> Polygon:
        """
        Find an equilateral triangle that includes an arbitrary rectangle.
        """
        # Compute delta_x, delta_y
        delta_x_list = list()
        delta_y_list = list()
        for side in rectangle.sides:
            delta_x = abs(side.point1.x - side.point2.x)
            delta_y = abs(side.point1.y - side.point2.y)
            if delta_x > 0:
                delta_x_list.append(delta_x)
            if delta_y > 0:
                delta_y_list.append(delta_y)

        delta_x = max(delta_x_list)
        delta_y = max(delta_y_list)

        """
        Find the circle that contains the give rectangle.
        Center of circle c = Center of rectangle
        Circle radius r = |p - c| + ρ
        However, p is any vertex of the given rectangle and
        ρ is any positive number.
        """
        center = Point(delta_x / 2, delta_y / 2)
        radius = math.sqrt((delta_x ** 2 + delta_y ** 2) / 4) + 1.0

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

        side1 = UndirectedLineSegment(p1, p2)
        side2 = UndirectedLineSegment(p2, p3)
        side3 = UndirectedLineSegment(p3, p1)

        return Polygon((side1, side2, side3))

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

MIN_DISTANCE = 30

def create_points_randomly(max_width: int, max_height: int, num_of_points: int) -> list:
    points = list()
    for i in range(num_of_points):
        flag = True
        point: Point
        while flag:
            flag = False
            x = random.randint(10, max_width - 10)
            y = random.randint(10, max_height - 10)
            point = Point(x, y)
            for other in points:
                flag = flag or point.distance(other) < MIN_DISTANCE
        points.append(point)
    return points

