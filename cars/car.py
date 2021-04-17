from typing import List

from cars.i_car import ICar
from cars.car_state import CarState
from cars.position import Position
from lanes.i_lane import ILane
from roadsections.i_road_section import IRoadSection


class Car(ICar):
    def __init__(self, length: float, path: List[IRoadSection], destination: Position):
        # TODO enter values
        self.__state = CarState()
        self.__length = length
        self.__path = path
        self.__destination = destination
        self.__speed = 0
        self.__acceleration = 0

        assert len(path) > 0
        self._enter_road_section(path[0], 0)

    @property
    def position(self):
        return self.__position

    def _enter_road_section(self, road: IRoadSection, lanes_from_right: int):
        self.__position = Position(0, 0)
        self.__current_road = road
        self.__current_lane = road.get_lane_from_right(lanes_from_right)

    def activate(self):
        pass

    def stop(self, location: float):
        self.__state.stopping = True
        position_in_lane = self.position.y if self.__current_lane.is_vertical else self.position.x

        # We want, where currentPosition = location then speed = 0
        # Gives us:
        # 0 = speed + a * t
        # location - currentPosition = speed * t + 0.5 * a * t ^ 2
        #
        # Results in:
        # a = -speed ^ 2 / (2 * (location - currentPosition))

        self.__acceleration = -pow(self.__speed, 2) / (2 * (location - position_in_lane))