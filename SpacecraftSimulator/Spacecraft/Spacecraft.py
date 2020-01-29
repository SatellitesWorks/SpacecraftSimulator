# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 10:52:34 2020

@author: EO
"""
import numpy as np

class spacecraft(object):
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

    def Update_state(self): # temperature, obc, gyro, acc, etc

        return

    def save_dynamics(self, pos, vel, quat, omg, lat = 0, long = 0, alt = 0): # update orbit to ECI frame, attitude to Body frame
        self.position_i.append(pos)
        self.velocity_i.append(vel)
        self.quaternion_b.append(quat)
        self.omega_b.append(omg)
        self.lats.append(lat)
        self.longs.append(long)
        self.alts.append(alt)

    def get_dynamics(self):
        self.attitude = {'Omega_b': np.array(self.omega_b),
                         'Quaternion_i2b': np.array(self.quaternion_b)}

        self.orbit = {'Position': np.array(self.position_i),
                      'Velocity': np.array(self.velocity_i)}

        self.Geo = {'lats' : np.array(self.lats),
                    'longs': np.array(self.longs),
                    'alts' : np.array(self.alts)}

        self.dynamics = {'Attitude'  : self.attitude,
                         'Orbital'   : self.orbit,
                         'Geocentric': self.Geo}

        return self.dynamics


    def Generate_torque_b(self):
        return


    def generate_force_b(self):

        return


