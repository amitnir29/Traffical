from db.dataclasses.road_data import RoadData
from graphics.graphics_manager import GraphicsManager
from map_creation import create_map, normalize_data
from simulation_objects.geometry.point import Point
from simulation_objects.roadsections.road_section import RoadSection
from simulation_objects.trafficlights.traffic_light import TrafficLight


def main():
    # get the simulation map
    roads, traffic_lights, all_junctions = create_map()
    # TODO this is a test road section
    # points = [(Point(0, 0), Point(200, 0)), (Point(0, 400), Point(200, 400)), (Point(300, 800), Point(400, 650))]
    # roads = {1: RoadSection(RoadData(1, points, 15, 100), set())}
    # TODO this is a test light
    # traffic_lights = [TrafficLight(list(), Point(400, 400))]
    # create the graphics object
    WIDTH = 800
    HEIGHT = 800
    gm = GraphicsManager(width=WIDTH, height=HEIGHT)
    normalize_data(roads, traffic_lights, all_junctions, WIDTH, HEIGHT)
    # get cars TODO create function that generates cars every once in a while
    cars = list()
    # while the screen is not closed, draw the current state and calculate the next state
    while gm.draw(roads, traffic_lights, cars):
        traffic_lights, cars = next_iter(roads, traffic_lights, all_junctions, cars)


def next_iter(roads, traffic_lights, all_junctions, cars):
    """
    calculate the next iteration of the simulation
    :param roads: the roads of the map
    :param traffic_lights: the traffic lights objects, including their state (red/green)
    :param all_junctions: the junctions objects of the map
    :param cars: the current cars on the map, should calculate their next position
    :return: new traffic lights and cars lists
    """
    # TODO
    return traffic_lights, cars


if __name__ == '__main__':
    main()
