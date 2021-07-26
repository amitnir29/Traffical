import os
from datetime import datetime

import pandas as pd
import pygame

from gui.screens.screen_activity import TITLES_SCREEN_PORTION
from gui.screens.stats_screens.stats_screen_parent import StatsScreenParent
from server.geometry.point import Point
from server.statistics.runs_data import ReportSimulationData


class SimulationStatsScreen(StatsScreenParent):
    def __init__(self, screen: pygame.Surface, background, reporter):
        super().__init__(screen, background)
        self.reporter = reporter

    def save(self, reporter_data: ReportSimulationData):
        data = {
            "Number of Iteration": reporter_data.iteration_number,
            "Total Waiting Time": reporter_data.total_waiting_time,
            "Total Deceleration Time": reporter_data.total_dec_time,
            "Average Waiting Time": reporter_data.avg_car_waiting,
            "Median Waiting Time": reporter_data.median_car_waiting,
            "Variance Waiting Time": reporter_data.var_car_waiting,
            "Number of Cars": reporter_data.car_num,
            "Average Deceleration Time": reporter_data.avg_car_dec,
            "Median Deceleration Time": reporter_data.median_car_dec,
            "Variance Deceleration Time": reporter_data.var_car_dec
        }
        df = pd.DataFrame(data)
        dir_path = "server/statistics/results"
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        os.mkdir(dir_path + "/" + dt_string)
        new_dir_path = dir_path + "/" + dt_string
        df.to_csv(new_dir_path + "/" + "data.csv")
        reporter_data.total_dec_image.save(new_dir_path + "/" + "Total Deceleration.png")
        reporter_data.total_waiting_image.save(new_dir_path + "/" + "Total Waiting.png")
        reporter_data.cars_dec_image.save(new_dir_path + "/" + "Cars Deceleration.png")
        reporter_data.cars_waiting_image.save(new_dir_path + "/" + "Cars Waiting.png")

    def _draw_all_data(self, total_delta_y, reporter_data:ReportSimulationData):
        self.screen.fill(self.background)
        middle_x = self.screen.get_width() // 2
        # graphs
        self.draw_image(self.pil_image_to_surface(reporter_data.cars_waiting_image),
                        Point(210, self.screen.get_height() // TITLES_SCREEN_PORTION + 120 - total_delta_y))
        self.draw_image(self.pil_image_to_surface(reporter_data.total_waiting_image),
                        Point(590, self.screen.get_height() // TITLES_SCREEN_PORTION + 120 - total_delta_y))
        self.draw_image(self.pil_image_to_surface(reporter_data.cars_dec_image),
                        Point(210, self.screen.get_height() // TITLES_SCREEN_PORTION + 420 - total_delta_y))
        self.draw_image(self.pil_image_to_surface(reporter_data.total_dec_image),
                        Point(590, self.screen.get_height() // TITLES_SCREEN_PORTION + 420 - total_delta_y))
        # texts
        texts = [
            f"number of iterations: {reporter_data.iteration_number}",
            f"number of cars: {reporter_data.car_num}",
            f"total waiting time: {reporter_data.total_waiting_time}",
            f"average car waiting time: {round(reporter_data.avg_car_waiting, 3)}",
            f"median car waiting time: {reporter_data.median_car_waiting}",
            f"variance car waiting time: {round(reporter_data.var_car_waiting, 3)}",
            f"total deceleration time: {reporter_data.total_dec_time}",
            f"average car deceleration time: {round(reporter_data.avg_car_dec, 3)}",
            f"median car deceleration time: {reporter_data.median_car_dec}",
            f"variance car deceleration time: {round(reporter_data.var_car_dec, 3)}"
        ]
        for i, txt in enumerate(texts):
            self.write_text(txt, middle_x, 800 + i * 40 - total_delta_y, 30)
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
        return self.reporter.report()

    @property
    def max_scroll(self):
        return 530

