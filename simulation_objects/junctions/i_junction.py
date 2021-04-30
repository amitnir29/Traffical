from abc import ABC, abstractmethod
from typing import List

import simulation_objects.trafficlights.traffic_light as tl
from simulation_objects.geometry.point import Point


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
    def coordinates(self)->List[Point]:
        pass
