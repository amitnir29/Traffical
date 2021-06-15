from abc import ABC, abstractmethod


class TLManager(ABC):
    def __init__(self, junction):
        self._junction = junction
        self._lights = self._junction.lights
        self.init_lights()

        self._current_light = self._lights[0] if len(self._lights) > 0 else None

    @abstractmethod
    def _manage_lights(self):
        raise NotImplemented

    def manage_lights(self):
        """
        update the traffic lights
        """
        if len(self._lights) > 0:
            new_green = self._manage_lights()
            if new_green != self._current_light:
                self._current_light.change_light(False)  # to red
                new_green.change_light(True)  # to green

                self._current_light = new_green

    def init_lights(self):
        if len(self._lights) > 0:
            self._lights[0].change_light(True)