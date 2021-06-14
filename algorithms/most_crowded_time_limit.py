from collections import defaultdict
from typing import Dict

from algorithms.tl_manager import TLManager


class MCTL(TLManager):

    def __init__(self, junction, min_green_time=5, max_red_time=60):
        super().__init__(junction)
        self._min_green_time = min_green_time

        self.__max_red_time = max_red_time

    def _map_cars_amount(self):
        # for each light, get number of cars in its lanes
        cars_count: Dict[int, int] = defaultdict(int)
        for i, tl in enumerate(self._junction.lights):
            for lane in tl.lanes:
                cars_count[i] += lane.cars_amount()

        return cars_count

    def manage_lights(self):
        if len(self._lights) == 0:
            return

        green = self._current_light
        if green.light_time < self._min_green_time:
            return

        # also, check if there is a light that has been red for too long
        waiting_longest = max([tl for tl in self._junction.lights if tl != green], key=lambda tl: tl.light_time)
        if waiting_longest.light_time > self.__max_red_time:
            green.change_light(False)  # to red
            waiting_longest.change_light(True)  # to green
        else:
            cars_count = self._map_cars_amount()
            # print(cars_count.values())
            mc_lane = self._junction.lights[max(cars_count, key=lambda k: cars_count[k])]
            if mc_lane != green:
            # if not mc_lane.can_pass:
                green.change_light(False)  # to red
                mc_lane.change_light(True)  # to green

            self._current_light = mc_lane
