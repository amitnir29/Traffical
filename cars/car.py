from __future__ import annotations

from typing import List

from cars.car_state import CarState
from cars.i_car import ICar
from cars.position import Position
from iteration_trackable import iteration_trackable
from roadsections.i_road_section import IRoadSection
from trafficlights.i_traffic_light import ITrafficLight


# access using self.iteration
@iteration_trackable
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
        self._enter_road_section(path[0], 0)

    def activate(self):
        """
        this is the main function of the car.
        the function evaluates the state of the car relative to other cars, red lights, lane switching etc.
        then, the function uses a function for the correct state.
        """
        state = self.get_state()

        self.move_forward()

    def get_state(self) -> CarState:
        # if we cant move from this lane to the next RoadSection in our path:

        pass

    def move_forward(self) -> None:
        front_car: ICar = self.get_next_car()
        red_light: ITrafficLight = self.get_closest_red_light()
        next_speed: float = None
        if front_car is None:
            if red_light is None:
                # update speed s.t. we do not pass the max speed and the max acceleration.
                next_speed = min(self.speed + self.__max_speed_change, self.__current_road.max_speed)
            else:
                # there is a red light.
                # update speed s.t. we do not pass the max speed, max deceleration, and light distance
                next_speed = self.get_valid_speed(self.distance_to_light(red_light))
        else:
            # we are not alone in the path
            # TODO fix all pass ifs, and fix the ICar interface s.t. we can apply front_car_speed on ICar
            front_car_speed, is_front_car_speed_real = self.front_car_speed(front_car)
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
        self.__position = Position(0, 0)  # TODO change
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

        self.__acceleration = -pow(self.__speed, 2) / (2 * (location - position_in_lane))

    def get_valid_speed(self, distance: float) -> float:
        """
        get a valid speed s.t. we do not pass the max speed, max deceleration,
        and can be able to stop by the input distance (possibly in next iters).
        :param distance: distance to
        :return: the speed to have
        """
        pass

    def is_car_done_this_iter(self, test_car: Car) -> bool:
        """
        something like:
        return testCar.iteration == this.iteration;
        //else, testCar.iteration == this.iteration-1.
        :param test_car: input car
        :return: true if the input car has already done this iteration.
        """
        pass

    def estimated_speed(self) -> float:
        """
        :return: estimated speed that the car will have in this iteration
        """
        pass

    def distance_to_light(self, light: ITrafficLight) -> float:
        """
        not trivial - should depend on the shapes of the road parts in the way to the end of the road
        :param light: a traffic light on the path
        :return: distance to the input light
        """
        pass

    def front_car_speed(self, front: Car) -> (float, bool):
        """
        :param front: car in front of self
        :return: (real speed, True) if already calculated. (estimated velocity, False) if not calculated.
        """
        if self.is_car_done_this_iter(front):
            return front.__speed, True
        return front.estimated_speed(), False

    def get_closest_red_light(self) -> Optional[ITrafficLight]:
        """
        should also depend on lane switching.
        :return: closest red light that affects the car.
        """
        pass

    def get_next_car(self) -> Optional[ICar]:
        """
        dependent also on lane switchig.
        :return: next car for us. None if no car at all in the path until the destination
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
            """
            calculate the new position:
            we are at pos = (x', y'). we have a movement line y=mx+b.
            we want to move distToMove along the line towards the other point.
            destination is a point (x,mx+b) s.t. the distance from curr pos to it is distToMove.
            we will have 2 result points - 2 different directions of movement along the line.
            we will choose the one that is closer to the othe point.

            d = sqrt((x-x')^2+(mx+b-y')^2) = sqrt(x^2-2xx'+x'^2+(mx)^2+b^2+y'^2+2mxb-2mxy-2by)
            x^2-2xx'+x'^2+(mx)^2+b^2+y'^2+2mxb-2mxy'-2by' = d^2
            x^2*(1+m^2)+x*(2mb-2my'-2x')+(x'^2+b^2+y'^2-2by-d^2) = 0

            delta = (2mb-2my'-2x')^2-4*(1+m^2)*(x'^2+b^2+y'^2-2by-d^2)
            x1,2 = (-(2mb-2my'-2x')+-sqrt(delta))/(2*(1+m^2))

            choose xi that is closer to nextMiddle
            """
            m = moving_line.m
            b = moving_line.b
            xt = self.position.x
            yt = self.position.y

            quad_a: float = 1 + m ** 2
            quad_b = 2 * b * m - 2 * m * yt - 2 * xt
            quad_c = xt ** 2 + b ** 2 + yt ** 2 - 2 * b * yt - dist_to_move ** 2
            delta = quad_b ** 2 - 4 * quad_a * quad_c

            x1 = (-quad_b + sqrt(delta)) / (2 * quad_a)
            x2 = (-quad_b - sqrt(delta)) / (2 * quad_a)

            dest1 = Point(x1, m * x1 + b)
            dest2 = Point(x2, m * x2 + b)

            if next_middle.distance(dest1) < next_middle.distance(dest2):
                self.__position = Position(dest1.x, dest1.y)
            else:
                self.__position = Position(dest2.x, dest2.y)
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
        dist_left = self.move_in_part(dist_to_move)
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
