from lanes.i_lane import ILane
from abc import abstractmethod


class INotifiedLane(ILane):
    @abstractmethod
    def notified(self) -> None:
        """
        gets a notification from the traffic light and according to that notifies the first car
        """
        pass
