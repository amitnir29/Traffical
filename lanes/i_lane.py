from abc import ABC, abstractmethod
from numbers import Real
from typing import List

from cars.i_car import ICar


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
    def get_car_ahead(self, car: ICar) -> ICar:
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
    def get_cars_between(self, start: Real, end: Real) -> List[ICar]:
        """
        we use this function when a car wants to know which car to talk with whenever it wants to move to their lane.
        :param start: distance from start of the lane
        :param end: distance from end of the lane
        :return: cars that has a y position value between start and end
        """
        pass

    @abstractmethod
    def cars_from_end(self, distance: Real) -> List[ICar]:
        """
        :param distance: a distance from the end of the lane
        :return: list of cars in the lane within the distance given from the end of the lane.
        """
        pass

    def cars_from_end_amount(self, distance: Real) -> int:
        """
        :param distance: a distance from the end of the lane
        :return: amount of cars in the lane within the distance given from the end of the lane.
        """
        return len(self.cars_from_end(distance))

    @property
    def is_vertical(self):
        pass
