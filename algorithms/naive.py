from algorithms.tl_manager import TLManager


class NaiveAlgo(TLManager):
    def get_tl_junctions(self):
        return [junc for junc in self._junctions if len(junc.lights) != 0]

    def get_lights_groups(self):
        max_lights = max(len(junc.lights) for junc in self._junctions)
        groups = list()
        for i in range(max_lights):
            groups.append(list())
            for junc in self._junctions:
                if len(junc.lights) >= i - 1:
                    groups[-1].append(junc.lights[i])
        return groups

    def init_lights(self):
        for tl in self.__light_groups[0]:
            tl.change_light()

    def __init__(self, traffic_lights, all_junctions):
        super().__init__(traffic_lights, all_junctions)
        self._junctions = self.get_tl_junctions()
        self.__light_groups = self.get_lights_groups()
        self.__time_count = 0
        self.init_lights()

    def manage_lights(self, cars):
        self.__time_count += 1
        curr_group = 0
        if self.__time_count % 10 == 0:
            for tl in self.__light_groups[curr_group]:
                tl.change_light()  # to red
            for tl in self.__light_groups[(curr_group + 1) % len(self.__light_groups)]:
                tl.change_light()  # to green
