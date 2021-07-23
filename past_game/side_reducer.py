import random
from libs import *


class SideReducer:
    def reduce_randomly(self, polygons: list, reduce_times: int):
        #self.reduce_randomly_helper2(polygons)
        for i in range(reduce_times):
            self.reduce_randomly_helper(polygons, 3 + i, )

    def reduce_randomly_helper2(self, polygons: list):
        num_reduce = random.randint(len(polygons) // 2, len(polygons) + 1)
        counter = 0
        while num_reduce > counter and len(polygons) > 0:
            polygons.sort(key=lambda polygon: polygon.area)
            target = polygons[0]

            flag = False
            reduce_side_num = 0
            while not flag and reduce_side_num < len(target.sides):
                reduce_side = target.sides[reduce_side_num]
                flag = self.try_reduce_side(polygons, reduce_side)
                reduce_side_num += 1

            counter += 1


    def reduce_randomly_helper(self, polygons: list, target: int):
        """ Brute force reduction is computationally expensive. """
        # TODO: Reduce computational effort
        target_polygons = self.select_target_polygons(polygons, target)
        num_reduce = random.randint(len(target_polygons) // 3, len(target_polygons) + 1)
        counter = 0
        while num_reduce > counter and len(target_polygons) > 0:
            target_polygons.sort(key=lambda polygon: polygon.area)
            target_polygon = target_polygons[0]

            flag = False
            reduce_side_num = 0
            while not flag and reduce_side_num < target:
                reduce_side = target_polygon.sides[reduce_side_num]
                flag = self.try_reduce_side(polygons, reduce_side)
                reduce_side_num += 1

            target_polygons = self.select_target_polygons(polygons, target)
            counter += 1

    def try_reduce_side(self, polygons: list, reduce_side: UndirectedLineSegment) -> bool:
        reduce_polygons = list()
        for polygon in polygons:
            if reduce_side in polygon.sides:
                reduce_polygons.append(polygon)

        if len(reduce_polygons) <= 1:
            return False

        new_polygon = reduce_polygons[0].combine(reduce_polygons[1])
        polygons.remove(reduce_polygons[0])
        polygons.remove(reduce_polygons[1])
        polygons.append(new_polygon)

        return True

    def select_target_polygons(self, polygons: list, target: int) -> list:
        target_polygons = list()
        for polygon in polygons:
            if polygon.vertex_quantity == target:
                target_polygons.append(polygon)
        return target_polygons

