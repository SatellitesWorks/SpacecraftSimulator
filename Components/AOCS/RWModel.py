"""
Created: Elias Obreque- -2/26/2020

"""
from ..Abstract.ComponentBase import ComponentBase
from .RWODE import RWODE
import numpy as np

RAD2RPM = 60 / (2 * np.pi)
RPM2RAD = 1 / RAD2RPM


class RWModel(ComponentBase, RWODE):
    def __init__(self, rwmodel_properties, dynamics):
        ComponentBase.__init__(self, 20)
        self.dynamics_in_rwmodel = dynamics
        self.inertia = float(rwmodel_properties['inertia'])
        self.angular_velocity_init = float(rwmodel_properties['angular_velocity_init'])
        self.angular_velocity_upperlimit_init = RPM2RAD * float(rwmodel_properties['angular_velocity_upperlimit_init'])
        self.angular_velocity_lowerlimit_init = RPM2RAD * float(rwmodel_properties['angular_velocity_lowerlimit_init'])
        self.motor_drive = bool(rwmodel_properties['motor_drive_init'])
        self.torque_transition = rwmodel_properties['torque_transition']
        self.firstorder_lag_const = float(rwmodel_properties['firstorder_lag_const'])
        self.coasting_lag_coef = float(rwmodel_properties['firstorder_lag_const'])
        self.dead_time = float(rwmodel_properties['dead_time'])
        self.rw_number_id = rwmodel_properties['rw_number_id']
        self.rw_torque_b = np.zeros(3)
        self.max_torque = float(rwmodel_properties['max_torque'])
        self.step_width = float(rwmodel_properties['prop_step'])
        self.target_angular_accl_before = 0.0
        self.target_angular_accl = []
        RWODE.__init__(self, self.step_width, self.angular_velocity_init, 0.0, self.firstorder_lag_const)

        self.epsilon = 1e-9
        self.angular_momentum_b = 0

    def main_routine(self, count):

        return

    def calc_torque(self):
        com_period_ = 0.05
        ite = 1
        pre_angular_velocity = self.get_angular_velocity()
        if not self.motor_drive:
            self.set_lag_coef(self.coasting_lag_coef)
            self.set_target_angular_velocity(0)
            while ite < com_period_ / self.step_width:
                self.update_ode()
                ite += 1
            angular_velocity = self.get_angular_velocity()
            angular_acc = (angular_velocity - pre_angular_velocity) / com_period_
            self.rw_torque_b = self.inertia * angular_acc
            self.angular_momentum_b = self.inertia * angular_velocity
            return self.rw_torque_b
        else:
            self.set_lag_coef(self.firstorder_lag_const)
            angular_acc_with_deadtime = self.target_angular_accl[0]
            # Target velocity at the end of the loop of ODE
            target_ang_velocity = pre_angular_velocity + angular_acc_with_deadtime * com_period_
            del self.target_angular_accl[0]
            # Set velocity target
            self.set_target_angular_velocity(target_ang_velocity)
            while ite < com_period_ / self.step_width:
                self.update_ode()
                ite += 1
            angular_velocity = self.get_angular_velocity()
            angular_acc = (angular_velocity - pre_angular_velocity) / com_period_
            self.rw_torque_b = self.inertia * angular_acc * self.torque_transition
            self.angular_momentum_b = self.inertia * angular_velocity
            return self.rw_torque_b

    def control_power(self):
        angular_velocity = self.get_angular_velocity()
        if abs(angular_velocity) > self.angular_velocity_upperlimit_init:
            self.set_driver(False)
        elif abs(angular_velocity) < self.angular_velocity_lowerlimit_init:
            self.set_driver(True)

    def set_driver(self, flag):
        self.motor_drive = flag

    def set_torque(self, torque):
        sign = 1
        if torque < 0:
            sign = -1
        if abs(torque) < self.max_torque:
            angular_acc = torque / self.inertia
        else:
            angular_acc = sign * self.max_torque / self.inertia

        i = 1
        while i < self.dead_time / self.step_width:
            self.target_angular_accl.insert(len(self.target_angular_accl), 0)
            i += 1
        self.target_angular_accl.insert(len(self.target_angular_accl), angular_acc)

        self.target_angular_accl_before = angular_acc

    def get_torque(self):
        return self.rw_torque_b
