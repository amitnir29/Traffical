from abc import ABC, abstractmethod


class TLManager(ABC):
    def __init__(self, junction):
        self._junction = junction
        self._lights = self._junction.lights

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
