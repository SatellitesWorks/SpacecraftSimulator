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
        self.omega = properties_sim_spacecraft['Omega_b']
        self.quaternion = properties_sim_spacecraft['Quaternion_i2b']
        self.Inertia = properties_sim_spacecraft['Inertia']
        self.h_rw = [0, 0, 0]
        self.torque_b = [0, 0, 0]

    def update_attitude(self):
        return [0,0,0, 1], [0,0,0]






