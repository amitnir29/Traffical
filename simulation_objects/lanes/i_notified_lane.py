from abc import abstractmethod

import simulation_objects.lanes.i_lane as il
import simulation_objects.trafficlights.i_traffic_light as itl


class INotifiedLane(il.ILane):
    @property
    @abstractmethod
    def traffic_light(self) -> itl.ITrafficLight:
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
