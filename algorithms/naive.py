from algorithms.tl_manager import TLManager


class NaiveAlgo(TLManager):
    def __init__(self, junction, light_interval=10):
        super().__init__(junction)
        self.__time_count = 0
        self.__light_interval = light_interval
        self.init_lights()
        self._curr_light = 0

    def manage_lights(self):
        if len(self._lights) > 1:

            if self.__time_count % self.__light_interval == 0:
                self._lights[self._curr_light].change_light(False)
                self._lights[(self._curr_light + 1) % len(self._lights)].change_light(True)

                self._curr_light += 1
                self._curr_light %= len(self._lights)

        self.__time_count += 1