from __future__ import annotations

from abc import ABC, abstractmethod
from numbers import Real

from lanes.i_lane import ILane


class ICar(ABC):

    @abstractmethod
    def activate(self) -> None:
        """
        commit one "step" of the car's action
        """
        pass

    @abstractmethod
    def should_move_lane(self) -> bool:
        """
        :return: True if we should move lane.
        """
        pass

    @abstractmethod
    def get_closest_valid_lane(self) -> ILane:
        """
        :return: the lane we should move to next
        """
        pass

    @abstractmethod
    def moveLane(self) -> None:
        """
        moves a lane. when done - returns.
        for the future us - when we get a premission to move a line, make sure to add the car to the moved laned, and
        to only delete the car from the current lane, when we are completly done with the transaction. #TODO
        """
        pass

    @abstractmethod
    def stop(self, location: Real) -> None:
        """
        :param location: #TODO
        :return: stops the car until it reaches the location.
        """
        pass

    @abstractmethod
    def notified(self) -> None:
        """
        getting a light notification
        """
        pass

    @abstractmethod
    def wants_to_enter_lane(self, car: ICar) -> None:
        """
        gets a car that wants to enter your lane,
        be nice to it!
        :param car: the car that wants to enter
        """
        pass
