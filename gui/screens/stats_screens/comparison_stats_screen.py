from io import BytesIO
from typing import List

import pygame
from PIL import Image
from matplotlib import pyplot as plt

from gui.screens.screen_activity import TITLES_SCREEN_PORTION
from gui.screens.stats_screens.stats_screen_parent import StatsScreenParent
from server.geometry.point import Point
from server.statistics.runs_data import ReportComparisonData, ComparisonListData


class ComparisonStatsScreen(StatsScreenParent):

    def __init__(self, screen: pygame.Surface, reporters):
        super().__init__(screen)
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

                f"average cars waiting per iteration: {round(reporters_data.avg_car_waiting[i], 3)}",
                f"median cars waiting per iteration: {reporters_data.median_car_waiting[i]}",
                f"variance cars waiting per iteration: {round(reporters_data.var_car_waiting[i], 3)}",

                f"average cars decelerating per iteration: {round(reporters_data.avg_car_dec[i], 3)}",
                f"median cars decelerating per iteration: {reporters_data.median_car_dec[i]}",
                f"variance cars decelerating per iteration: {round(reporters_data.var_car_dec[i], 3)}",

                f"average waiting of cars per iteration: {round(reporters_data.waiting_per_car_avg[i], 3)}",
                f"median waiting of cars per iteration: {reporters_data.waiting_per_car_median[i]}",
                f"variance waiting of cars per iteration: {round(reporters_data.waiting_per_car_variance[i], 3)}"
            ]))

        self.write_text(f"number of cars: {reporters_data.car_num}", middle_x, 500 - total_delta_y, 40)
        for i, pair in enumerate(texts):
            head, data_lines = pair
            start_i = 600 + i * 600 - total_delta_y
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
            self.write_text(f"saved to: {self.was_saved_text}", self.screen.get_width() // 2, 15, 15)
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
        avg_car_dec: List[float] = []
        median_car_dec: List[float] = []
        var_car_dec: List[float] = []
        total_dec_df: Image
        cars_waiting_avg: List[float] = []
        cars_waiting_med: List[float] = []
        cars_waiting_var: List[float] = []

        for name, reporter in self.reporters:
            data: ReportComparisonData = reporter.report_compare()
            datas.append(data)
            iteration_number.append(data.iteration_number)
            car_num = data.car_num
            algo_names.append(name)
            total_waiting_time.append(data.total_waiting_time)
            total_dec_time.append(data.total_dec_time)
            avg_car_waiting.append(data.avg_car_waiting)
            median_car_waiting.append(data.median_car_waiting)
            var_car_waiting.append(data.var_car_waiting)
            avg_car_dec.append(data.avg_car_dec)
            median_car_dec.append(data.median_car_dec)
            var_car_dec.append(data.var_car_dec)
            cars_waiting_avg.append(data.waiting_per_car_avg)
            cars_waiting_med.append(data.waiting_per_car_median)
            cars_waiting_var.append(data.waiting_per_car_variance)

        plt.clf()

        for i, data in enumerate(datas):
            plt.plot(data.total_waiting_df['Iterations'], data.total_waiting_df['Total Waiting Time'],
                     label=algo_names[i])
        plt.xlabel('Iterations')
        plt.ylabel('Aggregated Waiting Time')
        plt.title('Aggregated waiting time of the entire simulation\nin each iteration')
        plt.legend()
        temp_image_mem = BytesIO()
        plt.savefig(temp_image_mem)
        total_waiting_image = Image.open(temp_image_mem)

        plt.clf()

        for i, data in enumerate(datas):
            plt.plot(data.total_dec_df['Iterations'], data.total_dec_df['Total Dec Time'],
                     label=algo_names[i])
        plt.xlabel('Iterations')
        plt.ylabel('Aggregated Dec Time')
        plt.title('Aggregated deceleration time of the\n entire simulation in each iteration')
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
            total_dec_image=total_dec_image, iteration_number=iteration_number, waiting_per_car_avg=cars_waiting_avg,
            waiting_per_car_median=cars_waiting_med, waiting_per_car_variance=cars_waiting_var
        )

    @property
    def max_scroll(self):
        return 400 + 650 * (len(self.reporters) - 1)

    def _save_to_file(self):
        path = self._reporters_data().save_to_file()
        if path is not None:
            self.was_saved_text = path
