
from .MagEnv import MagEnv


class Environment(MagEnv):
    def __init__(self, radius):
        MagEnv.__init__(self, radius)
        self.calkok = True

    def update_environment(self, decyear, sideral, lat, lon, alt, q_i2b):
        if self.calkok:
            self.calc_mag(decyear, sideral, lat, lon, alt, q_i2b)


