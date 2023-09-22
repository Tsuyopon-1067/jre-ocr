import re

class FrameDataWriter:

    SPEED_FILE = 'speed.csv'
    LIMIT_FILE = 'limit.csv'

    speed = -1
    distance = -1
    limit = -1

    def __init__(self):
        self.sf = open(self.SPEED_FILE, 'w')
        self.lf = open(self.LIMIT_FILE, 'w')

    def write(self, arg):
        if self.speed == -1:
            self.speed = arg.speed
        if self.limit == -1 and arg.limit >= 10:
            self.limit = arg.limit
        if self.distance == -1:
            self.distance = arg.distance

        if (abs(self.speed - arg.speed) < 1) and (arg.limit >= 10) and (abs(self.distance - arg.distance) < 10):
            self.speed = arg.speed
            self.distance = arg.distance
            self.limit = arg.limit
            self.sf.write("{},{}\n".format(self.distance, self.speed))
            self.lf.write("{},{}\n".format(self.distance, self.limit))