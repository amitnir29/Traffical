from graphics.graphics_manager import GraphicsManager
from server.geometry.point import Point
from server.map_creation import create_map
from server.server_runner import next_iter
from server.simulation_objects.cars.car import Car
from server.simulation_objects.cars.position import Position


def main():
    # get the simulation map
    roads, traffic_lights, all_junctions = create_map()
    # create the graphics object
    gm = GraphicsManager(fps=10)
    # get cars TODO create function that generates cars every once in a while
    cars = list()
    cars.append(Car([roads[3], roads[1]], 0, 0))
    # while the screen is not closed, draw the current state and calculate the next state
    while gm.draw(roads, traffic_lights, cars):
        traffic_lights, cars = next_iter(roads, traffic_lights, all_junctions, cars)


if __name__ == '__main__':
    main()
