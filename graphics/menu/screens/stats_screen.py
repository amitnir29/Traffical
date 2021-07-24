from dataclasses import dataclass

import pygame

from graphics.menu.screens.screen_activity import Screen, TITLES_SCREEN_PORTION
from server.geometry.point import Point
from server.statistics.stats_reporter import ReportScreenData


class StatsScreen(Screen):
    def __init__(self, screen: pygame.Surface, background, reporter):
        super().__init__(screen, background)
        self.reporter = reporter

    def display(self):
        # ddd
        x=5
        report_data: ReportScreenData = self.reporter.report()
        total_delta_y = 0
        scroll_delta_y = 50
        self.__draw_all_data(report_data, total_delta_y)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        # finish
                        return
                    elif event.button == 4:
                        # scroll up
                        total_delta_y = max(-self.screen.get_height() // TITLES_SCREEN_PORTION,
                                            total_delta_y - scroll_delta_y)
                        self.__draw_all_data(report_data, total_delta_y)
                    elif event.button == 5:
                        # scroll down
                        max_scroll = 500
                        total_delta_y = min(max_scroll, total_delta_y + scroll_delta_y)
                        self.__draw_all_data(report_data, total_delta_y)

    def __draw_all_data(self, report_data, total_delta_y):
        self.screen.fill(self.background)
        middle_x = self.screen.get_width() // 2

        # graphs
        self.draw_image(self.pil_image_to_surface(report_data.cars_waiting_image),
                        Point(210, self.screen.get_height() // TITLES_SCREEN_PORTION - total_delta_y))
        self.draw_image(self.pil_image_to_surface(report_data.total_waiting_image),
                        Point(590, self.screen.get_height() // TITLES_SCREEN_PORTION - total_delta_y))
        self.draw_image(self.pil_image_to_surface(report_data.cars_neg_acc_image),
                        Point(210, self.screen.get_height() // TITLES_SCREEN_PORTION + 300 - total_delta_y))
        self.draw_image(self.pil_image_to_surface(report_data.total_neg_acc_image),
                        Point(590, self.screen.get_height() // TITLES_SCREEN_PORTION + 300 - total_delta_y))
        # texts
        texts = [
            f"number of cars: {report_data.car_num}",
            f"total waiting time: {report_data.total_waiting_time}",
            f"average car waiting time: {round(report_data.avg_car_waiting, 3)}",
            f"median car waiting time: {report_data.median_car_waiting}",
            f"variance car waiting time: {round(report_data.var_car_waiting, 3)}",
            f"total negative acceleration time: {report_data.total_neg_acc_time}",
            f"average car negative acceleration time: {round(report_data.avg_car_neg_acc, 3)}",
            f"median car negative acceleration time: {report_data.median_car_neg_acc}",
            f"variance car negative acceleration time: {round(report_data.var_car_neg_acc, 3)}"
        ]
        for i, txt in enumerate(texts):
            self.write_text(txt, middle_x, 700 + i * 40 - total_delta_y, 30)
        # write header and footer
        pygame.draw.rect(self.screen, self.background, [0, 0, self.screen.get_width(),
                                                        self.screen.get_height() // TITLES_SCREEN_PORTION])
        self.write_text("Simulation Statistics", middle_x, self.screen.get_height() // 8, 60)
        pygame.draw.rect(self.screen, self.background, [0, self.screen.get_height() - 50, self.screen.get_width(), 50])
        self.write_text("click to go back", middle_x, self.screen.get_height() - 50, 40)
        # Draws the surface object to the screen.
        pygame.display.update()

    def pil_image_to_surface(self, pil_image):
        return pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode).convert()

    def draw_image(self, image, center: Point, scale=0.5):
        img = pygame.transform.rotozoom(image, 0, scale)
        rect = img.get_rect()
        rect.center = center.to_tuple()
        self.screen.blit(img, rect)
