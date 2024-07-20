# hill.py
import math


class Hill:
    def __init__(self, width, height, hill_height):
        self.width = width
        self.height = height
        self.hill_height = hill_height

    def get_hill_y(self, x):
        relative_x = (x - self.width / 2) / (self.width / 2)
        y = self.height - self.hill_height * (math.cos(relative_x * math.pi) + 1) / 2
        return int(y)

    def get_hill_angle(self, x):
        dx = 1
        y1 = self.get_hill_y(x)
        y2 = self.get_hill_y(x + dx)
        return math.atan2(y2 - y1, dx)

    def is_on_hill(self, x, y, object_size):
        hill_y = self.get_hill_y(x + object_size / 2)
        return y + object_size >= hill_y

    def adjust_position(self, x, y, object_size):
        hill_y = self.get_hill_y(x + object_size / 2)
        return x, hill_y - object_size
