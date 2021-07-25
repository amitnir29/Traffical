from __future__ import annotations

from abc import ABC, abstractmethod

from server.simulation_objects.iteration_trackable import IterationTrackable


class ICar(ABC, metaclass=IterationTrackable):
    @property
    @abstractmethod
    def position(self):
        pass

    @abstractmethod
    def activate(self):
        """
        commit one "step" of the car's action.
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

    @abstractmethod
    def estimated_speed(self) -> float:
        """
        :return: estimated speed that the car will have in this iteration
        """
        pass

    @property
    @abstractmethod
    def current_part_in_lane(self):
        pass

    @abstractmethod
    def has_arrived_destination(self):
        pass

    @abstractmethod
    def get_angle(self):
        """
        calculate the angle at which the cars should appear, counter clock wise.
        """
        pass

    @abstractmethod
    def get_id(self):
        pass
