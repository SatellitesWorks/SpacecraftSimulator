# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 03:00:38 2020

@author: EO
"""

from .EarthCenterOrbit.EarthCenter import EarthCenterOrbit


class MainOrbit(object):
    def __init__(self, propagation_properties, orbit_properties):

        self.orbit_properties       = orbit_properties
        self.propagation_properties = propagation_properties
        self.current_position       = 0
        self.current_velocity       = 0
        self.orbit_propagate        = None
        self.wgs                    = self.propagation_properties[0]['wgs']

    def set_propagator(self):
        if self.propagation_properties[0]['propagate_mode'] == 0:
            print('0')
        elif self.propagation_properties[0]['propagate_mode'] == 1:
            line1      = self.orbit_properties[0]
            line2      = self.orbit_properties[1]

            self.orbit_propagate = EarthCenterOrbit(line1, line2, self.wgs)
        elif self.propagation_properties[0]['propagate_mode'] == 2:
            print('2')
        elif self.propagation_properties[0]['propagate_mode'] == 3:
            print('3')

    def update_orbit(self, array_time):
        self.current_position, self.current_velocity = self.orbit_propagate.propagate_in_earth(array_time)
