from abc import ABC, abstractmethod
from typing import List

import trafficlights.traffic_light as tl


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
