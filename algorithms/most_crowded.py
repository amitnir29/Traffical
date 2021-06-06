from collections import defaultdict
from typing import Dict

from algorithms.tl_manager import TLManager


class MCAlgo(TLManager):

    def __init__(self, traffic_lights, all_junctions, min_green_time=5):
        super().__init__(traffic_lights, all_junctions)
        self._min_green_time = min_green_time
        self.init_lights()

    def init_lights(self):
        for junc in self.get_tl_junctions():
            junc.lights[0].change_light()

    def _get_green_tl(self, junc):
        for tl in junc.lights:
            if tl.can_pass:
                return tl
        raise Exception("no green light")

    def manage_lights(self, cars):
        for junc in self._tl_junctions:
            green = self._get_green_tl(junc)
            if green.light_time < self._min_green_time:
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
