from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

from cars.i_car import ICar
from geometry.point import Point
from roadsections.i_road_section import IRoadSection


class ILane(ABC):
    """
    /**
    * returns the cars in the lane within
    * the distance given from the end of the lane.
    * ------------------------------- for the future us --------------------------
    * we can implement using getCarBetween
    */
    int getCarsInRange(int distance);
    """

    @abstractmethod
    def get_car_ahead(self, car: ICar) -> Optional[ICar]:
        """
        :param car: a car in the lane
        :return: the car ahead of the input car, in the lane
        """
        pass

    @abstractmethod
    def cars_amount(self) -> int:
        """
        :return: amount of cars in the lane
        """
        pass

    @abstractmethod
    def add_car(self, car) -> None:
        """
        :param car: a car
        :return: adds the input car to the lane
        """
        pass

    @abstractmethod
    def remove_car(self, car) -> None:
        """
        :param car: a car
        :return: removes the input car from the lane
        """
        pass

    @abstractmethod
    def get_cars_between(self, start: float, end: float) -> List[ICar]:
        """
        we use this function when a car wants to know which car to talk with whenever it wants to move to their lane.
        :param start: distance from start of the lane
        :param end: distance from end of the lane
        :return: cars that has a y position value between start and end
        """
        pass

    @abstractmethod
    def cars_from_end(self, distance: float) -> List[ICar]:
        """
        :param distance: a distance from the end of the lane
        :return: list of cars in the lane within the distance given from the end of the lane.
        """
        pass

    def cars_from_end_amount(self, distance: float) -> int:
        """
        :param distance: a distance from the end of the lane
        :return: amount of cars in the lane within the distance given from the end of the lane.
        """
        return len(self.cars_from_end(distance))

    @abstractmethod
    def car_position_in_lane(self, car):
        pass

    @property
    @abstractmethod
    def coordinates(self) -> List[Tuple[Point, Point]]:
        pass

    @property
    @abstractmethod
    def road(self) -> IRoadSection:
        pass

    @abstractmethod
    def is_going_to_road(self, road: IRoadSection):
        pass

    @abstractmethod
    def add_movement(self, to_lane: ILane):
        """
        add a lane to go to from this lane
        :param to_lane: the new lane to add
        """
        pass
