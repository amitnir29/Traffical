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
        self.__path: path
        self.__destination = destination
        self.__speed = 0
        self.__acceleration = 0

        assert len(path) > 0
        self._enter_road_section(path[0], 0)

    def _enter_road_section(self, road: IRoadSection, lanes_from_right: int):
        self.__position = Position(0, 0)
        self.__current_road = road
        self.__current_lane = road.get_lane_from_right(lanes_from_right)

    def activate(self) -> None:
        self.__iteration += 1
        # TODO rest
        pass
