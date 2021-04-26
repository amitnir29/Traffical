from __future__ import annotations

from math import sqrt
from typing import List, Optional, Tuple

from cars.car_state import CarState
from cars.i_car import ICar
from cars.position import Position
from geometry.line import Line
from geometry.point import Point
from iteration_trackable import iteration_trackable
from roadsections.i_road_section import IRoadSection
from trafficlights.i_traffic_light import ITrafficLight


class Car(ICar):
    def __init__(self, length: float, width: float, max_speed: float, max_speed_change: float, path: List[IRoadSection],
                 destination: Position):
        # TODO enter values
        self.__state = CarState()
        self.__length = length
        self.__width = width
        self.__path = path
        self.__destination = destination
        self.__max_speed = max_speed
        self.__speed = 0
        self.__max_speed_change = max_speed_change  # acceleration/decceleration
        self.__acceleration = 0

        assert len(path) > 0
        initial_road_section = path[0]
        self._enter_road_section(initial_road_section, initial_road_section.get_most_right_lane_index())

    @property
    def speed(self) -> float:
        return self.__speed

    def activate(self):
        """
        this is the main function of the car.
        the function evaluates the state of the car relative to other cars, red lights, lane switching etc.
        then, the function uses a function for the correct state.
        """
        state = self.get_state()

        self._set_acceleration()  # TODO this method should only control acceleration
        self._update_speed()
        self._advance()

    def _update_speed(self):
        self.__speed += self.__acceleration
        self.__acceleration = min(self.__acceleration, self.__current_road.max_speed - self.__speed)

    def get_state(self) -> CarState:
        # if we cant move from this lane to the next RoadSection in our path:
        pass

    def _full_gass(self):
        if self.speed + self.__max_speed_change <= self.__current_road.max_speed:
            self.__acceleration = self.__max_speed_change
        else:
            self.__acceleration = self.__current_road.max_speed - self.speed

    def _set_acceleration(self):
        front_car = self.__current_lane.get_car_ahead(self)
        red_light = self.get_closest_red_light()

        if front_car is None:
            if red_light is None or red_light.can_pass:
                # update speed s.t. we do not pass the max speed and the max acceleration.
                self._full_gass()
            else:
                # there is a red light.
                # update speed s.t. we do not pass the max speed, max deceleration, and light distance
                self.stop(self.__distance_from_lane_end)
        else:
            # we are not alone in the path
            # TODO fix all pass ifs, and fix the ICar interface s.t. we can apply front_car_speed on ICar
            front_car_speed, is_front_car_speed_real = self._front_car_speed(front_car)
            if red_light is None:
                if is_front_car_speed_real:
                    # calculate next speed s.t. we do not pass the:
                    # max speed, max de/acceleration, safe distance from car.
                    pass
                else:
                    # calculate next speed s.t. we do not pass the:
                    # max speed, max de/acceleration, safe distance from car.
                    # using estimated speed
                    pass
            else:
                # we are not first and there is a red light.
                if is_front_car_speed_real:
                    # calculate next speed s.t.we do not pass the:
                    # max speed, max de/acceleration, safe distance from car.
                    # also handle the red light deceleration.
                    pass
                else:
                    # calculate next speed s.t.we do not pass the:
                    # max speed, max de/acceleration, safe distance from car.
                    # also handle the red light deceleration.
                    # using estimated speed
                    pass
        # now we should also depend on lane switching.
        pass

    @property
    def position(self):
        return self.__position

    def _enter_road_section(self, road: IRoadSection, lanes_from_left: int):
        self.__current_road = road
        self.__current_lane = road.get_lane(lanes_from_left)
        self.__current_lane_part = 0
        self.__distance_from_lane_end = ... # TODO

    def stop(self, location: float):
        self.__state.stopping = True
        position_in_lane = self.__current_lane.car_position_in_lane(self)

        # We want, where currentPosition = location then speed = 0
        # Gives us:
        # 0 = speed + a * t
        # location - currentPosition = speed * t + 0.5 * a * t ^ 2
        #
        # Results in:
        # a = -speed ^ 2 / (2 * (location - currentPosition))

        self.__acceleration = -pow(self.__speed, 2) / (2 * (location - position_in_lane))

    def _is_car_done_this_iter(self, test_car: ICar) -> bool:
        """
        :param test_car: input car
        :return: true if the input car has already done this iteration.
        """
        return test_car.iteration == self.iteration + 1

    def estimated_speed(self) -> float:
        """
        :return: estimated speed that the car will have in this iteration
        """
        return self.__speed + self.__acceleration

    def distance_to_light(self, light: ITrafficLight) -> float:
        """
        not trivial - should depend on the shapes of the road parts in the way to the end of the road
        :param light: a traffic light on the path
        :return: distance to the input light
        """
        pass

    def _front_car_speed(self, front: ICar) -> Tuple[float, bool]:
        """
        :param front: car in front of self
        :return: (real speed, True) if already calculated. (estimated velocity, False) if not calculated.
        """
        if self._is_car_done_this_iter(front):
            return front.speed, True
        return front.estimated_speed(), False

    def get_closest_red_light(self) -> Optional[ITrafficLight]:
        """
        should also depend on lane switching.
        :return: closest red light that affects the car.
        """
        pass

    def move_in_part(self, dist_to_move: float) -> float:
        """
        move forward in the part of the lane
        :param dist_to_move: the distance to move
        :return: the distance left to move, if got to end of part. 0 if finished inside the part.
        """
        # We have the current part of the road, calculate the line to the next part.
        # We want to meet the next part's start line at the middle of the line.
        next_line_points: Tuple[Point, Point] = self.__current_road.coordinates[self.__current_lane_part + 1]
        next_line: Line = Line(next_line_points[0], next_line_points[1])
        # TODO not completely currect. should be relative to the lane, and not the whole road's width
        next_middle: Point = next_line.middle()
        moving_line: Line = Line(self.position, next_middle)
        dist: float = moving_line.length()
        if dist > dist_to_move:  # great, move just along the line
            self.__position = moving_line.split_by_ratio(dist_to_move / dist)
            return 0

        # else, move to next_middle and return distance left
        self.__position = Position(next_middle.x, next_middle.y)
        self.__current_lane_part += 1
        return dist_to_move - dist

    def move_in_lane(self, dist_to_move: float) -> float:
        """
        move through the parts of the lane until we finished the distance or the lane.
        :param dist_to_move: the distance to move
        :return: the distance left to move, if got to end of the lane. 0 if finished inside the lane.
        """
        dist_left = dist_to_move
        number_of_parts = len(self.__current_road.coordinates)

        while dist_left > 0 and self.__current_lane_part < number_of_parts - 1:
            # continue while we have distance to cover and parts to move forward to
            dist_left = self.move_in_part(dist_left)

        # return the distance left. if it is 0, we are done. else, we have to move to the next road.
        return dist_left

    def should_move_lane(self) -> bool:
        curr_road_index = self.__path.index(self.__current_road)
        if curr_road_index == len(self.__path) - 1:
            return False
        next_road = self.__path[curr_road_index + 1]
        return self.__current_lane.is_going_to_road(next_road)
