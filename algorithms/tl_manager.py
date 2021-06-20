from abc import ABC, abstractmethod
import numpy as np


class TLManager(ABC):
    def __init__(self, junction, time_limit=np.inf):
        self._junction = junction
        self._lights = self._junction.lights
        self.init_lights()

        self._current_light = self._lights[0] if len(self._lights) > 0 else None
        self._time_limit = time_limit

    @abstractmethod
    def _manage_lights(self):
        raise NotImplemented

    def manage_lights(self):
        """
        update the traffic lights
        """
        if len(self._lights) > 0:
            # also, check if there is a light that has been red for too long
            waiting_longest = max([tl for tl in self._junction.lights if tl != self._current_light],
                                  key=lambda tl: tl.light_time)
            if waiting_longest.light_time > self._time_limit:
                new_green = waiting_longest
            else:
                new_green = self._manage_lights()

            if new_green != self._current_light:
                self._current_light.change_light(False)  # to red
                new_green.change_light(True)  # to green

                self._current_light = new_green

    def init_lights(self):
        if len(self._lights) > 0:
            self._lights[0].change_light(True)
