from algorithms.tl_manager import TLManager


def next_iter(light_algos, traffic_lights, cars):
    """
    calculate the next iteration of the simulation
    :param lights_algorithm: traffic lights manager
    :param traffic_lights: the traffic lights objects, including their state (red/green)
    :param cars: the current cars on the map, should calculate their next position
    :return: new traffic lights and cars lists
    """
    __handle_cars(cars)
    __handle_lights(light_algos, traffic_lights)
    return traffic_lights, cars


def __handle_cars(cars):
    # we want to remove all cars that have finished theit path
    to_remove = list()
    for car in cars:
        car.activate()
        if car.has_arrived_destination():
            to_remove.append(car)
    for car in to_remove:
        cars.remove(car)


def __handle_lights(light_algos, traffic_lights):
    for tl in traffic_lights:
        tl.activate()

    for light_algo in light_algos:
        light_algo.manage_lights()
