import os
from dataclasses import dataclass
from datetime import datetime
from typing import List

import pandas as pd
from PIL.Image import Image
from pandas import DataFrame

FILE_NAME_FORMAT = "%d_%m_%Y__%H_%M_%S"


@dataclass
class ReportSimulationData:
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
    was_saved = False

    def save_to_file(self):
        if self.was_saved:
            return
        self.was_saved = True
        data = {
            "Algorithm Name": "todo",
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
        dir_path = "server/statistics/results"
        # check if dir exists
        try:
            dirs = os.listdir(dir_path)
        except FileNotFoundError:
            # no "generated" dir. create it
            os.mkdir(dir_path)
        now = datetime.now()
        dt_string = now.strftime(FILE_NAME_FORMAT)
        os.mkdir(dir_path + "/" + dt_string)
        new_dir_path = dir_path + "/" + dt_string
        df.to_csv(new_dir_path + "/" + "data.csv", index=False)
        self.total_dec_image.save(new_dir_path + "/" + "Total Deceleration.png")
        self.total_waiting_image.save(new_dir_path + "/" + "Total Waiting.png")
        self.cars_dec_image.save(new_dir_path + "/" + "Cars Deceleration.png")
        self.cars_waiting_image.save(new_dir_path + "/" + "Cars Waiting.png")


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
    was_saved = False

    def save_to_file(self):
        if self.was_saved:
            return
        self.was_saved = True
        data = {"Algorithm Names": self.algo_names, "Number of Iterations": self.iteration_number,
                "Total Waiting Time": self.total_waiting_time, "Total Deceleration Time": self.total_dec_time,
                "Average Car Waiting": self.avg_car_waiting, "Median Car Waiting": self.median_car_waiting,
                "Variance Car Waiting": self.var_car_waiting, "Number of Cars": [self.car_num] * len(self.algo_names),
                "Average Car Deceleration": self.avg_car_dec, "Median Car Deceleration": self.median_car_dec,
                "Variance Car Deceleration": self.var_car_dec}
        df = pd.DataFrame(data, index=[0, 1, 2])
        # df.set_, (ndex("Algorithm Names")
        dir_path = "server/statistics/results"
        # check if dir exists
        try:
            dirs = os.listdir(dir_path)
        except FileNotFoundError:
            # no "generated" dir. create it
            os.mkdir(dir_path)
        now = datetime.now()
        dt_string = now.strftime(FILE_NAME_FORMAT)
        os.mkdir(dir_path + "/" + dt_string)
        new_dir_path = dir_path + "/" + dt_string
        df.to_csv(new_dir_path + "/" + "data.csv", index=False)
        self.total_dec_image.save(new_dir_path + "/" + "Total Deceleration.png")
        self.total_waiting_image.save(new_dir_path + "/" + "Total Waiting.png")
