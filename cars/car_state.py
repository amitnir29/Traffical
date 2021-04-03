class CarState:

    def __init__(self):
        self.__driving = False
        self.__moving_lane = False
        self.__stopping = False

    @property
    def driving(self):
        return self.__driving

    @driving.setter
    def driving(self, flag):
        self.__driving = flag

    @property
    def moving_lane(self):
        return self.__moving_lane

    @moving_lane.setter
    def moving_lane(self, flag):
        self.__moving_lane = flag

    @property
    def stopping(self):
        return self.__stopping

    @stopping.setter
    def stopping(self, flag):
        self.__stopping = flag
