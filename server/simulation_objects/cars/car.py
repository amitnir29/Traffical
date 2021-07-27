from __future__ import annotations

import copy
import math
from copy import deepcopy
from math import atan, degrees
from typing import List, Optional, Tuple

import numpy as np

from server.geometry.line import Line
from server.geometry.point import Point
from server.simulation_objects.cars.car_state import CarState
from server.simulation_objects.cars.i_car import ICar
from server.simulation_objects.cars.position import Position
from server.simulation_objects.lanes.lane import Lane
from server.simulation_objects.lanes.notified_lane import NotifiedLane
from server.simulation_objects.roadsections.i_road_section import IRoadSection
from server.simulation_objects.trafficlights.i_traffic_light import ITrafficLight


class Car(ICar):
    next_car_index = 0

    def __init__(self, path: List[IRoadSection],
                 max_speed: float = 30,
                 max_speed_change: float = 10):
        self.__max_speed = max_speed
        self.__max_speed_change = max_speed_change  # acceleration/decceleration
        # initial car start state
        self.__speed = 0
        self.__acceleration = 0
        self.__state = CarState()
        # initial_distance and destination are distances from start of the source/target roads
        self.__path = path
        self.__next_road_idx = 0
        self.__idx = Car.next_car_index
        Car.next_car_index += 1
        self.__position = None
        self.__current_road = None
        self.__current_lane = None
        assert len(path) > 0

        self.__speed = 0

    def __deepcopy__(self, memodict={}):
        res = Car.__new__(Car)
        res.__dict__ = copy.copy(self.__dict__)

        res.__position = copy.copy(self.position)
        res.__current_road = deepcopy(self.__current_road)
        res.__current_lane = deepcopy(self.__current_lane)
        res.__path = deepcopy(self.__path)
        if self.__current_lane is not None:
            res.__current_lane._cars.appendleft(res)

        return res

    def enter_first_road(self):
        self._enter_road_section(self.__path[0])

    def _enter_road_section(self, road: IRoadSection, initial_distance: float = 0):
        if self.__current_lane is not None:
            self.__current_lane.remove_car(self)
        self.__current_road = road
        self.__next_road_idx += 1

        self.__current_lane = road.get_lane(self.__current_road.get_most_right_lane_index())

        self.__current_lane.add_car(self)
        self.__current_lane_part = 0
        # put on the initial_distance from start of the road
        assert initial_distance <= self.__current_lane.lane_length()
        self.__position = Line(*self.__current_lane.coordinates[0]).middle()
        self._advance(initial_distance)

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
        dist_left = self._move_in_lane(distance_to_move)

        while dist_left > 0:
            self.move_road_section()
            dist_left = self._move_in_lane(dist_left)

    def move_road_section(self):
        if self.__next_road_idx < len(self.__path):
            self._enter_road_section(self.__path[self.__next_road_idx])

    def _update_speed(self):
        self.__speed += self.__acceleration
        self.__speed = max(0, min(self.__speed, self.__max_speed))
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
        if self.__state.driving:
            if self._should_move_lane():
                self.move_lane(self.lane_to_move_in())
            elif front_car is None:
                if red_light is None or red_light.can_pass:
                    # update speed s.t. we do not pass the max speed and the max acceleration.
                    self._full_gass()
                else:
                    # there is a red light.
                    # update speed s.t. we do not pass the max speed, max deceleration, and light distance
                    lane_end_coordinates = self.__current_lane.coordinates[-1]
                    distance_to_stop = self._distance_to_part_end(self.position, lane_end_coordinates)

                    if self.__acceleration == 0:
                        if self.__speed == 0:
                            current_expected_distance_to_stop = 0
                        else:
                            current_expected_distance_to_stop = np.inf
                    else:
                        current_expected_distance_to_stop = -pow(self.__speed, 2) / (2 * self.__acceleration)

                    distance_in_full_gas = min(self.__speed + self.__max_speed_change, self.__current_road.max_speed)
                    if current_expected_distance_to_stop < distance_to_stop and distance_to_stop > distance_in_full_gas:
                        self._full_gass()
                    else:
                        self._stop(distance_to_stop)
            else:
                if self._is_car_done_this_iter(front_car) and (red_light is None or red_light.can_pass):
                    distance_to_keep = self.__speed + self.__current_lane.lane_length() / 10
                    distance_to_move = Line(self.position, front_car.position).length() - distance_to_keep

                else:
                    distance_to_keep = self.__speed * 1.1 + self.__current_lane.lane_length() / 10

                    simulation_car = deepcopy(front_car)
                    simulation_car._advance(simulation_car.estimated_speed())

                    estimated_front_car_pos = simulation_car.position

                    distance_to_move = Line(self.position, estimated_front_car_pos).length() - distance_to_keep

                required_speed = min(distance_to_move, self.__max_speed)
                self.__acceleration = min(required_speed - self.__speed, self.__max_speed_change)
        self.__acceleration = min(self.__acceleration, self.__max_speed_change)

    @property
    def position(self):
        return self.__position

    def _stop(self, distance: float):
        self.__state.stopping = True

        # We want, where currentPosition = location then speed = 0
        # Gives us:
        # 0 = speed + a * t
        # location - currentPosition = speed * t + 0.5 * a * t ^ 2
        #
        # Results in:
        # a = -speed ^ 2 / (2 * (location - currentPosition))

        self.__acceleration = -pow(self.__speed, 2) / (2 * distance)

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
        if isinstance(self.__current_lane, NotifiedLane):
            return self.__current_lane.traffic_light
        return None

    @staticmethod
    def _distance_to_part_end(current_position: Point, coordinates: Tuple[Point, Point]) -> float:
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
        next_line_points = self.__current_lane.coordinates[self.__current_lane_part + 1]

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
        if self.__next_road_idx == len(self.__path):
            return False
        next_road = self.__path[self.__next_road_idx]
        return not self.__current_lane.is_going_to_road(next_road)

    def move_lane(self, lane):
        current_part_as_line = Lane.part_as_line(self.__current_lane.coordinates[self.__current_lane_part],
                                                 self.__current_lane.coordinates[self.__current_lane_part + 1])
        new_part_as_line = Lane.part_as_line(lane.coordinates[self.__current_lane_part],
                                             lane.coordinates[self.__current_lane_part + 1])

        self.__position = self._position_in_new_line(current_part_as_line, new_part_as_line)

        self.__current_lane.remove_car(self)
        self.__current_lane = lane

        before_car: Car = lane.get_car_before(self)
        lane.insert_before(self, before_car)

        if before_car is not None:
            before_car.wants_to_enter_lane(self)

        self.__state.moving_lane = lane

    @property
    def current_part_in_lane(self):
        return self.__current_lane_part

    def lane_to_move_in(self):
        if self.__next_road_idx == len(self.__path):
            return self.__current_lane

        next_road = self.__path[self.__next_road_idx]
        for lane in self.__current_road.lanes:
            if lane.is_going_to_road(next_road):
                return lane

        raise Exception

    def _position_in_new_line(self, current_line, line_to_move_to):
        x_current, y_current = self.position.to_tuple()
        m1 = current_line.m
        m2 = line_to_move_to.m
        b2 = line_to_move_to.b

        if m2 != math.inf and m2 != -math.inf and m1 * m2 != -1 and m1 != 0:
            x_expected = (x_current / m1 + y_current - b2) / (m2 + 1 / m1)
            y_expected = m2 * x_expected + b2
        elif m1 * m2 == -1:
            x_expected, y_expected = line_to_move_to.p1
        elif m1 == 0:
            x_expected = x_current
            y_expected = m2 * x_expected + b2
        else:
            x_expected = line_to_move_to.p1.x
            y_expected = -x_expected / m1 + x_current / m1 + y_current

        return Position(x_expected, y_expected)

    def wants_to_enter_lane(self, car: Car) -> None:
        # current_part_as_line = Lane.part_as_line(self.__current_lane.coordinates[self.__current_lane_part],
        #                                          self.__current_lane.coordinates[self.__current_lane_part + 1])
        # cars_line = Lane.part_as_line(*car.__current_lane.coordinates[car.__current_lane_part])
        # expected_position = car._position_in_new_line(cars_line, current_part_as_line)
        path_to_move = Line(self.position, car.position)

        self._stop(path_to_move.length())

    def has_arrived_destination(self):
        last_road = self.__path[-1]
        return self.__current_road == last_road

    def reached_destination(self):
        self.__current_lane.remove_car(self)

    def __repr__(self):
        return f"Car:{self.get_id()}, at: {self.position}"

    def get_angle(self):
        # the line from the middle of the start of the current part, to the middle of the end of the current part
        curr_line = Line(
            Line(*self.__current_lane.coordinates[self.__current_lane_part]).middle(),
            Line(*self.__current_lane.coordinates[self.__current_lane_part + 1]).middle())
        x_diff = curr_line.p2.x - curr_line.p1.x
        y_diff = curr_line.p1.y - curr_line.p2.y  # y axis is upside down
        if x_diff == 0:
            if y_diff > 0:
                return 0
            else:
                return 180
        res = (90 - degrees(atan(y_diff / x_diff))) % 360
        if x_diff < 0:
            res = 180 - res
        if x_diff > 0:
            res = 360 - res
        return res

    def get_speed(self):
        return self.__speed

    def get_acceleration(self):
        return self.__acceleration

    def get_id(self):
        return self.__idx

    def car_with_same_path(self) -> ICar:
        return Car(self.__path)

    def is_waiting(self):
        return self.__speed < 0.01
