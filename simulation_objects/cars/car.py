from __future__ import annotations

from typing import List, Optional, Tuple

from simulation_objects.cars.car_state import CarState
from simulation_objects.cars.i_car import ICar
from simulation_objects.cars.position import Position
from simulation_objects.geometry.line import Line
from simulation_objects.geometry.point import Point
from simulation_objects.roadsections.i_road_section import IRoadSection
from simulation_objects.trafficlights.i_traffic_light import ITrafficLight


class Car(ICar):
    MIN_DISTANCE_TO_KEEP = ...  # TODO
    MIN_DISTANCE_CONFIDENCE_INTERVAL = ...  # Todo

    def __init__(self, length: float, width: float, max_speed: float, max_speed_change: float,
                 initial_position: Position, path: List[IRoadSection],
                 destination: Position):
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

    def activate(self):
        """
        this is the main function of the car.
        the function evaluates the state of the car relative to other cars, red lights, lane switching etc.
        then, the function uses a function for the correct state.
        """
        self._set_acceleration()
        self._update_speed()
        self._advance(self.__speed)

    def _advance(self, distance_to_move):
        dist_left = distance_to_move
        self._move_in_lane(dist_left)

        while dist_left > 0:
            self.move_lane()
            self._move_in_lane(dist_left)

    def _update_speed(self):
        self.__speed += self.__acceleration
        self.__acceleration = min(self.__acceleration, self.__current_road.max_speed - self.__speed)

    def _full_gass(self):
        if self.__speed + self.__max_speed_change <= self.__current_road.max_speed:
            self.__acceleration = self.__max_speed_change
        else:
            self.__acceleration = self.__current_road.max_speed - self.__speed

    def _set_acceleration(self):
        front_car = self.__current_lane.get_car_ahead(self)
        red_light = self._get_closest_traffic_light()

        if self.__state.moving_lane == self.__current_lane:
            # Already moved lane
            self.__state.moving_lane = None
        if self.__state.stopping and (self.__speed == 0 or (red_light is not None and red_light.can_pass)):
            self.__state.stopping = False
        if front_car == self.__state.letting_car_in:
            # The car already moved into the lane
            self.__state.letting_car_in = None
        if self.__state.driving:  # Equivalent to else
            if front_car is None:
                if red_light is None or red_light.can_pass:
                    # update speed s.t. we do not pass the max speed and the max acceleration.
                    self._full_gass()
                else:
                    # there is a red light.
                    # update speed s.t. we do not pass the max speed, max deceleration, and light distance
                    lane_end_coordinates = self.__current_road.coordinates[-1]
                    distance_to_stop = self._distance_to_part_end(self.position, lane_end_coordinates)
                    self._stop(distance_to_stop)
            else:
                if self._is_car_done_this_iter(front_car) and (red_light is None or red_light.can_pass):
                    distance_to_keep = self.MIN_DISTANCE_TO_KEEP
                    distance_to_move = Line(self.position, front_car.position).length() - distance_to_keep

                else:
                    # TODO MIN DISTANCE depends on velocity
                    distance_to_keep = self.MIN_DISTANCE_TO_KEEP + self.MIN_DISTANCE_CONFIDENCE_INTERVAL
                    # TODO not completely correct. should be relative to the lane, and not the whole road's width
                    part_end = Line(*self.__current_road.coordinates[self.__current_lane_part]).middle()

                    estimated_front_car_speed = front_car.estimated_speed()
                    front_car_path = Line(front_car.position, part_end)
                    estimated_front_car_pos = front_car_path.split_by_ratio(
                        estimated_front_car_speed / front_car_path.length())
                    distance_to_move = Line(self.position, estimated_front_car_pos).length() - distance_to_keep

                required_speed = min(distance_to_move, self.__max_speed)
                self.__acceleration = min(required_speed - self.__speed, self.__max_speed_change)

    @property
    def position(self):
        return self.__position

    def _enter_road_section(self, road: IRoadSection, lanes_from_left: int):
        self.__current_road = road
        self.__current_lane = road.get_lane(lanes_from_left)
        self.__current_lane_part = 0

    def _stop(self, location: float):
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

    def _get_closest_traffic_light(self) -> Optional[ITrafficLight]:
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

    def _move_in_part(self, dist_to_move: float) -> float:
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

    def _move_in_lane(self, dist_to_move: float) -> float:
        """
        move through the parts of the lane until we finished the distance or the lane.
        :param dist_to_move: the distance to move
        :return: the distance left to move, if got to end of the lane. 0 if finished inside the lane.
        """
        dist_left = dist_to_move
        number_of_parts = len(self.__current_road.coordinates)

        while dist_left > 0 and self.__current_lane_part < number_of_parts - 1:
            # continue while we have distance to cover and parts to move forward to
            dist_left = self._move_in_part(dist_left)

        # return the distance left. if it is 0, we are done. else, we have to move to the next road.
        return dist_left

    def _should_move_lane(self) -> bool:
        curr_road_index = self.__path.index(self.__current_road)
        if curr_road_index == len(self.__path) - 1:
            return False
        next_road = self.__path[curr_road_index + 1]
        return self.__current_lane.is_going_to_road(next_road)

    @property
    def current_part_in_lane(self):
        return self.__current_lane_part

    def wants_to_enter_lane(self, car: ICar) -> None:
        pass
