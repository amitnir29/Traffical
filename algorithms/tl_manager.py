from abc import ABC, abstractmethod


class TLManager(ABC):
    def __init__(self, traffic_lights, all_junctions):
        self._traffic_lights = traffic_lights
        self._junctions = all_junctions

    @abstractmethod
    def manage_lights(self, cars):
        """
        update the traffic lights
        :param cars: all cars in the simulation
        """
        pass
