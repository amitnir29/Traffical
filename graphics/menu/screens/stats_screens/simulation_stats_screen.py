from dataclasses import dataclass

import pygame

from graphics.menu.screens.screen_activity import Screen, TITLES_SCREEN_PORTION
from graphics.menu.screens.stats_screens.stats_screen_parent import StatsScreenParent
from server.geometry.point import Point
from server.statistics.stats_reporter import ReportScreenData


class SimulationStatsScreen(StatsScreenParent):
    def __init__(self, screen: pygame.Surface, background, reporter):
        super().__init__(screen, background)
        self.reporter = reporter

    def __draw_all_data(self, total_delta_y, reporter_data):
        self.screen.fill(self.background)
        middle_x = self.screen.get_width() // 2
        # graphs
        self.draw_image(self.pil_image_to_surface(reporter_data.cars_waiting_image),
                        Point(210, self.screen.get_height() // TITLES_SCREEN_PORTION + 120 - total_delta_y))
        self.draw_image(self.pil_image_to_surface(reporter_data.total_waiting_image),
                        Point(590, self.screen.get_height() // TITLES_SCREEN_PORTION + 120 - total_delta_y))
        self.draw_image(self.pil_image_to_surface(reporter_data.cars_neg_acc_image),
                        Point(210, self.screen.get_height() // TITLES_SCREEN_PORTION + 420 - total_delta_y))
        self.draw_image(self.pil_image_to_surface(reporter_data.total_neg_acc_image),
                        Point(590, self.screen.get_height() // TITLES_SCREEN_PORTION + 420 - total_delta_y))
        # texts
        texts = [
            f"number of cars: {reporter_data.car_num}",
            f"total waiting time: {reporter_data.total_waiting_time}",
            f"average car waiting time: {round(reporter_data.avg_car_waiting, 3)}",
            f"median car waiting time: {reporter_data.median_car_waiting}",
            f"variance car waiting time: {round(reporter_data.var_car_waiting, 3)}",
            f"total negative acceleration time: {reporter_data.total_neg_acc_time}",
            f"average car negative acceleration time: {round(reporter_data.avg_car_neg_acc, 3)}",
            f"median car negative acceleration time: {reporter_data.median_car_neg_acc}",
            f"variance car negative acceleration time: {round(reporter_data.var_car_neg_acc, 3)}"
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

    def __reporters_data(self):
        return self.reporter.report()
