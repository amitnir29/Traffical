import copy
from collections import deque
from typing import List, Optional, Tuple
from copy import deepcopy

from server.geometry.line import Line
from server.geometry.point import Point

import server.simulation_objects.cars.i_car as ic
import server.simulation_objects.lanes.i_lane as il
import server.simulation_objects.roadsections.i_road_section as irs


class Lane(il.ILane):

    def __init__(self, road: irs.IRoadSection, coordinates: List[Tuple[Point, Point]]):
        self._cars = deque()
        self.__coordinates = deepcopy(coordinates)
        self._goes_to: List[il.ILane] = list()
        self._comes_from: List[il.ILane] = list()
        self.__road: irs.IRoadSection = road

        self._comes_from_junction = None

    def __deepcopy__(self, memodict={}):
        res = Lane.__new__(Lane)
        res.__dict__ = copy.copy(self.__dict__)

        res._cars = copy.copy(self._cars)

        return res

    @property
    def coordinates(self) -> List[Tuple[Point, Point]]:
        return self.__coordinates

    @property
    def road(self) -> irs.IRoadSection:
        return self.__road

    @property
    def goes_to_lanes(self):
        return self._goes_to

    def add_movement_out(self, to_lane: il.ILane):
        self._goes_to.append(to_lane)

    def add_movement_in(self, from_lane: il.ILane):
        self._comes_from.append(from_lane)

    def set_prev_junction(self, junction):
        self._comes_from_junction = junction

    @staticmethod
    def _calculate_part_length(start: Tuple[Point, Point], end: Tuple[Point, Point]):
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

    def lane_length(self) -> float:
        return sum([self._calculate_part_length(c1, c2) for c1, c2 in zip(self.coordinates, self.coordinates[1:])])

    def is_going_to_road(self, road: irs.IRoadSection):
        return road in [lane.road for lane in self._goes_to]

    def get_car_ahead(self, car: ic.ICar) -> Optional[ic.ICar]:
        car_index = self._cars.index(car)

        if car_index == 0:
            return None

        return self._cars[car_index - 1]

    def cars_amount(self) -> int:
        return len(self._cars)

    def add_car(self, car):
        self._cars.append(car)

    def remove_car(self, car):
        self._cars.remove(car)

    def cars_from_end(self, distance: float) -> List[ic.ICar]:
        return self.get_cars_between(self.lane_length() - distance, self.lane_length())

    def get_cars_between(self, start: float, end: float) -> List[ic.ICar]:
        res = list()

        for car in reversed(self._cars):
            position_in_line = self.car_position_in_lane(car)

            if start <= position_in_line <= end:
                res.append(car)

            elif position_in_line < start:
                break

        return res

    def car_position_in_lane(self, car):
        current_part = car.current_part_in_lane
        distance_of_previous_parts = sum(
            self._calculate_part_length(self.__coordinates[i], self.__coordinates[i + 1]) for i in range(current_part))

        current_part_start = Line(*self.__coordinates[current_part]).middle()
        distance_in_current_part = Line(current_part_start, car.position).length()

        return distance_of_previous_parts + distance_in_current_part

    def get_all_cars(self):
        return self._cars
