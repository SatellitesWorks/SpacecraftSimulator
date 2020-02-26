"""
Created: Elias Obreque- -2/26/2020

"""

import numpy as np


class RWModel(object):
    def __init__(self, rwmodel_properties):
        self.inertia = float(rwmodel_properties['inertia'])
        self.angular_velocity_init = float(rwmodel_properties['angular_velocity_init'])
        self.angular_velocity_upperlimit_init = float(rwmodel_properties['angular_velocity_upperlimit_init'])
        self.angular_velocity_lowerlimit_init = float(rwmodel_properties['angular_velocity_lowerlimit_init'])
        self.motor_drive_init = float(rwmodel_properties['motor_drive_init'])
        self.torque_transition = rwmodel_properties['torque_transition']
        self.firstorder_lag_const = float(rwmodel_properties['firstorder_lag_const'])
        self.dead_time = float(rwmodel_properties['dead_time'])
        self.rw_number_id = rwmodel_properties['rw_number_id']

    def update(self, va):
        return


