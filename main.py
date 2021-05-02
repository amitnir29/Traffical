from graphics.graphics_manager import GraphicsManager
from server.map_creation import create_map
from server.server_runner import next_iter


def main():
    # get the simulation map
    roads, traffic_lights, all_junctions = create_map()
    # create the graphics object
    gm = GraphicsManager()
    # get cars TODO create function that generates cars every once in a while
    cars = list()
    # while the screen is not closed, draw the current state and calculate the next state
    while gm.draw(roads, traffic_lights, cars):
        traffic_lights, cars = next_iter(roads, traffic_lights, all_junctions, cars)


if __name__ == '__main__':
    main()
