from __future__ import annotations
from abc import abstractmethod

import server.simulation_objects.lanes.i_lane as il
import server.simulation_objects.trafficlights.i_traffic_light as itl


class INotifiedLane(il.ILane):
    @property
    @abstractmethod
    def traffic_light(self) -> itl.ITrafficLight:
        pass

    @traffic_light.setter
    @abstractmethod
    def traffic_light(self, new_traffic_light):
        pass
