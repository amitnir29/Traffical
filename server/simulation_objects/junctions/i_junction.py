from abc import ABC, abstractmethod
from typing import List

from server.geometry.point import Point
from server.simulation_objects.trafficlights.i_traffic_light import ITrafficLight


class IJunction(ABC):
    @property
    @abstractmethod
    def coordinates(self) -> List[Point]:
        pass

    @property
    @abstractmethod
    def lights(self) -> List[ITrafficLight]:
        pass
