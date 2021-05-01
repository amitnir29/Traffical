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