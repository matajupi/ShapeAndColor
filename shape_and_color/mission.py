"""
Module for mission generation and execution.
"""

from abc import ABC, abstractmethod
from .delaunay_triangles import *


# "MissionCreator" that creates the mission and "Mission" that represents the mission are separated.
# "Mission" also holds run-time information.
class Mission:
    canvas: Canvas

    width: int
    height: int

    matrix: list
    vectors: list = list()

    time: int = 0

    def __init__(self, canvas: Canvas):
        self.canvas: Canvas = canvas
        self.initialize_canvas()

        self.width = canvas.winfo_width()
        self.height = canvas.winfo_height()

        self.matrix = [[None for j in range(self.width)]
                       for i in range(self.height)]

    def initialize_canvas(self):
        self.canvas.bind("<ButtonRelease1>", self.on_left_button_click)

    def on_left_button_click(self, event):
        # debug
        print(event.x, event.y)
        # TODO: Implement

    def start(self):
        self.draw()
        # TODO: Implement

    def draw(self):
        # TODO: Implement
        pass


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
    NUM_OF_POINTS: int = 500

    def create(self, canvas: Canvas) -> Mission:
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        points = create_points_randomly(width, height, self.NUM_OF_POINTS)
        delaunay = DelaunayTriangles(width, height)
        delaunay.triangulation(points)

        # TODO: Randomly reduce the number of edges in the Delaunay diagram
        # それぞれの三角形の面積を測量する
        # 測量した面積をKeyに三角形をソートする
        # 三角形の以下のrandomな数を取得する
        # 面積の小さい三角形の辺からランダムな辺を順に1本ずつ間引いていく。
        # 線を間引いたらその2つの三角形は結合して一つの4角形として定義しなおす。
        # 四角形の一部となった三角形は上でソートした配列からRemoveする。
        # RemoveしたらRandomな数も1減らす
        # この動作をN回繰り返す（次は四角形のみを取り出しそれの面積を測量してソートしてRandomな数だけ線を間引く（5角形もしくは6角形に））
        # 本当はこれらの操作の時に結合時の2辺のなす角度なども考慮するがそれはまた後から
        # NはS角形を最大の多角形にしたいとすると3, 4, 6, 10, 18,...と増えていくので...
        # という式で表される
        # TODO: Build a mission
