from abc import ABC, abstractmethod

from simulation_objects.geometry.point import Point


class ITrafficLight(ABC):

    @abstractmethod
    def changeLight(self) -> None:
        """
        changes the light and notifies the cars that see the light
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
