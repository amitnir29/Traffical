from abc import ABC, abstractmethod


class TLManager(ABC):
    def __init__(self, traffic_lights, all_junctions):
        self._traffic_lights = traffic_lights
        self._junctions = all_junctions
        self._tl_junctions = self.get_tl_junctions()

    @abstractmethod
    def manage_lights(self, cars):
        """
        update the traffic lights
        :param cars: all cars in the simulation
        """
        pass

    @abstractmethod
    def init_lights(self):
        pass

    def get_tl_junctions(self):
        return [junc for junc in self._junctions if len(junc.lights) != 0]
