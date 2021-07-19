from __future__ import annotations

from copy import deepcopy
from math import atan, degrees
from typing import List, Optional, Tuple

from server.geometry.line import Line
from server.geometry.point import Point
from server.simulation_objects.cars.car_state import CarState
from server.simulation_objects.cars.i_car import ICar
from server.simulation_objects.cars.position import Position
from server.simulation_objects.lanes.i_lane import ILane
from server.simulation_objects.lanes.notified_lane import NotifiedLane
from server.simulation_objects.roadsections.i_road_section import IRoadSection
from server.simulation_objects.trafficlights.i_traffic_light import ITrafficLight


class Car(ICar):
    MIN_DISTANCE_TO_KEEP = ...  # TODO
    MIN_DISTANCE_CONFIDENCE_INTERVAL = ...  # Todo

    # TODO temp values
    def __init__(self, path: List[IRoadSection], initial_distance: float = 0,
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

        assert len(path) > 0
        initial_road_section = path[0]

        self.__current_lane: ILane = None
        self._enter_road_section(initial_road_section, initial_distance)

        self.__speed = max_speed  # TODO remove

    def _enter_road_section(self, road: IRoadSection, initial_distance: float = 0):
        if self.__current_lane is not None:
            self.__current_lane.remove_car(self)
        self.__current_road = road
        self.__next_road_idx += 1
        self.__current_lane = road.get_lane(road.get_most_right_lane_index())
        self.__current_lane.add_car(self)
        self.__current_lane_part = 0
        # put on the initial_distance from start of the road
        assert initial_distance <= self.__current_lane.lane_length()
        # TODO change, it is currently on initial_distance=0:
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
            if front_car is None:
                if red_light is None or red_light.can_pass:
                    # update speed s.t. we do not pass the max speed and the max acceleration.
                    self._full_gass()
                else:
                    # there is a red light.
                    # update speed s.t. we do not pass the max speed, max deceleration, and light distance
                    lane_end_coordinates = self.__current_lane.coordinates[-1]
                    distance_to_stop = self._distance_to_part_end(self.position, lane_end_coordinates)
                    self._stop(distance_to_stop)
            else:
                if self._is_car_done_this_iter(front_car) and (red_light is None or red_light.can_pass):
                    # distance_to_keep = self.MIN_DISTANCE_TO_KEEP
                    distance_to_keep = self.__speed
                    distance_to_move = Line(self.position, front_car.position).length() - distance_to_keep

                else:
                    # TODO MIN DISTANCE depends on velocity
                    # distance_to_keep = self.MIN_DISTANCE_TO_KEEP + self.MIN_DISTANCE_CONFIDENCE_INTERVAL
                    distance_to_keep = self.__speed * 1.1
                    # TODO not completely correct. should be relative to the lane, and not the whole road's width
                    # part_end = Line(*self.__current_road.coordinates[self.__current_lane_part]).middle()

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
        # TODO improve
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

    def has_arrived_destination(self):
        # return True if passed the middle of the last road
        last_road = self.__path[-1]
        return self.__current_road == last_road

    def __repr__(self):
        return str([road for road in self.__path])

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
