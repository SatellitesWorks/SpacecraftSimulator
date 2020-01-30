# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 10:52:34 2020

@author: EO
"""
import numpy as np


class Spacecraft(object):
    def __init__(self,
                 dynamics_satproperties, components_properties):

        self.mass               = dynamics_satproperties['Mass']
        self.Inertia            = dynamics_satproperties['Inertia']
        self.attitude_dynamics  = {'Omega_b': dynamics_satproperties['Omega_b'],
                                   'Quaternion_i2b': dynamics_satproperties['Quaternion_i2b']}
        self.orbit_dynamics     = dynamics_satproperties['Orbit_info']
        self.tle                = dynamics_satproperties['TLE']
        self.position_i         = []
        self.velocity_i         = []
        self.quaternion_b       = []
        self.omega_b            = []
        self.lats               = []
        self.longs              = []
        self.alts               = []
        self.currentDateTime    = []
        self.satStepTime        = []

    # temperature, obc, gyro, acc, etc, time
    def update_spacecraft_state(self, currentDateTime, stepTime):
        self.currentDateTime.append(currentDateTime)
        self.satStepTime.append(stepTime)

    # update orbit to ECI frame, attitude to Body frame
    def update_spacecraft_dynamics(self, pos, vel, quaternion, omg, lat = 0, long = 0, alt = 0):
        self.position_i.append(pos)
        self.velocity_i.append(vel)
        self.quaternion_b.append(quaternion)
        self.omega_b.append(omg)
        self.lats.append(lat)
        self.longs.append(long)
        self.alts.append(alt)

    def create_data(self):
        report_attitude = {'omega_t_b(X)[rad/s]': np.array(self.omega_b)[:, 0],
                           'omega_t_b(Y)[rad/s]': np.array(self.omega_b)[:, 1],
                           'omega_t_b(Z)[rad/s]': np.array(self.omega_b)[:, 2],
                           'q_t_i2b(0)[-]': np.array(self.quaternion_b)[:, 0],
                           'q_t_i2b(1)[-]': np.array(self.quaternion_b)[:, 1],
                           'q_t_i2b(2)[-]': np.array(self.quaternion_b)[:, 2],
                           'q_t_i2b(3)[-]': np.array(self.quaternion_b)[:, 3]}

        report_orbit = {'sat_position_i(X)[m]': np.array(self.position_i)[:, 0],
                        'sat_position_i(Y)[m]': np.array(self.position_i)[:, 1],
                        'sat_position_i(Z)[m]': np.array(self.position_i)[:, 2],
                        'sat_velocity_i(X)[m/s]': np.array(self.velocity_i)[:, 0],
                        'sat_velocity_i(Y)[m/s]': np.array(self.velocity_i)[:, 1],
                        'sat_velocity_i(Z)[m/s]': np.array(self.velocity_i)[:, 2],}

        report_geo = {'lat[rad]' : np.array(self.lats),
                      'lon[rad]': np.array(self.longs),
                      'alt[m]' : np.array(self.alts)}
        
        report_timelog = {'Date time': self.currentDateTime,
                          'time[sec]': self.satStepTime}

        self.master_data_satellite = {**report_timelog, **report_attitude, **report_orbit, **report_geo}


    def Generate_torque_b(self):
        return


    def generate_force_b(self):

        return


