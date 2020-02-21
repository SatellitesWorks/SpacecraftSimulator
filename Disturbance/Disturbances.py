
import numpy as np
from .AirDrag import AirDrag
from .GravGrad import GravGrad
from .Magnetic import Magnetic
from .SRP import SRP


class Disturbances(object):
    def __init__(self):
        self.flag = True

    def update_disturbances(self):
        if self.flag:
            return 0

    def get_disturbance_torque(self):
        return 0