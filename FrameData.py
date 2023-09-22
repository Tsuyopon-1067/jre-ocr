import re

class FrameData:
    speed = 0
    distance = 0
    limit = 0

    def __init__(self, s):
        s = re.sub(r'\n\s*\n', '\n', s)
        lines = s.split('\n')
        if len(lines) >= 4:
            match_speed = re.search(r"(\d+(\.\d+)?)", lines[0])
            if match_speed:
                self.speed = match_speed.group(1)
                self.speed = float(self.speed)

            match_distance = re.search(r"(\d+(\.\d+)?)", lines[3])
            if match_distance:
                self.distance = match_distance.group(1)
                self.distance = float(self.distance)

            match_limit = re.search(r"(\d+(\.\d+)?)", lines[1])
            if match_limit:
                self.limit = match_limit.group(1)
                self.limit = int(self.limit)

    def to_string(self):
        return "{}km/h, {}m, [{}]".format(self.speed, self.distance, self.limit)