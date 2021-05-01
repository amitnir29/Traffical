from abc import ABC, abstractmethod
from typing import List

from simulation_objects.geometry.point import Point


class Drawable(ABC):
    @abstractmethod
    def draw(self, screen, scale):
        """
        draw the object on the window
        """
        pass

    @staticmethod
    @abstractmethod
    def from_server_obj(obj):
        """
        create a drawable from the matching server object
        :param obj: the server object
        :return: the drawable object
        """
        pass

    @abstractmethod
    def get_all_points(self) -> List[Point]:
        """
        :return: a list of all points that are saved in the drawable
        """
        pass
