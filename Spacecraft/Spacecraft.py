# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 10:52:34 2020

@author: EO
"""
import numpy as np
from .SubSystems import SubSystems
from Dynamics.Dynamics import Dynamics
from Dynamics.ClockGenerator import ClockGenerator


class Spacecraft(object):
    def __init__(self, dynamics_properties, components_properties, simtime):

        self.simtime = simtime
        self.dynamics = Dynamics(dynamics_properties, self.simtime)

        # variables for historical data
        self.position_i         = []
        self.velocity_i         = []
        self.quaternion_b       = []
        self.omega_b            = []
        self.lats               = []
        self.longs              = []
        self.alts               = []
        self.currentDateTime    = []
        self.satStepTime        = []
        self.torque_t_b         = []
        self.h_total            = []

        self.master_data_satellite = {}
        print('Spacecraft name: ' + str(dynamics_properties['Attitude']['spacecraft_name']))
        # Add components
        print('Spacecraft components:')

        self.subsystems = SubSystems(components_properties, self.dynamics)
        self.clockgenerator = ClockGenerator(self.subsystems)

    def update(self):
        # Dynamics updates
        self.dynamics.update()

        # Tick the time on component
        i = 0
        while i < self.simtime.stepsimTime*10:
            self.clockgenerator.tick_to_components()
            i += 1
        return

    def generate_torque_b(self):
        return self.subsystems.generate_torque_b()

    # update orbit to ECI frame, attitude to Body frame
    #def update(self, pos, vel, quaternion, omg, h_total_i, current_torque, lat = 0, long = 0, alt = 0):
    def update_data(self):
        # Historical data
        self.subsystems.update()
        self.currentDateTime.append(self.simtime.get_array_time()[1])
        self.satStepTime.append(self.simtime.maincountTime)
        self.position_i.append(self.dynamics.orbit.current_position)
        self.velocity_i.append(self.dynamics.orbit.current_velocity)
        self.quaternion_b.append(self.dynamics.attitude.current_quaternion_i2b())
        self.omega_b.append(self.dynamics.attitude.current_omega_b)
        self.h_total.append(self.dynamics.attitude.h_total_norm)
        self.lats.append(self.dynamics.orbit.current_lat)
        self.longs.append(self.dynamics.orbit.current_long)
        self.alts.append(self.dynamics.orbit.current_alt)
        self.torque_t_b.append(self.dynamics.attitude.total_torque_b())

    def create_data(self):
        report_attitude = {'omega_t_b(X)[rad/s]': np.array(self.omega_b)[:, 0],
                           'omega_t_b(Y)[rad/s]': np.array(self.omega_b)[:, 1],
                           'omega_t_b(Z)[rad/s]': np.array(self.omega_b)[:, 2],
                           'q_t_i2b(0)[-]': np.array(self.quaternion_b)[:, 0],
                           'q_t_i2b(1)[-]': np.array(self.quaternion_b)[:, 1],
                           'q_t_i2b(2)[-]': np.array(self.quaternion_b)[:, 2],
                           'q_t_i2b(3)[-]': np.array(self.quaternion_b)[:, 3]}

        report_sensor = {}
        i = 1
        for subsys in self.subsystems.system_name:
            if hasattr(self.subsystems.components[subsys], 'gyro'):
                gyro = self.subsystems.components[subsys].gyro
                report_sensor['gyro_omega' + str(i) + '_c(X)[rad/s]'] = np.array(gyro.historical_omega_c)[:, 0]
                report_sensor['gyro_omega' + str(i) + '_c(Y)[rad/s]'] = np.array(gyro.historical_omega_c)[:, 1]
                report_sensor['gyro_omega' + str(i) + '_c(Z)[rad/s]'] = np.array(gyro.historical_omega_c)[:, 2]
                i += 1

        report_orbit = {'sat_position_i(X)[m]': np.array(self.position_i)[:, 0],
                        'sat_position_i(Y)[m]': np.array(self.position_i)[:, 1],
                        'sat_position_i(Z)[m]': np.array(self.position_i)[:, 2],
                        'sat_velocity_i(X)[m/s]': np.array(self.velocity_i)[:, 0],
                        'sat_velocity_i(Y)[m/s]': np.array(self.velocity_i)[:, 1],
                        'sat_velocity_i(Z)[m/s]': np.array(self.velocity_i)[:, 2]}

        report_geo = {'lat[rad]': np.array(self.lats),
                      'lon[rad]': np.array(self.longs),
                      'alt[m]': np.array(self.alts)}

        report_torque = {'torque_t_b(X)[Nm]': np.array(self.torque_t_b)[:, 0],
                         'torque_t_b(Y)[Nm]': np.array(self.torque_t_b)[:, 1],
                         'torque_t_b(Z)[Nm]': np.array(self.torque_t_b)[:, 2],
                         'h_total[Nms]': np.array(self.h_total)}

        report_timelog = {'Date time': self.currentDateTime,
                          'time[sec]': self.satStepTime}

        self.master_data_satellite = {**report_timelog, **report_attitude, **report_torque,
                                      **report_orbit, **report_geo, **report_sensor}
