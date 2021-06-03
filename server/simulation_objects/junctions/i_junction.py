from abc import ABC, abstractmethod
from typing import List

import server.simulation_objects.trafficlights.traffic_light as tl
from server.geometry.point import Point
from server.simulation_objects.trafficlights.i_traffic_light import ITrafficLight


class IJunction(ABC):
    @abstractmethod
    def update_traffic_lights(self, change: List[tl.TrafficLight]) -> None:
        """
        :param change: the traffic lights of the junctions
        """
        pass

    @abstractmethod
    def naive_algorithm(self) -> None:
        """
        algorithm1 - naive
        """
        pass

    @property
    @abstractmethod
    def coordinates(self) -> List[Point]:
        pass

    @property
    @abstractmethod
    def lights(self) -> List[ITrafficLight]:
        pass
