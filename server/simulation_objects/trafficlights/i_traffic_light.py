from abc import ABC, abstractmethod

from server.geometry.point import Point
from server.simulation_objects.iteration_trackable import IterationTrackable


class ITrafficLight(ABC):

    @abstractmethod
    def change_light(self, turn_to_green=None) -> None:
        """
        changes the light and notifies the cars that see the light
        :param turn_to_green: optional arg to constraint the value of the light
        """
        pass

    @property
    @abstractmethod
    def can_pass(self) -> bool:
        """
        return True if cars can pass (green light), False otherwise
        """
        pass

    @property
    @abstractmethod
    def coordinate(self) -> Point:
        pass

    @abstractmethod
    def activate(self):
        return

    @property
    @abstractmethod
    def light_time(self):
        pass

    @property
    @abstractmethod
    def lanes(self):
        pass
