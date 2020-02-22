import numpy as np


class GravGrad(object):
    def __init__(self, grav_dist_properties):
        self.dist_gra_flag  = grav_dist_properties['gra_calculation']
        self.grav_logging   = grav_dist_properties['gra_logging']

        self.current_grav_torque_b = np.zeros(3)

    def get_grav_torque_b(self):
        return self.current_grav_torque_b
