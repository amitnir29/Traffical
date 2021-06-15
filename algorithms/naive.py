import numpy as np

from algorithms.tl_manager import TLManager


class NaiveAlgo(TLManager):
    def __init__(self, junction, light_interval=10, time_limit=np.inf):
        super().__init__(junction, time_limit)
        self.__time_count = 0
        self.__light_interval = light_interval
        self._curr_light_index = 0

    def _manage_lights(self):
        if self.__time_count % self.__light_interval == 0:
            self._curr_light_index = (self._curr_light_index + 1) % len(self._lights)
            res = self._lights[self._curr_light_index]
        else:
            res = self._current_light

        self.__time_count += 1

        return res
