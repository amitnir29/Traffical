from algorithms.tl_manager import TLManager


class NaiveAlgo(TLManager):

    def __init__(self, traffic_lights, all_junctions, light_interval=10):
        super().__init__(traffic_lights, all_junctions)
        self.__light_groups = self.get_lights_groups()
        self.__time_count = 0
        self.__light_interval = light_interval
        self.__curr_group = 0
        self.init_lights()

    def init_lights(self):
        for tl in self.__light_groups[0]:
            tl.change_light()

    def get_lights_groups(self):
        max_lights = max(len(junc.lights) for junc in self._tl_junctions)
        groups = list()
        for i in range(max_lights):
            groups.append(list())
            for junc in self._tl_junctions:
                if len(junc.lights) >= i - 1:
                    groups[-1].append(junc.lights[i])
        return groups

    def manage_lights(self, cars):
        self.__time_count += 1
        if self.__time_count % self.__light_interval == 0:
            for tl in self.__light_groups[self.__curr_group]:
                tl.change_light(False)  # to red
            for tl in self.__light_groups[(self.__curr_group + 1) % len(self.__light_groups)]:
                tl.change_light(True)  # to green
            self.__curr_group = (self.__curr_group + 1) % len(self.__light_groups)
