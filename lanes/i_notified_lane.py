from lanes.i_lane import ILane
from abc import abstractmethod

from trafficlights.i_traffic_light import ITrafficLight


class INotifiedLane(ILane):
    @property
    @abstractmethod
    def traffic_light(self) -> ITrafficLight:
        pass

    @traffic_light.setter
    @abstractmethod
    def traffic_light(self, new_traffic_light):
        pass

    @abstractmethod
    def notified(self) -> None:
        """
        gets a notification from the traffic light and according to that notifies the first car
        """
        pass
