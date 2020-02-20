# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 14:52:52 2019

@author: Elias
"""
from .Earth import Earth
import astropy.coordinates as coord
from astropy.time import Time
import astropy.units as u

class Ephemeris(Earth):
    def __init__(self, wgs):
        Earth.__init__(self, wgs)

    def Earth(self):
        self.Earth()



