import pygame

from gui.screens.screen_activity import Screen
from gui.simulation_graphics.colors import RED

TITLE_SCREEN_PORTION = 4
FOOTER_SCREEN_PORTION = 10
TITLE_TEXT_SIZE = 40
ALGO_HEADER_TEXT_SIZE = 30
ALGO_DATA_TEXT_SIZE = 16
ALGO_ROW_DIFF = 5


class AlgosHelp(Screen):

    def display(self):
        total_delta_y = 0
        scroll_delta_y = 50
        self.__draw_all(total_delta_y)
        # block until click
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        return
                    elif event.button == 4:
                        # scroll up
                        total_delta_y = max(0, total_delta_y - scroll_delta_y)
                        self.__draw_all(total_delta_y)
                    elif event.button == 5:
                        # scroll down
                        max_scroll = self.screen.get_height() * 1
                        total_delta_y = min(max_scroll, total_delta_y + scroll_delta_y)
                        self.__draw_all(total_delta_y)

    def __draw_all(self, delta_y):
        self.screen.fill(self.background)
        self.__draw_algos_data(delta_y)
        self.__draw_titles()
        # Draws the surface object to the screen.
        pygame.display.update()

    def __draw_titles(self):
        # title
        pygame.draw.rect(self.screen, RED, [0, 0, self.screen.get_width(),
                                            self.screen.get_height() // TITLE_SCREEN_PORTION])
        self.write_text("In this screen you choose an", self.screen.get_width() // 2,
                        self.screen.get_height() // (4 * TITLE_SCREEN_PORTION), TITLE_TEXT_SIZE)
        self.write_text("algorithm which will determine the ", self.screen.get_width() // 2,
                        self.screen.get_height() // (4 * TITLE_SCREEN_PORTION) + TITLE_TEXT_SIZE, TITLE_TEXT_SIZE)
        self.write_text("traffic light's colors", self.screen.get_width() // 2,
                        self.screen.get_height() // (4 * TITLE_SCREEN_PORTION) + TITLE_TEXT_SIZE * 2,
                        TITLE_TEXT_SIZE)
        # footer
        pygame.draw.rect(self.screen, RED,
                         [0, (FOOTER_SCREEN_PORTION - 1) * self.screen.get_height() // FOOTER_SCREEN_PORTION,
                          self.screen.get_width(), self.screen.get_height() // FOOTER_SCREEN_PORTION])
        self.write_text("click to go back", self.screen.get_width() // 2,
                        (2 * FOOTER_SCREEN_PORTION - 1) * self.screen.get_height() // (2 * FOOTER_SCREEN_PORTION),
                        TITLE_TEXT_SIZE)

    def __draw_algos_data(self, delta_y):
        curr_y = self.screen.get_height() // TITLE_SCREEN_PORTION + ALGO_DATA_TEXT_SIZE + 10 - delta_y
        # Naive
        curr_y += ALGO_HEADER_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("Naive Algorithm", self.screen.get_width() // 2, curr_y, ALGO_HEADER_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("Round robin for each junction separately + cannot cause starvation",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        # MCAlgo
        curr_y += ALGO_HEADER_TEXT_SIZE + ALGO_ROW_DIFF * 5
        self.write_text("MCAlgo", self.screen.get_width() // 2, curr_y, ALGO_HEADER_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("Most Crowded algorithm. Chooses the road with the largest number of cars heading to it.",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("When deciding on a green light, the light will stay green for a minimal time",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("(cannot change too fast, wasting time on switching lights)",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        # MCTL
        curr_y += ALGO_HEADER_TEXT_SIZE + ALGO_ROW_DIFF * 5
        self.write_text("MCTL", self.screen.get_width() // 2, curr_y, ALGO_HEADER_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("A version of MCAlgo in which a green light cannot",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("stay green forever – has a maximal threshold.",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        # RLQ explanation
        curr_y += ALGO_HEADER_TEXT_SIZE + ALGO_ROW_DIFF * 5
        self.write_text("RLQ – An abstract algorithm that",
                        self.screen.get_width() // 2, curr_y, ALGO_HEADER_TEXT_SIZE - 5)
        curr_y += ALGO_HEADER_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("gives priority to busy roads",
                        self.screen.get_width() // 2, curr_y, ALGO_HEADER_TEXT_SIZE - 5)
        curr_y += ALGO_HEADER_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("(roads with the largest density)",
                        self.screen.get_width() // 2, curr_y, ALGO_HEADER_TEXT_SIZE - 5)
        # RLQTL
        curr_y += ALGO_HEADER_TEXT_SIZE + ALGO_ROW_DIFF * 3
        self.write_text("RLQTL", self.screen.get_width() // 2, curr_y, ALGO_HEADER_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("RLQTL is an implementation of RLQ in which",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("the density is calculated as the sum of all",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("cars dividing by the total length of all lane",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        # RLQRS
        curr_y += ALGO_HEADER_TEXT_SIZE + ALGO_ROW_DIFF * 3
        self.write_text("RLQRS", self.screen.get_width() // 2, curr_y, ALGO_HEADER_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("RLQRS is an implementation of RLQ in which",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("the density is calculated for each lane separately",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("to create an 'average density' for the car",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        # Cost Based
        curr_y += ALGO_HEADER_TEXT_SIZE + ALGO_ROW_DIFF * 5
        self.write_text("Cost Based", self.screen.get_width() // 2, curr_y, ALGO_HEADER_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("A cost-based algorithm which chooses the",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("most efficient decision according to the cost",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("For each car that passes – the cost is increased",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        curr_y += ALGO_DATA_TEXT_SIZE + ALGO_ROW_DIFF
        self.write_text("For each car that waits – the cost is decreased",
                        self.screen.get_width() // 2, curr_y, ALGO_DATA_TEXT_SIZE)
        # TODO MLAlgo
