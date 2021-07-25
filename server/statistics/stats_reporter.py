import os
from collections import defaultdict
from copy import copy
from dataclasses import dataclass
from io import BytesIO

import pandas as pd
import matplotlib.pyplot as plt

# from xlwt import Workbook
from PIL import Image
from pandas import DataFrame

MAGIC_ITER_NUMBER = 10


@dataclass
class ReportScreenData:
    total_waiting_time: int
    total_neg_acc_time: int
    avg_car_waiting: float
    median_car_waiting: float
    var_car_waiting: float
    car_num: int
    total_waiting_image: Image
    cars_waiting_image: Image
    avg_car_neg_acc: float
    median_car_neg_acc: float
    var_car_neg_acc: float
    total_neg_acc_image: Image
    cars_neg_acc_image: Image


@dataclass
class ComparisonData:
    total_waiting_time: int
    total_neg_acc_time: int
    avg_car_waiting: float
    median_car_waiting: float
    var_car_waiting: float
    car_num: int
    total_waiting_df: DataFrame
    cars_waiting_df: DataFrame
    avg_car_neg_acc: float
    median_car_neg_acc: float
    var_car_neg_acc: float
    total_neg_acc_df: DataFrame
    cars_neg_acc_df: DataFrame


class StatsReporter:
    def __init__(self, cars, file_name='server/statistics/stats/try.xls'):
        self.file_name = file_name
        self.cars = copy(cars)
        self.car_num = len(cars)
        self.sum_waiting_data = {'Iterations': [], 'Total Waiting Time': []}
        self.waiting_data = {'Iteration': [], 'Waiting Cars': []}
        self.sum_neg_acc_data = {'Iterations': [], 'Total Neg Acc Time': []}
        self.neg_acc_data = {'Iteration': [], 'Neg Acc Cars': []}
        self.curr_iter = 0
        self.total_waiting_time = 0
        self.total_neg_acc_time = 0

    def next_iter(self, cars):
        self.curr_iter += 1
        waiting_curr = 0
        neg_acc_curr = 0
        for car in cars:
            if car.get_speed() < 0.0001:
                self.total_waiting_time += 1
                waiting_curr += 1
            if car.get_acceleration() < 0:
                self.total_neg_acc_time += 1
                neg_acc_curr += 1
        self.waiting_data['Iteration'] += [self.curr_iter]
        self.waiting_data['Waiting Cars'] += [waiting_curr]
        self.sum_waiting_data['Iterations'] += [self.curr_iter]
        self.sum_waiting_data['Total Waiting Time'] += [self.total_waiting_time]
        self.neg_acc_data['Iteration'] += [self.curr_iter]
        self.neg_acc_data['Neg Acc Cars'] += [neg_acc_curr]
        self.sum_neg_acc_data['Iterations'] += [self.curr_iter]
        self.sum_neg_acc_data['Total Neg Acc Time'] += [self.total_neg_acc_time]

    def report_compare(self):
        # Waiting data
        sum_waiting_df = pd.DataFrame(self.sum_waiting_data)
        sum_waiting_df.reset_index(drop=True, inplace=True)
        waiting_df = pd.DataFrame(self.waiting_data)
        waiting_df.reset_index(drop=True, inplace=True)
        avg_car_waiting = waiting_df['Waiting Cars'].mean()
        median_car_waiting = waiting_df['Waiting Cars'].median()
        var_car_waiting = waiting_df['Waiting Cars'].var()

        # Negative Acceleration data
        sum_neg_acc_df = pd.DataFrame(self.sum_neg_acc_data)
        sum_neg_acc_df.reset_index(drop=True, inplace=True)
        neg_acc_df = pd.DataFrame(self.neg_acc_data)
        neg_acc_df.reset_index(drop=True, inplace=True)
        avg_car_neg_acc = neg_acc_df['Neg Acc Cars'].mean()
        median_car_neg_acc = neg_acc_df['Neg Acc Cars'].median()
        var_car_neg_acc = neg_acc_df['Neg Acc Cars'].var()

        return ComparisonData(total_waiting_time=self.total_waiting_time, total_neg_acc_time=self.total_neg_acc_time,
                              avg_car_waiting=avg_car_waiting, median_car_waiting=median_car_waiting,
                              var_car_waiting=var_car_waiting, car_num=self.car_num,
                              total_waiting_df=sum_waiting_df, cars_waiting_df=waiting_df,
                              avg_car_neg_acc=avg_car_neg_acc, median_car_neg_acc=median_car_neg_acc,
                              var_car_neg_acc=var_car_neg_acc, total_neg_acc_df=sum_neg_acc_df,
                              cars_neg_acc_df=neg_acc_df)

    def report(self):
        # Waiting data
        sum_waiting_df = pd.DataFrame(self.sum_waiting_data)
        sum_waiting_df.reset_index(drop=True, inplace=True)
        waiting_df = pd.DataFrame(self.waiting_data)
        waiting_df.reset_index(drop=True, inplace=True)
        plt.plot(sum_waiting_df['Iterations'], sum_waiting_df['Total Waiting Time'])
        plt.xlabel('Iterations')
        plt.ylabel('Total Waiting Time')
        plt.title('Total waiting time of the entire simulation\nin each iteration')
        temp_image_mem = BytesIO()
        plt.savefig(temp_image_mem)
        total_waiting_image = Image.open(temp_image_mem)

        plt.clf()
        plt.scatter(waiting_df['Iteration'], waiting_df['Waiting Cars'])
        plt.xlabel('Iteration')
        plt.ylabel('Waiting Cars')
        plt.title('Total Waiting cars in the entire simulation\nin each iteration')
        temp_image_mem2 = BytesIO()
        plt.savefig(temp_image_mem2)
        cars_waiting_image = Image.open(temp_image_mem2)
        avg_car_waiting = waiting_df['Waiting Cars'].mean()
        median_car_waiting = waiting_df['Waiting Cars'].median()
        var_car_waiting = waiting_df['Waiting Cars'].var()

        # Negative Acceleration data
        plt.clf()
        sum_neg_acc_df = pd.DataFrame(self.sum_neg_acc_data)
        sum_neg_acc_df.reset_index(drop=True, inplace=True)
        neg_acc_df = pd.DataFrame(self.neg_acc_data)
        neg_acc_df.reset_index(drop=True, inplace=True)
        plt.plot(sum_neg_acc_df['Iterations'], sum_neg_acc_df['Total Neg Acc Time'])
        plt.xlabel('Iterations')
        plt.ylabel('Total Neg Acc Time')
        plt.title('Total negative acceleration time of the\n entire simulation in each iteration')
        temp_image_mem3 = BytesIO()
        plt.savefig(temp_image_mem3)
        total_neg_acc_image = Image.open(temp_image_mem3)

        plt.clf()
        plt.scatter(neg_acc_df['Iteration'], neg_acc_df['Neg Acc Cars'])
        plt.xlabel('Iteration')
        plt.ylabel('Neg Acc Cars')
        plt.title('Total negative acceleration cars in the\nentire simulation in each iteration')
        temp_image_mem4 = BytesIO()
        plt.savefig(temp_image_mem4)
        cars_neg_acc_image = Image.open(temp_image_mem4)
        avg_car_neg_acc = neg_acc_df['Neg Acc Cars'].mean()
        median_car_neg_acc = neg_acc_df['Neg Acc Cars'].median()
        var_car_neg_acc = neg_acc_df['Neg Acc Cars'].var()

        return ReportScreenData(total_waiting_time=self.total_waiting_time, total_neg_acc_time=self.total_neg_acc_time,
                                avg_car_waiting=avg_car_waiting, median_car_waiting=median_car_waiting,
                                var_car_waiting=var_car_waiting, car_num=self.car_num,
                                total_waiting_image=total_waiting_image, cars_waiting_image=cars_waiting_image,
                                avg_car_neg_acc=avg_car_neg_acc, median_car_neg_acc=median_car_neg_acc,
                                var_car_neg_acc=var_car_neg_acc, total_neg_acc_image=total_neg_acc_image,
                                cars_neg_acc_image=cars_neg_acc_image)
