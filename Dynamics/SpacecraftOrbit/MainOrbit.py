# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 03:00:38 2020

@author: EO
"""

import numpy as np
from .EarthCenter import EarthCenterOrbit
from Library.math_sup.tools_reference_frame import fmod2
from .TwoBodyProblem import TwoBodyProblem

twopi = 2.0 * np.pi
deg2rad = np.pi / 180.0
rad2deg = 1 / deg2rad


class MainOrbit(object):
    def __init__(self, orbit_spacecraft, step_width, selected_planet):
        self.step_width             = step_width
        self.selected_planet        = selected_planet
        self.orbit_properties       = orbit_spacecraft['Orbit_info']
        self.propagation_properties = orbit_spacecraft['propagate']
        self.current_position       = np.zeros(3)
        self.current_velocity       = np.zeros(3)
        self.propagator_model       = None
        self.wgs                    = self.propagation_properties['wgs']
        self.current_lat            = 0
        self.current_long           = 0
        self.current_alt            = 0
        self.historical_position_i  = []
        self.historical_velocity_i  = []
        self.historical_lats        = []
        self.historical_longs       = []
        self.historical_alts        = []

    def set_propagator(self):
        if self.propagation_properties['propagate_mode'] == 0:
            self.propagator_model = TwoBodyProblem(self.selected_planet.mu,
                                                   self.step_width,
                                                   self.current_position,
                                                   self.current_velocity)
        elif self.propagation_properties['propagate_mode'] == 1:
            line1      = self.orbit_properties[0]
            line2      = self.orbit_properties[1]

            self.propagator_model = EarthCenterOrbit(line1, line2, self.wgs)
        elif self.propagation_properties['propagate_mode'] == 2:
            print('2')
        elif self.propagation_properties['propagate_mode'] == 3:
            print('3')

    def update_orbit(self, array_time):
        self.current_position, self.current_velocity = self.propagator_model.update_state(array_time)

    def TransECItoGeo(self, current_sideral):
        r = np.sqrt(self.current_position[0] ** 2 + self.current_position[1] ** 2)

        long = fmod2(np.arctan2(self.current_position[1], self.current_position[0]) - current_sideral)
        lat = np.arctan2(self.current_position[2], r)

        flag_iteration = True

        while flag_iteration:
            phi = lat
            c = 1 / np.sqrt(1 - self.propagator_model.e2 * np.sin(phi) * np.sin(phi))
            lat = np.arctan2(self.current_position[2] + self.propagator_model.radiusearthkm * c
                             * self.propagator_model.e2 * np.sin(phi) * 1000, r)
            if (np.abs(lat - phi)) <= self.propagator_model.tolerance:
                flag_iteration = False

        alt = r / np.cos(lat) - self.propagator_model.radiusearthkm * c * 1000  # *metros
        if lat > np.pi / 2:
            lat -= twopi
        self.current_alt = alt
        self.current_lat = lat
        self.current_long = long
        return lat, long, alt

    def save_orbit_data(self):
        self.historical_position_i.append(self.current_position)
        self.historical_velocity_i.append(self.current_velocity)
        self.historical_lats.append(self.current_lat)
        self.historical_longs.append(self.current_long)
        self.historical_alts.append(self.current_alt)

    def get_log_values(self):
        report_orbit = {'sat_position_i(X)[m]': np.array(self.historical_position_i)[:, 0],
                        'sat_position_i(Y)[m]': np.array(self.historical_position_i)[:, 1],
                        'sat_position_i(Z)[m]': np.array(self.historical_position_i)[:, 2],
                        'sat_velocity_i(X)[m/s]': np.array(self.historical_velocity_i)[:, 0],
                        'sat_velocity_i(Y)[m/s]': np.array(self.historical_velocity_i)[:, 1],
                        'sat_velocity_i(Z)[m/s]': np.array(self.historical_velocity_i)[:, 2],
                        'lat[rad]': np.array(self.historical_lats),
                        'lon[rad]': np.array(self.historical_longs),
                        'alt[m]': np.array(self.historical_alts)}
        return report_orbit

