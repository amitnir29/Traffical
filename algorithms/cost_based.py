from collections import defaultdict

from algorithms.tl_manager import TLManager
import numpy as np

from server.simulation_objects.trafficlights.traffic_light import TrafficLight


class CostBased(TLManager):
    def __init__(self, junction, time_limit=np.inf, passing_carr_revenue=5, waiting_time_to_charge=5,
                 waiting_penalty=5):
        super().__init__(junction, time_limit)
        self.passing_car_revenue = passing_carr_revenue
        self.waiting_time_to_charge = waiting_time_to_charge
        self.waiting_penalty = waiting_penalty

        self.time_tracker = defaultdict(int)

    def _cost_for_tl(self, tl: TrafficLight):
        all_cars = sum(
            [sum([[car for car in lane.get_all_cars()] for lane in tl.lanes], []) for tl in self._junction.lights],
            [])
        cars_per_lane_in_green_tl = [[car for car in lane.get_all_cars()] for lane in tl.lanes]
        passing_cars = [cars[0] for cars in cars_per_lane_in_green_tl if len(cars) > 0]

        passing_cars_gain = self.passing_car_revenue * len(passing_cars)

        waiting_cars_punishment = self.waiting_penalty * len([car for car in all_cars if car not in passing_cars and self.time_tracker[
            car] % self.waiting_time_to_charge == 0])

        # passing_cars_gain = sum(lane.cars_amount() for lane in tl.lanes) * self.passing_car_revenue  # TODO fix
        #
        # waiting_cars_punishment = sum(len([car for car in lane.cars_from_end(lane.lane_length()) if
        #                                    self.time_tracker[car] % self.waiting_time_to_charge == 0]) for lane in
        #                               tl.lanes if lane != tl) * self.waiting_penalty  # TODO fix

        return passing_cars_gain - waiting_cars_punishment

    def _track_time(self):
        all_cars = sum(
            [sum([[car for car in lane.get_all_cars()] for lane in tl.lanes], []) for tl in self._junction.lights],
            [])
        for car in self.time_tracker.keys() - set(all_cars):
            self.time_tracker.pop(car)

        for car in all_cars:
            self.time_tracker[car] += 1

    def _manage_lights(self):
        self._track_time()

        return max(self._junction.lights, key=self._cost_for_tl)
