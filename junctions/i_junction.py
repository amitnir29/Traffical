from abc import ABC, abstractmethod
from typing import List

from trafficlights.traffic_light import TrafficLight


class IJunction(ABC):
    @abstractmethod
    def update_traffic_lights(self, change: List[TrafficLight]) -> None:
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
