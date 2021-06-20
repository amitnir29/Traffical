from abc import ABC, abstractmethod

from algorithms.tl_manager import TLManager


class RLQ(TLManager, ABC):
    @staticmethod
    @abstractmethod
    def _cars_load_in_tl(tl):
        raise NotImplemented

    def _manage_lights(self):
        return max(self._lights, key=lambda tl: self._cars_load_in_tl(tl))


class RLQTL(RLQ):
    @staticmethod
    def _cars_load_in_tl(tl):
        # Load should also depend on cars' lengths. Assuming all cars are of the same length,
        # car's length can be dropped for ordering purpose.
        return sum(lane.cars_amount() for lane in tl.lanes) / sum(lane.lane_length() for lane in tl.lanes)


class RLQRS(RLQ):
    @staticmethod
    def _cars_load_in_tl(tl):
        # Load should also depend on cars' lengths. Assuming all cars are of the same length,
        # car's length can be dropped for ordering purpose.
        return sum(lane.cars_amount() / lane.lane_length() for lane in tl.lanes) / len(tl.lanes)
