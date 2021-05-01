from abc import ABC, abstractmethod


class Drawable(ABC):
    @abstractmethod
    def draw(self, screen, scale):
        """
        draw the object on the window
        """
        pass

    @staticmethod
    @abstractmethod
    def from_server_obj(obj):
        """
        create a drawable from the matching server object
        :param obj: the server object
        :return: the drawable object
        """
        pass
