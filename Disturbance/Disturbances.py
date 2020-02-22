
import numpy as np
from .AirDrag import AirDrag
from .GravGrad import GravGrad
from .MagDist import Magnetic
from .SRP import SRP


class Disturbances(Magnetic, GravGrad):
    def __init__(self, disturbance_properties):
        Magnetic.__init__(self, disturbance_properties['MAG'])
        GravGrad.__init__(self, disturbance_properties['GRA'])

        self.dist_torque_b = np.zeros(3)
        self.dist_force_b  = np.zeros(3)

    def update_disturbances(self, Mag_b):
        self.update_output()

        if self.dist_mag_flag:
            self.dist_torque_b += self.get_mag_torque_b(Mag_b)
        elif self.dist_gra_flag:
            self.dist_torque_b += self.get_grav_torque_b()

    def get_dist_torque(self):
        return self.dist_torque_b

    def get_dis_force(self):
        return self.dist_force_b

    def update_output(self):
        self.dist_torque_b = np.zeros(3)
        self.dist_force_b  = np.zeros(3)
