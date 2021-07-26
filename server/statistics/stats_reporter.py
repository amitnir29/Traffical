from copy import copy
from io import BytesIO

import matplotlib.pyplot as plt
import pandas as pd
# from xlwt import Workbook
from PIL import Image

from server.statistics.runs_data import ReportComparisonData, ReportSimulationData

MAGIC_ITER_NUMBER = 10


class StatsReporter:
    def __init__(self, cars, algo_name, file_name='server/statistics/stats/try.xls'):
        self.algo_name = algo_name
        self.file_name = file_name
        self.cars = copy(cars)
        self.car_num = len(cars)
        self.sum_waiting_data = {'Iterations': [], 'Total Waiting Time': []}
        self.waiting_data = {'Iteration': [], 'Waiting Cars': []}
        self.sum_dec_data = {'Iterations': [], 'Total Dec Time': []}
        self.dec_data = {'Iteration': [], 'Dec Cars': []}
        self.curr_iter = 0
        self.total_waiting_time = 0
        self.total_dec_time = 0

    def next_iter(self, cars):
        self.curr_iter += 1
        waiting_curr = 0
        dec_curr = 0
        for car in cars:
            if car.get_speed() < 0.0001:
                self.total_waiting_time += 1
                waiting_curr += 1
            if car.get_acceleration() < 0:
                self.total_dec_time += 1
                dec_curr += 1
        self.waiting_data['Iteration'] += [self.curr_iter]
        self.waiting_data['Waiting Cars'] += [waiting_curr]
        self.sum_waiting_data['Iterations'] += [self.curr_iter]
        self.sum_waiting_data['Total Waiting Time'] += [self.total_waiting_time]
        self.dec_data['Iteration'] += [self.curr_iter]
        self.dec_data['Dec Cars'] += [dec_curr]
        self.sum_dec_data['Iterations'] += [self.curr_iter]
        self.sum_dec_data['Total Dec Time'] += [self.total_dec_time]

    def report_compare(self):
        # Waiting data
        sum_waiting_df = pd.DataFrame(self.sum_waiting_data)
        sum_waiting_df.reset_index(drop=True, inplace=True)
        waiting_df = pd.DataFrame(self.waiting_data)
        waiting_df.reset_index(drop=True, inplace=True)
        avg_car_waiting = waiting_df['Waiting Cars'].mean()
        median_car_waiting = waiting_df['Waiting Cars'].median()
        var_car_waiting = waiting_df['Waiting Cars'].var()

        # Deceleration data
        sum_dec_df = pd.DataFrame(self.sum_dec_data)
        sum_dec_df.reset_index(drop=True, inplace=True)
        dec_df = pd.DataFrame(self.dec_data)
        dec_df.reset_index(drop=True, inplace=True)
        avg_car_dec = dec_df['Dec Cars'].mean()
        median_car_dec = dec_df['Dec Cars'].median()
        var_car_dec = dec_df['Dec Cars'].var()

        return ReportComparisonData(total_waiting_time=self.total_waiting_time, total_dec_time=self.total_dec_time,
                                    avg_car_waiting=avg_car_waiting, median_car_waiting=median_car_waiting,
                                    var_car_waiting=var_car_waiting, car_num=self.car_num,
                                    total_waiting_df=sum_waiting_df, cars_waiting_df=waiting_df,
                                    avg_car_dec=avg_car_dec, median_car_dec=median_car_dec,
                                    var_car_dec=var_car_dec, total_dec_df=sum_dec_df,
                                    cars_dec_df=dec_df, iteration_number=self.curr_iter)

    def report(self):
        # Waiting data
        sum_waiting_df = pd.DataFrame(self.sum_waiting_data)
        sum_waiting_df.reset_index(drop=True, inplace=True)
        waiting_df = pd.DataFrame(self.waiting_data)
        waiting_df.reset_index(drop=True, inplace=True)

        plt.clf()
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

        # Deceleration data
        plt.clf()
        sum_dec_df = pd.DataFrame(self.sum_dec_data)
        sum_dec_df.reset_index(drop=True, inplace=True)
        dec_df = pd.DataFrame(self.dec_data)
        dec_df.reset_index(drop=True, inplace=True)
        plt.plot(sum_dec_df['Iterations'], sum_dec_df['Total Dec Time'])
        plt.xlabel('Iterations')
        plt.ylabel('Total Dec Time')
        plt.title('Total deceleration time of the\n entire simulation in each iteration')
        temp_image_mem3 = BytesIO()
        plt.savefig(temp_image_mem3)
        total_dec_image = Image.open(temp_image_mem3)

        plt.clf()
        plt.scatter(dec_df['Iteration'], dec_df['Dec Cars'])
        plt.xlabel('Iteration')
        plt.ylabel('Dec Cars')
        plt.title('Total deceleration cars in the\nentire simulation in each iteration')
        temp_image_mem4 = BytesIO()
        plt.savefig(temp_image_mem4)
        cars_dec_image = Image.open(temp_image_mem4)
        avg_car_dec = dec_df['Dec Cars'].mean()
        median_car_dec = dec_df['Dec Cars'].median()
        var_car_dec = dec_df['Dec Cars'].var()

        return ReportSimulationData(algo_name=self.algo_name, total_waiting_time=self.total_waiting_time,
                                    total_dec_time=self.total_dec_time,
                                    avg_car_waiting=avg_car_waiting, median_car_waiting=median_car_waiting,
                                    var_car_waiting=var_car_waiting, car_num=self.car_num,
                                    total_waiting_image=total_waiting_image, cars_waiting_image=cars_waiting_image,
                                    avg_car_dec=avg_car_dec, median_car_dec=median_car_dec,
                                    var_car_dec=var_car_dec, total_dec_image=total_dec_image,
                                    cars_dec_image=cars_dec_image, iteration_number=self.curr_iter)
