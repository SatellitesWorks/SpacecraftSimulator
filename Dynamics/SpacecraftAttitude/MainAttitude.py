# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 00:17:35 2020

@author: EO
"""

import numpy as np
from .AttInertialFrame import AttInertialFrame
from .AttLVLHFrame import AttLVLHFrame


class MainAttitude(AttLVLHFrame, AttInertialFrame):
    def __init__(self, properties_sim_spacecraft):
        self.FRAME = 'J2000' # or 'LVLH'
        self.omega_current = properties_sim_spacecraft['Omega_b']
        self.quaternion_current = properties_sim_spacecraft['Quaternion_i2b']
        self.Inertia = properties_sim_spacecraft['Inertia']
        self.h_rw = [0, 0, 0]
        self.h_total = [0, 0 ,0]
        self._h_total_norm = 0
        self.torque_b = [0, 0, 0]
        self.force_b = [0, 0, 0]
        self.ext_torque = [0, 0, 0]
        self.ext_force = [0, 0, 0]
        self.calAngMom()

    def calAngMom(self):
        if self.FRAME == 'J2000':
            self.calAngMonInertial()
        elif self.FRAME == 'LVLH':
            self.calAngMomLVLH()
        else:
            print('Reference frame to attitude incorrect')

    def update_attitude(self):
        return np.array(self.quaternion_current), np.array(self.omega_current)

    def add_ext_torque(self, ext_torque):
        self.ext_torque = ext_torque

    def add_ext_force(self, ext_force):
        self.ext_force = ext_force

    def add_int_torque(self, torque_b):
        self.torque_b = torque_b

    def add_int_force(self, force_b):
        self.force_b = force_b









