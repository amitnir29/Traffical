from algorithms.tl_manager import TLManager


class NaiveAlgo(TLManager):
    def __init__(self, junction, light_interval=10):
        super().__init__(junction)
        self.__time_count = 0
        self.__light_interval = light_interval
        self.init_lights()

    def init_lights(self):
        self._lights[0].change_light()
        for tl in self._lights[1:]:
            tl.change_light()

    def manage_lights(self, cars):
        curr_group = self.__time_count % len(self._lights)
        self.__time_count += 1

        if self.__time_count % self.__light_interval == 0:
            self._lights[curr_group].change_light(False)
            self._lights[curr_group].change_light(True)