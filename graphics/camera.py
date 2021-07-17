from dataclasses import dataclass

from server.geometry.line import Line
from server.geometry.point import Point


@dataclass(init=True, repr=True)
class Camera:
    min_x: int
    min_y: int
    max_x: int
    max_y: int
    width: int
    height: int
    ratio_to_change_size = 1.2
    ratio_towards_new_center = 0.25
    arrow_press_move_ratio = 0.2

    @property
    def delta_x(self):
        return self.max_x - self.min_x

    @property
    def delta_y(self):
        return self.max_y - self.min_y

    @property
    def center_x(self):
        return self.min_x + self.delta_x // 2

    @property
    def center_y(self):
        return self.min_y + self.delta_y // 2

    def zoom_in(self, x: int, y: int):
        """
        zoom the camera in, centered at closer to x,y (relative to current camera position,
        and dependent on ratio_towards_new_center) and range smaller by ratio
        """
        # set x,y to be relative to current camera position
        relative_x = self.min_x + (x * self.delta_x) // self.width
        relative_y = self.min_y + (y * self.delta_y) // self.height
        # shrink the delta
        delta_x = self.delta_x / self.ratio_to_change_size
        delta_y = self.delta_y / self.ratio_to_change_size
        # calculate new centers
        center_x, center_y = Line(Point(self.center_x, self.center_y), Point(relative_x, relative_y)) \
            .split_by_ratio(self.ratio_towards_new_center).to_tuple()
        # set new values
        self.min_x = center_x - delta_x // 2
        self.max_x = center_x + delta_x // 2
        self.min_y = center_y - delta_y // 2
        self.max_y = center_y + delta_y // 2

    def zoom_out(self, x: int, y: int):
        """
        zoom the camera out, centered at closer to x,y (relative to current camera position,
        and dependent on ratio_towards_new_center, and total width,height) and range higher by ratio
        """
        # set x,y to be relative to current camera position
        relative_x = self.min_x + (x * self.delta_x) // self.width
        relative_y = self.min_y + (y * self.delta_y) // self.height
        # increase the delta
        delta_x = min(self.ratio_to_change_size * self.delta_x, self.width)
        delta_y = min(self.ratio_to_change_size * self.delta_y, self.height)
        # calculate new centers
        center_x, center_y = Line(Point(self.center_x, self.center_y), Point(relative_x, relative_y)) \
            .split_by_ratio(self.ratio_towards_new_center).to_tuple()
        # move the camera to the side, if values are outside the total borders (0,0,width,height)
        min_x = center_x - delta_x // 2
        max_x = center_x + delta_x // 2
        min_y = center_y - delta_y // 2
        max_y = center_y + delta_y // 2
        if min_x < 0:
            max_x += abs(min_x)
            min_x = 0
        if max_x > self.width:
            min_x -= (max_x - self.width)
            max_x = self.width
        if min_y < 0:
            max_y += abs(min_y)
            min_y = 0
        if max_y > self.height:
            min_y -= (max_y - self.height)
            max_y = self.height
        # set new values
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    def up(self):
        movement = min(self.delta_y * self.arrow_press_move_ratio, self.min_y)
        self.min_y -= movement
        self.max_y -= movement

    def down(self):
        movement = min(self.delta_y * self.arrow_press_move_ratio, self.height - self.max_y)
        self.min_y += movement
        self.max_y += movement

    def left(self):
        movement = min(self.delta_x * self.arrow_press_move_ratio, self.min_x)
        self.min_x -= movement
        self.max_x -= movement

    def right(self):
        movement = min(self.delta_x * self.arrow_press_move_ratio, self.width - self.max_x)
        self.min_x += movement
        self.max_x += movement
