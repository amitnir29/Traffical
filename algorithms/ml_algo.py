import pickle

import numpy as np
import pandas as pd

from algorithms.algo_to_index import index_to_algo, algos_list_to_num
from algorithms.naive import NaiveAlgo
from algorithms.tl_manager import TLManager

from server.simulation_objects.lanes.lane import Lane
from server.simulation_objects.trafficlights.traffic_light import TrafficLight


class MLAlgo(TLManager):
    def __init__(self, junction, model_path, time_limit=np.inf, depth=2, time_interval=40):
        super().__init__(junction, time_limit)

        with open(model_path, "rb") as model_file:
            self.model = pickle.load(model_file)
        self.depth = depth
        self.time_interval = time_interval

        self._time_count = 0
        self.running_algo: TLManager = NaiveAlgo(junction)

    @staticmethod
    def expected_traffic(tl: TrafficLight, depth):
        return sum(MLAlgo.expected_traffic_per_lane(lane, depth) for lane in tl.lanes)

    @staticmethod
    def expected_traffic_per_lane(lane: Lane, depth):
        prev_lanes = lane._comes_from
        traff = sum(len(prev_lane.get_all_cars()) for prev_lane in prev_lanes)

        if depth > 0:
            expected_traff = sum(MLAlgo.expected_traffic_per_lane(prev_lane, depth - 1) for prev_lane in prev_lanes)
            return traff + expected_traff

        return traff

    def _predict(self):
        def padd(arr):
            return arr + [0] * (4 - len(arr))

        local_traffics = padd([len(tl.all_cars) for tl in self._lights])
        local_traffics = {f"local_traffic{i}": traffic for i, traffic in enumerate(local_traffics)}

        expected_traffic = padd([MLAlgo.expected_traffic(tl, depth=self.depth - 1) for tl in self._lights])
        expected_traffic = {f"expected_traffic{i}": traffic for i, traffic in enumerate(expected_traffic)}

        nearby_junctions_algos = padd(
            [algos_list_to_num(
                [lane._comes_from_junction._algo for lane in tl.lanes if lane._comes_from_junction is not None]) for tl
             in self._lights])
        nearby_junctions_algos = {f"nearby_algos{i}": algos for i, algos in enumerate(nearby_junctions_algos)}

        predict_input = {**{**local_traffics, **expected_traffic}, **nearby_junctions_algos,
                         "time_interval": self.time_interval}

        predict_input = pd.DataFrame(predict_input, index=[0])

        self.running_algo: TLManager = index_to_algo.get(self.model.predict(predict_input)[0], self.running_algo)

        return self.running_algo(self._junction)._manage_lights()

    def _manage_lights(self):
        if self._time_count % self.time_interval == 0:
            res = self._predict()
        else:
            res = self._current_light

        self._time_count += 1
        return res
