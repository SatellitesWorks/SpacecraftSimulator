# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 10:52:34 2020

@author: EO
"""
import numpy as np
from .Components import Components


class Spacecraft(Components):
    def __init__(self,
                 dynamics_satproperties, components_properties):

        self.mass               = dynamics_satproperties['Mass']
        self.Inertia            = dynamics_satproperties['Inertia']
        self.attitude_dynamics  = {'Omega_b': dynamics_satproperties['Omega_b'],
                                   'Quaternion_i2b': dynamics_satproperties['Quaternion_i2b'],
                                   'Inertia': self.Inertia}
        #self.orbit_dynamics     = dynamics_satproperties['Orbit_info']
        #self.tle                = dynamics_satproperties['TLE']

        # Variables for sensor
        self.current_omega_b = np.zeros(3)
        self.current_mag_b = np.zeros(3)
        self.variables_sensor = {'omega': self.current_omega_b,
                                 'mag': self.current_mag_b}

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
        print('\nSpacecraft name: ' + str(dynamics_satproperties['spacecraft_name']))
        # Add components
        print('Spacecraft components:')
        Components.__init__(self, components_properties)

    # temperature, obc, gyro, current, time, power
    def update_spacecraft_components(self, currentDateTime, stepTime):
        self.currentDateTime.append(currentDateTime)
        self.satStepTime.append(stepTime)

        self.variables_sensor['omega'] = self.current_omega_b
        self.variables_sensor['mag'] = self.current_mag_b
        self.update_components(self.variables_sensor)

    # update orbit to ECI frame, attitude to Body frame
    def update_spacecraft_dynamics(self, pos, vel, quaternion, omg, h_total_i, current_torque, lat = 0, long = 0, alt = 0):
        # update variables for sensor
        self.current_omega_b = omg

        # Historical data
        self.position_i.append(pos)
        self.velocity_i.append(vel)
        self.quaternion_b.append(quaternion)
        self.omega_b.append(omg)
        self.h_total.append(h_total_i)
        self.lats.append(lat)
        self.longs.append(long)
        self.alts.append(alt)
        self.torque_t_b.append(current_torque)

    def create_data(self):
        report_attitude = {'omega_t_b(X)[rad/s]': np.array(self.omega_b)[:, 0],
                           'omega_t_b(Y)[rad/s]': np.array(self.omega_b)[:, 1],
                           'omega_t_b(Z)[rad/s]': np.array(self.omega_b)[:, 2],
                           'q_t_i2b(0)[-]': np.array(self.quaternion_b)[:, 0],
                           'q_t_i2b(1)[-]': np.array(self.quaternion_b)[:, 1],
                           'q_t_i2b(2)[-]': np.array(self.quaternion_b)[:, 2],
                           'q_t_i2b(3)[-]': np.array(self.quaternion_b)[:, 3],
                           'gyro_omega1_c(X)[rad/s]': np.array(self.gyro.historical_omega_c)[:, 0],
                           'gyro_omega1_c(Y)[rad/s]': np.array(self.gyro.historical_omega_c)[:, 1],
                           'gyro_omega1_c(Z)[rad/s]': np.array(self.gyro.historical_omega_c)[:, 2]}

        report_orbit = {'sat_position_i(X)[m]': np.array(self.position_i)[:, 0],
                        'sat_position_i(Y)[m]': np.array(self.position_i)[:, 1],
                        'sat_position_i(Z)[m]': np.array(self.position_i)[:, 2],
                        'sat_velocity_i(X)[m/s]': np.array(self.velocity_i)[:, 0],
                        'sat_velocity_i(Y)[m/s]': np.array(self.velocity_i)[:, 1],
                        'sat_velocity_i(Z)[m/s]': np.array(self.velocity_i)[:, 2],}

        report_geo = {'lat[rad]' : np.array(self.lats),
                      'lon[rad]': np.array(self.longs),
                      'alt[m]' : np.array(self.alts)}

        report_torque = {'torque_t_b(X)[Nm]': np.array(self.torque_t_b)[:, 0],
                         'torque_t_b(Y)[Nm]': np.array(self.torque_t_b)[:, 1],
                         'torque_t_b(Z)[Nm]': np.array(self.torque_t_b)[:, 2],
                         'h_total[Nms]': np.array(self.h_total)}

        report_timelog = {'Date time': self.currentDateTime,
                          'time[sec]': self.satStepTime}

        self.master_data_satellite = {**report_timelog, **report_attitude, **report_torque, **report_orbit, **report_geo}


