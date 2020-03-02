# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 10:52:34 2020

@author: EO
"""
import numpy as np
from .SubSystems import SubSystems
from Dynamics.Dynamics import Dynamics
from Dynamics.ClockGenerator import ClockGenerator


class Spacecraft(SubSystems):
    def __init__(self, dynamics_properties, components_properties, simtime):

        self.simtime = simtime
        self.dynamics = Dynamics(dynamics_properties, self.simtime)

        self.master_data_satellite = {}
        print('Spacecraft name: ' + str(dynamics_properties['Attitude']['spacecraft_name']))
        # Add components
        print('Spacecraft components:')
        SubSystems.__init__(self, components_properties, self.dynamics)
        self.clockgenerator = ClockGenerator(self.subsystems, self.system_name)

    def update(self):
        # Dynamics updates
        self.dynamics.update()

        # Tick the time on component
        i = 0
        while i < self.simtime.stepsimTime*100:
            self.clockgenerator.tick_to_components()
            i += 1
        return

    # update orbit to ECI frame, attitude to Body frame
    #def update(self, pos, vel, quaternion, omg, h_total_i, current_torque, lat = 0, long = 0, alt = 0):
    def update_data(self):
        # Historical data
        self.save_log_values()
        self.dynamics.attitude.save_attitude_data()
        self.dynamics.orbit.save_orbit_data()
        self.simtime.save_simtime_data()

    def create_report(self):
        report_attitude = self.dynamics.attitude.get_log_values()
        report_orbit = self.dynamics.orbit.get_log_values()
        report_timelog = self.simtime.get_log_values()

        report_sensor = {}

        i = 1
        for subsys in self.system_name:
            if self.subsystems[subsys] is not None:
                if hasattr(self.subsystems[subsys].components, 'gyro'):
                    gyro = self.subsystems[subsys].components.gyro
                    report_sensor['gyro_omega' + str(i) + '_c(X)[rad/s]'] = np.array(gyro.historical_omega_c)[:, 0]
                    report_sensor['gyro_omega' + str(i) + '_c(Y)[rad/s]'] = np.array(gyro.historical_omega_c)[:, 1]
                    report_sensor['gyro_omega' + str(i) + '_c(Z)[rad/s]'] = np.array(gyro.historical_omega_c)[:, 2]
                    i += 1

        self.master_data_satellite = {**report_timelog, **report_attitude, **report_orbit, **report_sensor}
