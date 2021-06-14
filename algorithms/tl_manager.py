from abc import ABC, abstractmethod


class TLManager(ABC):
    def __init__(self, junction):
        self._junction = junction
        self._lights = self._junction.lights
        self.init_lights()

        self._current_light = self._lights[0] if len(self._lights) > 0 else None

    @abstractmethod
    def manage_lights(self):
        """
        update the traffic lights
        :param cars: all cars in the simulation
        """
        pass

    def init_lights(self):
        if len(self._lights) > 0:
            self._lights[0].change_light(True)