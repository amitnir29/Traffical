from itertools import combinations_with_replacement
import csv
import os

from algorithms.algo_to_index import algo_to_index, algos_list_to_num, index_to_algo
from algorithms.ml_algo import MLAlgo
from algorithms.tl_manager import TLManager
from server.cars_generator import generate_cars
from server.map_creation import create_map
from server.server_runner import next_iter
from server.simulation_objects.junctions.junction import Junction


class ReporterJunction:
    """
    A decorator class for junction to report state in each iteration.
    """

    def __init__(self, junction: Junction, report_path, time_interval: float, depth=2):
        self.junction = junction
        self.algo: TLManager = self.junction._algo

        self.report_path = report_path

        self.time_count = 0
        self.time_interval = time_interval

        self.algo_index = algo_to_index[self.algo.__class__]

        self.depth = depth

    def _get_simulation_state(self):
        local_traffics = [str(len(tl.all_cars)) for tl in self.lights]
        local_traffics += ["0"] * (4 - len(local_traffics))
        expected_traffics = [str(MLAlgo.expected_traffic(tl, self.depth - 1)) for tl in self.lights]
        expected_traffics += ["0"] * (4 - len(expected_traffics))

        nearby_algos = [str(algos_list_to_num(
            [lane._comes_from_junction._algo if hasattr(lane._comes_from_junction, '_algo') else None for lane in
             tl.lanes])) for tl in self.lights]
        nearby_algos += ["0"] * (4 - len(nearby_algos))
        return [str(self.algo_index), str(self.time_interval), *local_traffics, *expected_traffics, *nearby_algos]

    @staticmethod
    def _log(report_path, data):
        with open(report_path, 'a', newline='') as report_file:
            writer = csv.writer(report_file)
            writer.writerow(data)

    def manage_lights(self):
        if self.time_count % self.time_interval == 0:
            data = self._get_simulation_state()
            self._log(self.report_path, data)

        self.algo.manage_lights()

        self.time_count += 1

    def __getattr__(self, item):
        """
        Easily implement decorator design pattern.
        """
        return getattr(self.junction, item)


def run(i, roads, traffic_lights, algos_indices, junctions_with_lights, reporting_junctions):
    print("start", i)
    cars_num = 30
    time_interval = 40

    algos = [index_to_algo[index] for index in algos_indices]
    light_algos = [algo(junction) for algo, junction in zip(algos, junctions_with_lights)]

    # Some output paths
    # All junctions' reports
    report_path = f"data/test_{cars_num}_{time_interval}/{i}.csv"

    # Amount of iterations.
    txt_path = f"data/test_{cars_num}_{time_interval}/{i}.txt"

    if not os.path.exists(os.path.dirname(report_path)):
        os.makedirs(os.path.dirname(report_path))

    with open(report_path, 'w', newline='') as report_file:
        writer = csv.writer(report_file)

        # Create header
        writer.writerow(["used_algo", "time_interval", *[f"local_traffic{i}" for i in range(4)],
                         *[f"expected_traffic{i}" for i in range(4)], *[f"nearby_algos{i}" for i in range(4)]])

    # Wrap relevant junctions with reporter decorator.
    for idx in reporting_junctions:
        light_algos[idx] = ReporterJunction(junctions_with_lights[idx], report_path, 10)

    cars = generate_cars(roads, cars_num, p=0.9, min_len=6, with_prints=False)

    j = 0
    while len(cars) > 0:
        j += 1
        traffic_lights, cars = next_iter(light_algos, traffic_lights, cars)

    with open(txt_path, "w") as txt_file:
        txt_file.write(str(j))

    print("end", i)


def main():
    # Graphics measures
    win_width, win_height = (800, 800)

    # get the simulation map
    roads, traffic_lights, all_junctions = create_map(win_width, win_height, "db/databases/handmade/tel_aviv")

    junctions_with_lights = [junction for junction in all_junctions if len(junction.lights) > 0]
    reporting_junctions = [2, 3, 5]

    for i, comb in enumerate(
            combinations_with_replacement(sorted(index_to_algo.keys())[1:], len(junctions_with_lights))):
        run(i, roads, traffic_lights, comb, junctions_with_lights, reporting_junctions)


if __name__ == '__main__':
    main()
