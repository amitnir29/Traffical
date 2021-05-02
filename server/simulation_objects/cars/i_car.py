from __future__ import annotations

from abc import ABC, abstractmethod

from server.simulation_objects.iteration_trackable import iteration_trackable


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
    def wants_to_enter_lane(self, car: ICar) -> None:
        """
        gets a car that wants to enter your lane,
        be nice to it!
        :param car: the car that wants to enter
        """
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
