"""
Created on Sat Feb 22 10:37:53 2020

@author: EO
"""

import numpy as np


class Magnetic(object):
    def __init__(self, mag_dist_properties):
        self.dist_mag_flag      = mag_dist_properties['mag_calculation']
        self.mag_logging        = mag_dist_properties['mag_logging']
        self.mag_rmm_const_b    = mag_dist_properties['mag_rmm_const_b']
        self.mag_rmm_rwdev      = mag_dist_properties['mag_rmm_rwdev']
        self.mag_rmm_limit      = mag_dist_properties['mag_rmm_rwlimit']
        self.mag_rmm_wnvar      = mag_dist_properties['mag_rmm_wnvar']
        self.current_mag_torque_b = np.zeros(3)

        # create rmm_b to add noise
        self.mag_rmm_b = self.mag_rmm_const_b

        # constat to change [nT] to [T]
        self.mag_unit_change = 1.0e-9

    def get_mag_torque_b(self, Mag_b):
        # add gaussian noise and randomwalk  to the residual magnetic moment
        #self.add_gs_rw()
        self.current_mag_torque_b = self.mag_unit_change * np.cross(self.mag_rmm_b, Mag_b)
        return self.current_mag_torque_b

    def add_gd_rw(self):
        return



