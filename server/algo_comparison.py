from dataclasses import dataclass
from io import BytesIO
from typing import List

from PIL.Image import Image

from server.statistics.stats_reporter import StatsReporter, ComparisonData
import pandas as pd
import matplotlib.pyplot as plt

# from xlwt import Workbook
from PIL import Image
from pandas import DataFrame

@dataclass
class ComparisonListData:
    algo_names: List[str]
    total_waiting_time: List[int]
    total_neg_acc_time: List[int]
    avg_car_waiting: List[float]
    median_car_waiting: List[float]
    var_car_waiting: List[float]
    car_num: int
    total_waiting_df: Image
    # cars_waiting_df: Image
    avg_car_neg_acc: List[float]
    median_car_neg_acc: List[float]
    var_car_neg_acc: List[float]
    total_neg_acc_df: Image
    # cars_neg_acc_df: Image


def collect_reports(reporters: List[str, StatsReporter]):
    datas: List[ComparisonData] = []
    algo_names: List[str] = []
    total_waiting_time: List[int] = []
    total_neg_acc_time: List[int] = []
    avg_car_waiting: List[float] = []
    median_car_waiting: List[float] = []
    var_car_waiting: List[float] = []
    car_num: int
    total_waiting_df: Image
    # cars_waiting_df: Image
    avg_car_neg_acc: List[float] = []
    median_car_neg_acc: List[float] = []
    var_car_neg_acc: List[float] = []
    total_neg_acc_df: Image
    # cars_neg_acc_df: Image

    for name, reporter in reporters:
        data: ComparisonData = reporter.report_compare()
        datas += [data]
        car_num = data.car_num
        algo_names += [name]
        total_waiting_time += [data.total_waiting_time]
        total_neg_acc_time += [data.total_neg_acc_time]
        avg_car_waiting += [data.avg_car_waiting]
        median_car_waiting += [data.median_car_waiting]
        var_car_waiting += [data.var_car_waiting]
        avg_car_neg_acc += [data.avg_car_neg_acc]
        median_car_neg_acc += [data.median_car_neg_acc]
        var_car_neg_acc += [data.var_car_neg_acc]

    for i, data in enumerate(datas):
        plt.plot(data.total_waiting_df['Iterations'], data.total_waiting_df['Total Waiting Time'], label=algo_names[i])
    plt.xlabel('Iterations')
    plt.ylabel('Total Waiting Time')
    plt.title('Total waiting time of the entire simulation\nin each iteration')
    temp_image_mem = BytesIO()
    plt.savefig(temp_image_mem)
    total_waiting_image = Image.open(temp_image_mem)

    plt.clf()

    for i, data in enumerate(datas):
        plt.plot(data.total_neg_acc_df['Iterations'], data.total_neg_acc_df['Total Neg Acc Time'], label=algo_names[i])
    plt.xlabel('Iterations')
    plt.ylabel('Total Neg Acc Time')
    plt.title('Total negative acceleration time of the\n entire simulation in each iteration')
    temp_image_mem2 = BytesIO()
    plt.savefig(temp_image_mem2)
    total_neg_acc_image = Image.open(temp_image_mem2)

    return ComparisonListData(
        algo_names=algo_names, total_waiting_time=total_waiting_time,
        total_neg_acc_time=total_neg_acc_time, avg_car_waiting=avg_car_waiting,
        median_car_waiting=median_car_waiting, var_car_waiting=var_car_waiting,
        car_num=car_num, total_waiting_df=total_waiting_df, avg_car_neg_acc=avg_car_neg_acc,
        median_car_neg_acc=median_car_neg_acc, var_car_neg_acc=var_car_neg_acc,
        total_neg_acc_df=total_neg_acc_df
    )





