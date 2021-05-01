from abc import ABC, abstractmethod


class Drawable(ABC):
    @abstractmethod
    def draw(self, screen, scale):
        """
        draw the object on the window
        """
        pass
