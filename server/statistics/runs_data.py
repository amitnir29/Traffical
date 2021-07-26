import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

import pandas as pd
from PIL.Image import Image
from pandas import DataFrame

FILE_NAME_FORMAT = "%d_%m_%Y__%H_%M_%S"
DIR_PATH = "server/statistics/results"


@dataclass
class ReportSimulationData:
    algo_name: str
    iteration_number: int
    total_waiting_time: int
    total_dec_time: int
    avg_car_waiting: float
    median_car_waiting: float
    var_car_waiting: float
    car_num: int
    total_waiting_image: Image
    cars_waiting_image: Image
    avg_car_dec: float
    median_car_dec: float
    var_car_dec: float
    total_dec_image: Image
    cars_dec_image: Image
    inner_path = "/simulation"

    def save_to_file(self) -> Optional[str]:
        data = {
            "Algorithm Name": self.algo_name,
            "Number of Iteration": self.iteration_number,
            "Total Waiting Time": self.total_waiting_time,
            "Total Deceleration Time": self.total_dec_time,
            "Average Waiting Time": self.avg_car_waiting,
            "Median Waiting Time": self.median_car_waiting,
            "Variance Waiting Time": self.var_car_waiting,
            "Number of Cars": self.car_num,
            "Average Deceleration Time": self.avg_car_dec,
            "Median Deceleration Time": self.median_car_dec,
            "Variance Deceleration Time": self.var_car_dec
        }
        df = pd.DataFrame(data, index=[0])
        create_required_dirs(self.inner_path)
        now = datetime.now()
        dt_string = now.strftime(FILE_NAME_FORMAT)
        total_path = DIR_PATH + self.inner_path + "/" + dt_string
        os.mkdir(total_path)
        df.to_csv(total_path + "/" + "data.csv", index=False)
        self.total_dec_image.save(total_path + "/" + "Total Deceleration.png")
        self.total_waiting_image.save(total_path + "/" + "Total Waiting.png")
        self.cars_dec_image.save(total_path + "/" + "Cars Deceleration.png")
        self.cars_waiting_image.save(total_path + "/" + "Cars Waiting.png")
        return total_path


@dataclass
class ReportComparisonData:
    iteration_number: int
    total_waiting_time: int
    total_dec_time: int
    avg_car_waiting: float
    median_car_waiting: float
    var_car_waiting: float
    car_num: int
    total_waiting_df: DataFrame
    cars_waiting_df: DataFrame
    avg_car_dec: float
    median_car_dec: float
    var_car_dec: float
    total_dec_df: DataFrame
    cars_dec_df: DataFrame


@dataclass
class ComparisonListData:
    algo_names: List[str]
    iteration_number: List[int]
    total_waiting_time: List[int]
    total_dec_time: List[int]
    avg_car_waiting: List[float]
    median_car_waiting: List[float]
    var_car_waiting: List[float]
    car_num: int
    total_waiting_image: Image
    avg_car_dec: List[float]
    median_car_dec: List[float]
    var_car_dec: List[float]
    total_dec_image: Image
    inner_path = "/comparison"

    def save_to_file(self) -> Optional[str]:
        data = {"Algorithm Names": self.algo_names, "Number of Iterations": self.iteration_number,
                "Total Waiting Time": self.total_waiting_time, "Total Deceleration Time": self.total_dec_time,
                "Average Car Waiting": self.avg_car_waiting, "Median Car Waiting": self.median_car_waiting,
                "Variance Car Waiting": self.var_car_waiting, "Number of Cars": [self.car_num] * len(self.algo_names),
                "Average Car Deceleration": self.avg_car_dec, "Median Car Deceleration": self.median_car_dec,
                "Variance Car Deceleration": self.var_car_dec}
        df = pd.DataFrame(data, index=list(range(len(self.algo_names))))
        create_required_dirs(self.inner_path)
        now = datetime.now()
        dt_string = now.strftime(FILE_NAME_FORMAT)
        total_path = DIR_PATH + self.inner_path + "/" + dt_string
        os.mkdir(total_path)
        df.to_csv(total_path + "/" + "data.csv", index=False)
        self.total_dec_image.save(total_path + "/" + "Total Deceleration.png")
        self.total_waiting_image.save(total_path + "/" + "Total Waiting.png")
        return total_path


def create_required_dirs(inner_path):
    try:
        dirs = os.listdir(DIR_PATH)
    except FileNotFoundError:
        # no "generated" dir. create it
        os.mkdir(DIR_PATH)
    try:
        dirs = os.listdir(DIR_PATH + inner_path)
    except FileNotFoundError:
        # no "generated" dir. create it
        os.mkdir(DIR_PATH + inner_path)
