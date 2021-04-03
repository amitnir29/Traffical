from numbers import Real
from typing import List

from cars.i_car import ICar
from cars.car_state import CarState
from cars.position import Position
from lanes.i_lane import ILane
from roadsections.i_road_section import IRoadSection


class Car(ICar):
    def __init__(self):
        # TODO enter values
        self.__state: CarState
        self.__length: Real
        self.__position: Position
        self.__currentRoad: IRoadSection
        self.__currentLane: ILane
        self.__currentLinePart: int
        self.__path: List[IRoadSection]
        self.__destination: Position
        self.__speed: Real
        self.__iteration: int = 0
        self.__maxAcceleration: Real
        self.__maxDeceleration: Real

    def activate(self) -> None:
        self.__iteration += 1
        # TODO rest
        pass
