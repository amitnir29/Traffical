from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple

from iteration_trackable import iteration_trackable
from lanes.i_lane import ILane


@iteration_trackable
class ICar(ABC):
    @property
    @abstractmethod
    def position(self):
        pass

    @abstractmethod
    def activate(self) -> None:
        """
        commit one "step" of the car's action
        """
        pass

    @abstractmethod
    def notified(self) -> None:
        """
        getting a light notification
        """
        pass

    # car driving functions
    @abstractmethod
    def stop(self, location: float) -> None:
        """
        :param location: #TODO
        :return: stops the car until it reaches the location.
        """
        pass

    @abstractmethod
    def move_forward(self) -> None:
        """
        move one step forward depending on the speed of the car, cars around it, and junctions.
        """

    # Lane moving functions
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
    def move_lane(self) -> None:
        """
        moves a lane. when done - returns.
        for the future us - when we get a premission to move a line, make sure to add the car to the moved laned, and
        to only delete the car from the current lane, when we are completly done with the transaction. #TODO
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

    @property
    @abstractmethod
    def speed(self) -> float:
        pass

    def estimated_speed(self) -> float:
        """
        :return: estimated speed that the car will have in this iteration
        """
        pass

    @property
    @abstractmethod
    def current_part_in_lane(self):
        pass
