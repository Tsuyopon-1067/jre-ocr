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
        self.speed = arg.speed
        self.distance = arg.distance
        self.limit = arg.limit
        self.sf.write("{},{}\n".format(self.distance, self.speed))
        self.lf.write("{},{}\n".format(self.distance, self.limit))