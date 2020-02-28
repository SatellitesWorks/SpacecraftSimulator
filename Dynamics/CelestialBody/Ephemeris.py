# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 14:52:52 2019

@author: Elias
"""
from .Earth import Earth


class Ephemeris(object):
    def __init__(self, ephemerides_properties):
        self.inertial_frame = ephemerides_properties['inertial_frame']
        self.aberration_correction = ephemerides_properties['aberration_correction']
        self.center_object = ephemerides_properties['center_object']
        self.num_of_selected_body = ephemerides_properties['num_of_selected_body']

        self.earth = Earth(ephemerides_properties['wgs'])

    def Earth(self):
        self.Earth()



