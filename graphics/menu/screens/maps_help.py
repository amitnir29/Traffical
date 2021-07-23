import pygame

from graphics.menu.screens.screen_activity import Screen


class MapsHelp(Screen):

    def display(self):
        self.screen.fill(self.background)
        # write the text
        self.write_text("This is the", self.screen.get_width() // 2, self.screen.get_height() // 4, 80)
        self.write_text("Maps help screen", self.screen.get_width() // 2, self.screen.get_height() // 4 + 80, 80)
        # Draws the surface object to the screen.
        pygame.display.update()
        # block until click
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        # click
                        running = False
                        break
