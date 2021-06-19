from copy import copy


class StatsReporter:
    def __init__(self, cars):
        self.cars = copy(cars)

    def report(self):
        return [car.iteration for car in self.cars], sum(car.iteration for car in self.cars)