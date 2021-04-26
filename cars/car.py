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
    MIN_DISTANCE_TO_KEEP = ... #TODO
    MIN_DISTANCE_CONFIDENCE_INTERVAL = ... #Todo

    def __init__(self, length: float, width: float, max_speed: float, max_speed_change: float,
                 initial_position: Position, path: List[IRoadSection],
                 destination: Position):
        # TODO enter values
        self.__state = CarState()
        self.__length = length
        self.__width = width
        self.__path = path
        self.__position = initial_position
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
                lane_end_coordinates = self.__current_road.coordinates[-1]
                distance_to_stop = self._distance_to_part_end(self.position, lane_end_coordinates)
                self.stop(distance_to_stop)
        else:
            if self._is_car_done_this_iter(front_car) and (red_light is None or red_light.can_pass):
                distance_to_keep = self.MIN_DISTANCE_TO_KEEP
                distance_to_move = Line(self.position, front_car.position).length() - distance_to_keep

            else:
                distance_to_keep = self.MIN_DISTANCE_TO_KEEP + self.MIN_DISTANCE_CONFIDENCE_INTERVAL
                # TODO not completely correct. should be relative to the lane, and not the whole road's width
                part_end = Line(*self.__current_road.coordinates[self.__current_lane_part]).middle()

                estimated_front_car_speed = front_car.estimated_speed()
                front_car_path = Line(front_car.position, part_end)
                estimated_front_car_pos = front_car_path.split_by_ratio(estimated_front_car_speed / front_car_path.length())
                distance_to_move = Line(self.position, estimated_front_car_pos).length() - distance_to_keep

            required_speed = min(distance_to_move, self.__max_speed)
            self.__acceleration = min(required_speed - self.__speed, self.__max_speed_change)
        # now we should also depend on lane switching.
        pass

    @property
    def position(self):
        return self.__position

    def _enter_road_section(self, road: IRoadSection, lanes_from_left: int):
        self.__current_road = road
        self.__current_lane = road.get_lane(lanes_from_left)
        self.__current_lane_part = 0

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

        self.__acceleration = max(-pow(self.__speed, 2) / (2 * (location - position_in_lane)), self.__max_speed_change)

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

    def get_closest_red_light(self) -> Optional[ITrafficLight]:
        """
        should also depend on lane switching.
        :return: closest red light that affects the car.
        """
        pass


    @staticmethod
    def _distance_to_part_end(current_position: Point, coordinates: Tuple[Point, Point]) -> float:
        # TODO not completely correct. should be relative to the lane, and not the whole road's width
        next_middle = Line(*coordinates).middle()
        path = Line(current_position, next_middle)

        return path.length()

    def move_in_part(self, dist_to_move: float) -> float:
        """
        move forward in the part of the lane
        :param dist_to_move: the distance to move
        :return: the distance left to move, if got to end of part. 0 if finished inside the part.
        """
        # We have the current part of the road, calculate the line to the next part.
        # We want to meet the next part's start line at the middle of the line.
        next_line_points = self.__current_road.coordinates[self.__current_lane_part + 1]

        next_middle = Line(*next_line_points).middle()
        path = Line(self.position, next_middle)
        dist = path.length()

        if dist > dist_to_move:
            self.__position = path.split_by_ratio(dist_to_move / dist)
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
