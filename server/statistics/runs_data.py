from dataclasses import dataclass

from PIL.Image import Image
from pandas import DataFrame


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
