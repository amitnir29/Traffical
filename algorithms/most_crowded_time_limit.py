from collections import defaultdict
from typing import Dict

from algorithms.most_crowded import MCAlgo


class MCTL(MCAlgo):
    def __init__(self, traffic_lights, all_junctions, min_green_time=5, max_red_time=60):
        super().__init__(traffic_lights, all_junctions, min_green_time)
        self.__max_red_time = max_red_time

    def manage_lights(self, cars):
        for junc in self._tl_junctions:
            green = self._get_green_tl(junc)
            if green.light_time < self._min_green_time:
                continue
            # also, check if there is a light that has been red for too long
            waiting_longest = max([tl for tl in junc.lights if tl != green], key=lambda tl: tl.light_time)
            if waiting_longest.light_time > self.__max_red_time:
                green.change_light(False)  # to red
                waiting_longest.change_light(True)  # to green
                continue
            # for each light, get number of cars in its lanes
            cars_count: Dict[int, int] = defaultdict(int)
            for i, tl in enumerate(junc.lights):
                for lane in tl.lanes:
                    cars_count[i] += lane.cars_amount()
            mc_lane = junc.lights[max(cars_count, key=lambda k: cars_count[k])]
            if mc_lane != green:
                green.change_light(False)  # to red
                mc_lane.change_light(True)  # to green
