from collections import deque
from typing import List, Optional, Tuple

from cars.i_car import ICar
from db_dataclasses.road_lane import RoadLane
from geometry.line import Line
from geometry.point import Point
from lanes.i_lane import ILane
from roadsections.i_road_section import IRoadSection


class Lane(ILane):

    def __init__(self, road: IRoadSection, coordinates: List[Tuple[Point, Point]], vertical: bool = True):
        self.__cars = deque()
        self.__vertical = vertical
        self.__coordinates = coordinates
        self.__length = self.__calculate_lane_length(coordinates)
        self.__goes_to: List[ILane] = list()
        self.__road: IRoadSection = road

    @property
    def is_vertical(self):
        return self.__vertical

    @property
    def coordinates(self) -> List[Tuple[Point, Point]]:
        return self.__coordinates

    @property
    def road(self) -> IRoadSection:
        return self.__road

    def add_movement(self, to_lane: ILane):
        self.__goes_to.append(to_lane)

    def __calculate_part_length(self, start: Tuple[Point, Point], end: Tuple[Point, Point]):
        """
        calculate the lengtth of a lane part
        :param start: the pair of points of the start
        :param end: the pair of points of the end
        :return: the length of the part
        """
        # calcualte the length of the line between the middle points of the start and end lines
        start_line = Line(start[0], start[1])
        end_line = Line(end[0], end[1])
        start_middle = start_line.middle()
        end_middle = end_line.middle()
        main_line = Line(start_middle, end_middle)
        return main_line.length()

    def __calculate_lane_length(self, coordinates: List[Tuple[Point, Point]]) -> float:
        """
        :param coordinates: a list of pairs of points that represent the lane.
        :return: total length of the lane
        """
        return sum([self.__calculate_part_length(c1, c2) for c1, c2 in zip(coordinates, coordinates[1:])])

    def is_going_to_road(self, road: IRoadSection):
        return road in [lane.road for lane in self.__goes_to]

    def get_car_ahead(self, car: ICar) -> Optional[ICar]:
        car_index = self.__cars.index(car)

        if car_index == 0:
            return None

        return self.__cars[car_index - 1]

    def cars_amount(self) -> int:
        return len(self.__cars)

    def add_car(self, car):
        self.__cars.append(car)

    def remove_car(self, car):
        self.__cars.remove(car)

    def cars_from_end(self, distance: float) -> List[ICar]:
        return self.get_cars_between(self.__length - distance, self.__length)

    def get_cars_between(self, start: float, end: float) -> List[ICar]:
        res = list()

        for car in reversed(self.__cars):
            position_in_line = self.car_position_in_lane(car)

            if start <= position_in_line <= end:
                res.append(car)

            elif position_in_line < start:
                break

        return res

    def car_position_in_lane(self, car):
        return car.position.y if self.is_vertical else car.position.x
