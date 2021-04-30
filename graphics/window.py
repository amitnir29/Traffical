import pygame
from pygame.locals import *
from graphics.colors import *
from simulation_objects.roadsections.i_road_section import IRoadSection
from simulation_objects.trafficlights.i_traffic_light import ITrafficLight


class Window(pygame.sprite.Sprite):
    def __init__(self, screen, scale):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.scale = scale

    def scale_graphics(self, new_scale):
        """
        changes the scale of the cars and the traffic lights
        :param new_scale: the new scale of the simulation
        """
        self.scale = new_scale

    def draw_car(self, x, y, angle):
        """
        Draws a car
        :param x: the x coordinate of the center of the car
        :param y: the y coordinate of the center of the car
        :param angle: the angle of the car (looking up is 0)
        """
        car_img = pygame.image.load('graphics/images/car.png')
        img = pygame.transform.rotozoom(car_img, angle, self.scale)
        rect = img.get_rect()
        rect.center = (x, y)
        self.screen.blit(img, rect)

    def draw_light(self, light: ITrafficLight):
        """
        Draws a traffic light
        :param light: the traffic light to draw
        """
        # SETTING SIZES AND SCALES
        w = 160 * self.scale
        h = 330 * self.scale
        x, y = light.coordinate.to_tuple()
        rect = Rect(x, y, w, h)
        rect.center = x, y
        circle_radius = 42 * self.scale

        # CENTERS
        red_center = (x, y - 96 * self.scale)
        yellow_center = (x, y)
        green_center = (x, y + 96 * self.scale)

        # COLORS
        red_color = RED if not light.can_pass else DARK_GRAY
        yellow_color = DARK_GRAY
        green_color = GREEN if light.can_pass else DARK_GRAY

        # DRAWING
        pygame.draw.rect(self.screen, GRAY, rect)
        pygame.draw.circle(self.screen, red_color, red_center, circle_radius)
        pygame.draw.circle(self.screen, yellow_color, yellow_center, circle_radius)
        pygame.draw.circle(self.screen, green_color, green_center, circle_radius)

    def draw_road(self, road_section: IRoadSection):
        # DRAWS THE ROAD SECTION:
        coors = road_section.coordinates
        for i in range(len(coors) - 1):
            # yes, the order of [i+1] points is reversed on purpose
            current_points = (coors[i][0].to_tuple(), coors[i][1].to_tuple(),
                              coors[i + 1][1].to_tuple(), coors[i + 1][0].to_tuple())
            pygame.draw.polygon(self.screen, BLACK, current_points)

        # DRAWS THE LANES:
        for line in road_section.get_lines_between_lanes():
            for i in range(len(line) - 1):
                pygame.draw.line(self.screen, WHITE, line[i].to_tuple(), line[i + 1].to_tuple())
