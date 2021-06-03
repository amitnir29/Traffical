from graphics.graphics_manager import GraphicsManager
from server.geometry.point import Point
from server.map_creation import create_map
from server.server_runner import next_iter
from server.simulation_objects.cars.car import Car
from server.simulation_objects.cars.position import Position
from algorithms.algos_list import MCAlgo, NaiveAlgo


def main():
    # get the simulation map
    roads, traffic_lights, all_junctions = create_map()
    # create the graphics object
    gm = GraphicsManager(fps=10)
    # get cars TODO create function that generates cars every once in a while
    cars = list()
    # cars.append(Car([roads[4], roads[3], roads[2], roads[6]], 0.0001, max_speed=0.0001))
    # cars.append(Car([roads[4], roads[3], roads[2], roads[6]], 0))  # TODO why the simulation gets stuck?
    cars.append(Car([roads[26], roads[28], roads[16], roads[5], roads[6], roads[15], roads[24], roads[25], roads[26]],
                    0))  # TODO why the simulation gets stuck?
    # while the screen is not closed, draw the current state and calculate the next state
    lights_algorithm = MCAlgo(traffic_lights, all_junctions)
    while gm.draw(roads, traffic_lights, cars):
        traffic_lights, cars = next_iter(lights_algorithm, traffic_lights, cars)


if __name__ == '__main__':
    main()
