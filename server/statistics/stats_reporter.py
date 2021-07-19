import os
from collections import defaultdict
from copy import copy

from xlwt import Workbook


class StatsReporter:
    def __init__(self, cars, junctions, file_name='server/statistics/stats/try.xls'):
        self.file_name = file_name
        self.cars = copy(cars)
        # saves the number of iterations for each car
        self.iterations = defaultdict(int)
        # saves a list for each car of it's speeds (in each iteration)
        self.speeds = defaultdict(dict)
        # total time spent in all of the cars
        self.total_iterations = 0
        # time spent in 0 velocity
        self.waiting_time = defaultdict(int)
        self.total_waiting_time = 0
        # time spent in negative acc
        self.neg_acc_time = defaultdict(int)
        self.curr_iter = 0
        self.positions = defaultdict(dict)

    def next_iter(self, cars):
        self.curr_iter += 1
        for car in cars:
            if car not in self.cars:
                self.cars.append(car)
            self.iterations[car] += 1
            self.speeds[car][self.curr_iter] = car.get_speed()
            self.positions[car][self.curr_iter] = (car.position.x, car.position.y)
            self.total_iterations += 1
            if car.get_speed() < 0.0001:
                self.waiting_time[car] += 1
                self.total_waiting_time += 1
            if car.get_acceleration() < 0:
                self.neg_acc_time[car] += 1

    def report(self):
        if os.path.exists(self.file_name):
            os.remove(self.file_name)
        f = open(self.file_name, "x")
        f.close()
        wb = Workbook()
        cars_sheet = wb.add_sheet('Cars Sheet')
        speeds_sheet = wb.add_sheet('Speeds Sheet')
        positions_sheet = wb.add_sheet('Positions Sheet')
        general_sheet = wb.add_sheet('General Sheet')

        general_sheet.write(0, 0, 'Max Iteration')
        general_sheet.write(0, 1, self.curr_iter)
        general_sheet.write(1, 0, 'Total Iterations')
        general_sheet.write(1, 1, self.total_iterations)
        general_sheet.write(2, 0, 'Total Waiting Time')
        general_sheet.write(2, 1, self.total_waiting_time)

        cars_sheet.write(0, 1, 'Iterations')
        cars_sheet.write(0, 2, 'Waiting Time')
        cars_sheet.write(0, 3, 'Negative Acc Time')

        for i in range(self.curr_iter):
            speeds_sheet.write(0, i+1, i+1)
            positions_sheet.write(0, i+1, i+1)

        for i, car in enumerate(self.cars):
            cars_sheet.write(i+1, 0, str(car))
            speeds_sheet.write(i+1, 0, str(car))
            positions_sheet.write(i+1, 0, str(car))
            cars_sheet.write(i+1, 1, self.iterations[car])
            cars_sheet.write(i+1, 2, self.waiting_time[car])
            cars_sheet.write(i+1, 3, self.neg_acc_time[car])
            speed_dict = self.speeds[car]
            position_dict = self.positions[car]
            for iter, speed in speed_dict.items():
                speeds_sheet.write(i+1, iter, speed)
            for iter, pos in position_dict.items():
                positions_sheet.write(i+1, iter, str(pos))


        wb.save(self.file_name)
        # return [car.iteration for car in self.cars], sum(car.iteration for car in self.cars)
