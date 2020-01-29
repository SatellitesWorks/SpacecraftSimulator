# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 03:00:38 2020

@author: EO
"""

from .SpacecraftOrbit.EarthCenterOrbit.EarthCenter import earthcenterorbit


class main_dynamics(object):
    def __init__(self, propagation_properties, orbit_properties, simtime_class):

        self.orbit_properties       = orbit_properties
        self.propagation_properties = propagation_properties
        self.simulation_time        = simtime_class

    def set_propagator(self):
        if self.propagation_properties[0]['propagate_mode'] == 0:
            print('0')
        elif self.propagation_properties[0]['propagate_mode'] == 1:
            line1 = self.orbit_properties[0]
            line2 = self.orbit_properties[1]
            wgs   = self.propagation_properties[0]['wgs']
            self.orbit_propagate = earthcenterorbit(line1, line2, wgs)
        elif self.propagation_properties[0]['propagate_mode'] == 2:
            print('2')
        elif self.propagation_properties[0]['propagate_mode'] == 3:
            print('3')

    def update_orbit(self):
        array_time,_ = self.simulation_time.get_array_time()
        current_position, current_velocity = self.orbit_propagate.propagate(array_time)
        return current_position, current_velocity

    def update_attitude(self):
        return [0,0,0, 0], [0,0,0]
