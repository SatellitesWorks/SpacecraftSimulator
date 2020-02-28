"""
Created: Elias Obreque- -2/26/2020

"""
from ..Abstract.ComponentBase import ComponentBase
import numpy as np


class RWModel(ComponentBase):
    def __init__(self, rwmodel_properties, dynamics):
        ComponentBase.__init__(self, 20)
        self.dynamics_in_rwmodel              = dynamics
        self.inertia                          = float(rwmodel_properties['inertia'])
        self.angular_velocity_init            = float(rwmodel_properties['angular_velocity_init'])
        self.angular_velocity_upperlimit_init = float(rwmodel_properties['angular_velocity_upperlimit_init'])
        self.angular_velocity_lowerlimit_init = float(rwmodel_properties['angular_velocity_lowerlimit_init'])
        self.motor_drive_init                 = bool(rwmodel_properties['motor_drive_init'])
        self.torque_transition                = rwmodel_properties['torque_transition']
        self.firstorder_lag_const             = float(rwmodel_properties['firstorder_lag_const'])
        self.dead_time                        = float(rwmodel_properties['dead_time'])
        self.rw_number_id                     = rwmodel_properties['rw_number_id']
        self.rw_total_torque_b                = np.zeros(3)
        self.max_torque                       = float(rwmodel_properties['max_torque'])

    def main_routine(self, count):

        return

    def calc_torque(self):
        com_period_ = 0.05
        if self.motor_drive_init:
            pre_angular_velocity = 2#ode_angular_velocity_.getAngularVelocity()

        return 0

    def get_torque(self):
        return self.rw_total_torque_b

