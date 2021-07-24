import os
from collections import defaultdict
from copy import copy
from dataclasses import dataclass
from io import BytesIO

import pandas as pd
import matplotlib.pyplot as plt

# from xlwt import Workbook
from PIL import Image

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
        # self.waiting_time = defaultdict(int)
        # # saves the number of iterations for each car
        # self.iterations = defaultdict(int)
        # # saves a list for each car of it's speeds (in each iteration)
        # self.speeds = defaultdict(dict)
        # # total time spent in all of the cars
        # self.total_iterations = 0
        # # time spent in 0 velocity
        # self.waiting_time = defaultdict(int)
        # self.total_waiting_time = 0
        # # time spent in negative acc
        # self.neg_acc_time = defaultdict(int)
        # self.curr_iter = 0
        # self.positions = defaultdict(dict)

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
        # if self.curr_iter % MAGIC_ITER_NUMBER == 0:
        #     self.sum_waiting_data['Iterations'] += [self.curr_iter]
        #     self.sum_waiting_data['Total Waiting Time'] += [self.total_waiting_time]

        # self.curr_iter += 1
        # for car in cars:
        #     if car not in self.cars:
        #         self.cars.append(car)
        #     self.iterations[car] += 1
        #     self.speeds[car][self.curr_iter] = car.get_speed()
        #     self.positions[car][self.curr_iter] = (car.position.x, car.position.y)
        #     self.total_iterations += 1
        #     if car.get_speed() < 0.0001:
        #         self.waiting_time[car] += 1
        #         self.total_waiting_time += 1
        #     if car.get_acceleration() < 0:
        #         self.neg_acc_time[car] += 1

    def report_save(self):
        sum_waiting_df = pd.DataFrame(self.sum_waiting_data)
        sum_waiting_df.reset_index(drop=True, inplace=True)
        waiting_df = pd.DataFrame(self.waiting_data)
        waiting_df.reset_index(drop=True, inplace=True)
        plt.plot(sum_waiting_df['Iterations'], sum_waiting_df['Total Waiting Time'])
        plt.xlabel('Iterations')
        plt.ylabel('Total Waiting Time')
        plt.title('Total waiting time of the entire simulation\nin every 10 iterations')
        plt.savefig('total.png')
        plt.show()
        plt.scatter(waiting_df['Iteration'], waiting_df['Waiting Cars'])
        plt.xlabel('Iteration')
        plt.ylabel('Waiting Cars')
        plt.savefig('cars.png')
        plt.show()
        avg_car_waiting = waiting_df['Waiting Cars'].mean()
        median_car_waiting = waiting_df['Waiting Cars'].median()
        var_car_waiting = waiting_df['Waiting Cars'].var()

        return self.total_waiting_time, self.total_neg_acc_time \
            , avg_car_waiting, median_car_waiting, var_car_waiting

    """
    def convert_depth_map_bw(depth_map, new_size=None):
      # create a black-white theme version of the depth map, and return it.
      fig = plt.figure()
      plt.axis('off')
    
      #display the image onto a grayscale plot
      plt.set_cmap("gray")
      plt.imshow(depth_map)
    
      #save to the plot to a temp bytes IO and then read from it as an Image
      temp_image_mem = BytesIO()
      fig.savefig(temp_image_mem, dpi=fig.dpi, bbox_inches='tight', pad_inches=0)
      image = Image.open(temp_image_mem)
      img = image_to_numpy(image, new_size)
    
      return img
    """

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
        # return self.total_waiting_time, self.total_neg_acc_time, avg_car_waiting, median_car_waiting, var_car_waiting, self.car_num, total_image, cars_image
        # waiting_df.to_csv('try.csv')

        # if os.path.exists(self.file_name):
        #     os.remove(self.file_name)
        # f = open(self.file_name, "x")
        # f.close()
        # wb = Workbook()
        # cars_sheet = wb.add_sheet('Cars Sheet')
        # speeds_sheet = wb.add_sheet('Speeds Sheet')
        # positions_sheet = wb.add_sheet('Positions Sheet')
        # general_sheet = wb.add_sheet('General Sheet')
        #
        # general_sheet.write(0, 0, 'Max Iteration')
        # general_sheet.write(0, 1, self.curr_iter)
        # general_sheet.write(1, 0, 'Total Iterations')
        # general_sheet.write(1, 1, self.total_iterations)
        # general_sheet.write(2, 0, 'Total Waiting Time')
        # general_sheet.write(2, 1, self.total_waiting_time)
        #
        # cars_sheet.write(0, 1, 'Iterations')
        # cars_sheet.write(0, 2, 'Waiting Time')
        # cars_sheet.write(0, 3, 'Negative Acc Time')
        #
        # for i in range(self.curr_iter):
        #     speeds_sheet.write(0, i+1, i+1)
        #     positions_sheet.write(0, i+1, i+1)
        #
        # for i, car in enumerate(self.cars):
        #     cars_sheet.write(i+1, 0, str(car))
        #     speeds_sheet.write(i+1, 0, str(car))
        #     positions_sheet.write(i+1, 0, str(car))
        #     cars_sheet.write(i+1, 1, self.iterations[car])
        #     cars_sheet.write(i+1, 2, self.waiting_time[car])
        #     cars_sheet.write(i+1, 3, self.neg_acc_time[car])
        #     speed_dict = self.speeds[car]
        #     position_dict = self.positions[car]
        #     for iter, speed in speed_dict.items():
        #         speeds_sheet.write(i+1, iter, speed)
        #     for iter, pos in position_dict.items():
        #         positions_sheet.write(i+1, iter, str(pos))
        #
        #
        # wb.save(self.file_name)
        # return [car.iteration for car in self.cars], sum(car.iteration for car in self.cars)
