import os
from dataclasses import dataclass
from io import BytesIO
from typing import List
from datetime import datetime

import pandas as pd
import pygame
from PIL import Image
from matplotlib import pyplot as plt

from gui.screens.screen_activity import TITLES_SCREEN_PORTION
from gui.screens.stats_screens.stats_screen_parent import StatsScreenParent
from server.geometry.point import Point
from server.statistics.runs_data import ReportComparisonData, ComparisonListData


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
        self.draw_image(self.pil_image_to_surface(reporters_data.total_dec_image),
                        Point(590, self.screen.get_height() // TITLES_SCREEN_PORTION + 120 - total_delta_y))
        # texts
        texts = list()
        for i in range(len(reporters_data.algo_names)):
            texts.append((f"algo name: {reporters_data.algo_names[i]}", [
                f"number of iterations: {reporters_data.iteration_number[i]}",
                f"total waiting time: {reporters_data.total_waiting_time[i]}",
                f"total deceleration time: {reporters_data.total_dec_time[i]}",

                f"average car waiting time: {round(reporters_data.avg_car_waiting[i], 3)}",
                f"median car waiting time: {reporters_data.median_car_waiting[i]}",
                f"variance car waiting time: {round(reporters_data.var_car_waiting[i], 3)}",

                f"average car deceleration time: {round(reporters_data.avg_car_dec[i], 3)}",
                f"median car deceleration time: {reporters_data.median_car_dec[i]}",
                f"variance car deceleration time: {round(reporters_data.var_car_dec[i], 3)}"
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
        self.save_button.draw(self)
        if self.was_saved_text is not None:
            self.write_text(f"saved to: {self.was_saved_text}", self.screen.get_width() // 2, 20, 20)
        # Draws the surface object to the screen.
        pygame.display.update()

    def _reporters_data(self):
        iteration_number: List[int] = []
        datas: List[ReportComparisonData] = []
        algo_names: List[str] = []
        total_waiting_time: List[int] = []
        total_dec_time: List[int] = []
        avg_car_waiting: List[float] = []
        median_car_waiting: List[float] = []
        var_car_waiting: List[float] = []
        car_num: int
        total_waiting_df: Image
        # cars_waiting_df: Image
        avg_car_dec: List[float] = []
        median_car_dec: List[float] = []
        var_car_dec: List[float] = []
        total_dec_df: Image
        # cars_dec_df: Image

        for name, reporter in self.reporters:
            data: ReportComparisonData = reporter.report_compare()
            datas += [data]
            iteration_number += [data.iteration_number]
            car_num = data.car_num
            algo_names += [name]
            total_waiting_time += [data.total_waiting_time]
            total_dec_time += [data.total_dec_time]
            avg_car_waiting += [data.avg_car_waiting]
            median_car_waiting += [data.median_car_waiting]
            var_car_waiting += [data.var_car_waiting]
            avg_car_dec += [data.avg_car_dec]
            median_car_dec += [data.median_car_dec]
            var_car_dec += [data.var_car_dec]

        plt.clf()

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
            plt.plot(data.total_dec_df['Iterations'], data.total_dec_df['Total Dec Time'],
                     label=algo_names[i])
        plt.xlabel('Iterations')
        plt.ylabel('Total Dec Time')
        plt.title('Total deceleration time of the\n entire simulation in each iteration')
        plt.legend()
        temp_image_mem2 = BytesIO()
        plt.savefig(temp_image_mem2)
        total_dec_image = Image.open(temp_image_mem2)

        return ComparisonListData(
            algo_names=algo_names, total_waiting_time=total_waiting_time,
            total_dec_time=total_dec_time, avg_car_waiting=avg_car_waiting,
            median_car_waiting=median_car_waiting, var_car_waiting=var_car_waiting,
            car_num=car_num, total_waiting_image=total_waiting_image, avg_car_dec=avg_car_dec,
            median_car_dec=median_car_dec, var_car_dec=var_car_dec,
            total_dec_image=total_dec_image, iteration_number=iteration_number
        )

    @property
    def max_scroll(self):
        return 300 + 530 * (len(self.reporters) - 1)

    def _save_to_file(self):
        path = self._reporters_data().save_to_file()
        if path is not None:
            self.was_saved_text = path
