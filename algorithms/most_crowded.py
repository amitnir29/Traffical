from collections import defaultdict
from typing import Dict

from algorithms.tl_manager import TLManager


class MCAlgo(TLManager):

    def __init__(self, junction, min_green_time=5):
        super().__init__(junction)
        self._min_green_time = min_green_time

    def _map_cars_amount(self):
        # for each light, get number of cars in its lanes
        cars_count: Dict[int, int] = defaultdict(int)
        for i, tl in enumerate(self._junction.lights):
            for lane in tl.lanes:
                cars_count[i] += lane.cars_amount()

        return cars_count

    def _manage_lights(self):
        if self._current_light.light_time < self._min_green_time:
            return self._current_light

        cars_count = self._map_cars_amount()
        mc_lane = self._junction.lights[max(cars_count, key=lambda k: cars_count[k])]
        return mc_lane
