"""
Module for mission generation and execution.
"""

from abc import ABC, abstractmethod
from delaunay_triangles import *
from mission import *
from side_reducer import *


# "MissionCreator" uses Strategy pattern.
class MissionCreator(ABC):
    """
    Create mission with the implemented algorithm.
    This uses a strategy pattern and factory method pattern.
    (Let's google with "Gang of Four design patterns".)
    """
    @abstractmethod
    def create(self, canvas: Canvas) -> Mission:
        pass


class DelaunayMissionCreator(MissionCreator):
    """
    A class that creates missions using the Delaunay diagram.
    """
    # For the time being ...
    NUM_OF_REDUCE: int = 2

    def create(self, canvas: Canvas, width: int, height: int, num_points) -> Mission:
        polygons = self.create_delaunay_triangles(width, height, num_points)
        # self.reduce_sides_randomly(polygons, self.NUM_OF_REDUCE)
        mission = Mission(canvas, polygons, width, height)
        return mission

    def create_delaunay_triangles(self, width, height, num_points) -> list:
        points = create_points_randomly(width, height, num_points)
        delaunay = DelaunayTriangles(width, height)
        polygons = delaunay.triangulation(points)
        return polygons

    def reduce_sides_randomly(self, polygons: list, times: int):
        side_reducer = SideReducer()
        side_reducer.reduce_randomly(polygons, times)


