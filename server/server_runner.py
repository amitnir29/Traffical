from algorithms.tl_manager import TLManager


def next_iter(lights_algorithm: TLManager, traffic_lights, cars):
    """
    calculate the next iteration of the simulation
    :param lights_algorithm: traffic lights manager
    :param traffic_lights: the traffic lights objects, including their state (red/green)
    :param cars: the current cars on the map, should calculate their next position
    :return: new traffic lights and cars lists
    """
    for car in cars:
        car.activate()
    for tl in traffic_lights:
        tl.activate()
    lights_algorithm.manage_lights(cars)
    return traffic_lights, cars
