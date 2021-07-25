from dataclasses import dataclass
from io import BytesIO
from typing import List

import pygame
from PIL import Image
from matplotlib import pyplot as plt

from graphics.menu.screens.screen_activity import Screen, TITLES_SCREEN_PORTION
from graphics.menu.screens.stats_screens.stats_screen_parent import StatsScreenParent
from server.geometry.point import Point
from server.statistics.stats_reporter import ReportScreenData, ComparisonData


@dataclass
class ComparisonListData:
    algo_names: List[str]
    total_waiting_time: List[int]
    total_neg_acc_time: List[int]
    avg_car_waiting: List[float]
    median_car_waiting: List[float]
    var_car_waiting: List[float]
    car_num: int
    total_waiting_image: Image
    avg_car_neg_acc: List[float]
    median_car_neg_acc: List[float]
    var_car_neg_acc: List[float]
    total_neg_acc_image: Image


class ComparisonStatsScreen(StatsScreenParent):

    def __init__(self, screen: pygame.Surface, background, reporters):
        super().__init__(screen, background)
        self.reporters = reporters

    def _draw_all_data(self, total_delta_y, reporters_data: ComparisonListData):
        self.screen.fill(self.background)
        middle_x = self.screen.get_width() // 2

        # graphs
        self.draw_image(self.pil_image_to_surface(reporters_data.total_waiting_image),
                        Point(210, self.screen.get_height() // TITLES_SCREEN_PORTION + 120 - total_delta_y))
        self.draw_image(self.pil_image_to_surface(reporters_data.total_neg_acc_image),
                        Point(590, self.screen.get_height() // TITLES_SCREEN_PORTION + 120 - total_delta_y))
        # texts
        texts = list()
        for i in range(len(reporters_data.algo_names)):
            texts.append((f"algo name: {reporters_data.algo_names[i]}", [
                f"total waiting time: {reporters_data.total_waiting_time[i]}",
                f"total negative acceleration time: {reporters_data.total_neg_acc_time[i]}",

                f"average car waiting time: {round(reporters_data.avg_car_waiting[i], 3)}",
                f"median car waiting time: {reporters_data.median_car_waiting[i]}",
                f"variance car waiting time: {round(reporters_data.var_car_waiting[i], 3)}",

                f"average car negative acceleration time: {round(reporters_data.avg_car_neg_acc[i], 3)}",
                f"median car negative acceleration time: {reporters_data.median_car_neg_acc[i]}",
                f"variance car negative acceleration time: {round(reporters_data.var_car_neg_acc[i], 3)}"
            ]))

        self.write_text(f"number of cars: {reporters_data.car_num}", middle_x, 500 - total_delta_y, 40)
        for i, pair in enumerate(texts):
            head, data_lines = pair
            start_i = 600 + i * 500 - total_delta_y
            self.write_text(head, middle_x, start_i, 40)
            for j, data_line in enumerate(data_lines):
                self.write_text(data_line, middle_x, start_i + 50 + j * 40, 30)

        # write header and footer
        pygame.draw.rect(self.screen, self.background, [0, 0, self.screen.get_width(),
                                                        self.screen.get_height() // TITLES_SCREEN_PORTION])
        self.write_text("Simulation Statistics", middle_x, self.screen.get_height() // 8, 60)
        pygame.draw.rect(self.screen, self.background, [0, self.screen.get_height() - 100,
                                                        self.screen.get_width(), 100])
        self.write_text("click to go back", middle_x, self.screen.get_height() - 50, 40)
        # Draws the surface object to the screen.
        pygame.display.update()

    def _reporters_data(self):
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

        for name, reporter in self.reporters:
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
            plt.plot(data.total_waiting_df['Iterations'], data.total_waiting_df['Total Waiting Time'],
                     label=algo_names[i])
        plt.xlabel('Iterations')
        plt.ylabel('Total Waiting Time')
        plt.title('Total waiting time of the entire simulation\nin each iteration')
        plt.legend()
        temp_image_mem = BytesIO()
        plt.savefig(temp_image_mem)
        total_waiting_image = Image.open(temp_image_mem)

        plt.clf()

        for i, data in enumerate(datas):
            plt.plot(data.total_neg_acc_df['Iterations'], data.total_neg_acc_df['Total Neg Acc Time'],
                     label=algo_names[i])
        plt.xlabel('Iterations')
        plt.ylabel('Total Neg Acc Time')
        plt.title('Total negative acceleration time of the\n entire simulation in each iteration')
        plt.legend()
        temp_image_mem2 = BytesIO()
        plt.savefig(temp_image_mem2)
        total_neg_acc_image = Image.open(temp_image_mem2)

        return ComparisonListData(
            algo_names=algo_names, total_waiting_time=total_waiting_time,
            total_neg_acc_time=total_neg_acc_time, avg_car_waiting=avg_car_waiting,
            median_car_waiting=median_car_waiting, var_car_waiting=var_car_waiting,
            car_num=car_num, total_waiting_image=total_waiting_image, avg_car_neg_acc=avg_car_neg_acc,
            median_car_neg_acc=median_car_neg_acc, var_car_neg_acc=var_car_neg_acc,
            total_neg_acc_image=total_neg_acc_image
        )

    @property
    def max_scroll(self):
        return 800
