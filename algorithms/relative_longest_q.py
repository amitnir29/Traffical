from abc import ABC, abstractmethod

from algorithms.tl_manager import TLManager


class RLQ(TLManager, ABC):
    @staticmethod
    @abstractmethod
    def _cars_load_in_tl(tl):
        raise NotImplemented

    def manage_lights(self):
        if len(self._lights) == 0:
            return 0

        most_loaded_tl = max(self._lights, key=lambda tl: self._cars_load_in_tl(tl))

        if most_loaded_tl != self._current_light:
            self._current_light.change_light(False)
            most_loaded_tl.change_light(True)

            self._current_light = most_loaded_tl


class RLQTL(RLQ):
    @staticmethod
    def _cars_load_in_tl(tl):
        # Load should also depend on cars' lengths. Assuming all cars are of the same length, car's length can be dropped for ordering purpose.
        return sum(lane.cars_amount() for lane in tl.lanes) / sum(lane.lane_length() for lane in tl.lanes)


class RLQRS(RLQ):
    @staticmethod
    def _cars_load_in_tl(tl):
        # Load should also depend on cars' lengths. Assuming all cars are of the same length, car's length can be dropped for ordering purpose.
        return sum(lane.cars_amount() / lane.lane_length() for lane in tl.lanes) / len(tl.lanes)
