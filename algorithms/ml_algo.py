import numpy as np
from sklearn.tree import DecisionTreeClassifier

from algorithms.algo_to_index import index_to_algo
from algorithms.naive import NaiveAlgo
from algorithms.tl_manager import TLManager
import pandas as pd

from server.simulation_objects.trafficlights.traffic_light import TrafficLight


class MLAlgo(TLManager):
    def __init__(self, junction, data_path, time_limit=np.inf, depth=2, time_interval=10):
        super().__init__(junction, time_limit)

        fit_data = pd.read_csv(data_path)
        self.model = DecisionTreeClassifier()
        self.model.fit(fit_data.drop("label"), fit_data["label"])
        self.depth = depth
        self.time_interval = time_interval

        self._time_count = 0
        self.running_algo: TLManager = NaiveAlgo(junction)

    @staticmethod
    def expected_traffic(tl: TrafficLight, depth):
        prev_junctions = [lane._comes_from for lane in tl.lanes]
        traff_per_junction = [sum(tl.all_cars for tl in junc.lights) for junc in prev_junctions]
        if depth > 0:
            expected_traff_per_junction = [sum(MLAlgo.expected_traffic(tl, depth - 1) for tl in junc.lights) for junc
                                           in prev_junctions]
            return sum(traff_per_junction) + sum(expected_traff_per_junction)
        return sum(traff_per_junction)

    def _predict(self):
        local_traffics = {f"local_traffic{i}": len(tl.all_cars) for i, tl in enumerate(self._lights)}
        expected_traffic = {f"expected_traffic{i}": MLAlgo._expected_traffic(tl, depth=self.depth - 1) for i, tl in
                            enumerate(self._lights)}
        nearby_junctions_algos = {f"nearby_algos{i}": [lane._comes_from._algo for lane in tl.lanes] for i, tl in
                                  enumerate(self._lights)}
        predict_input = {**{**local_traffics, **expected_traffic}, **nearby_junctions_algos}
        predict_input["time_interval"] = self.time_interval

        predict_input = pd.DataFrame(predict_input)

        self.running_algo: TLManager = index_to_algo.get(self.model.predict(predict_input), self.running_algo)

        return self.running_algo._manage_lights()

    def _manage_lights(self):
        if self._time_count % self.time_interval == 0:
            res = self._predict()
        else:
            res = self._current_light

        self._time_count += 1
        return res
