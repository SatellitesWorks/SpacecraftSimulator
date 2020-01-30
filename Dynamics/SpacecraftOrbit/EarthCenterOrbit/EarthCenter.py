# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 05:54:44 2020

@author: EO
#satrec.inclo: Inclination [rad]
#satrec.nodeo: Right Ascension of the Ascending Node [rad]
#satrec.argpo: Argument of Perigee [rad]
#satrec.mo   : Mean Anomaly [rad]
#satrec.ecco : Eccentricity [-]
#satrec.no: Mean Motion [rad/min]

"""

from Library.sgp4.earth_gravity import wgs72, wgs72old, wgs84
from Library.sgp4.io import twoline2rv
from Library.math_sup.tools_reference_frame import fmod2, _gstime

import numpy as np

twopi       = 2.0 * np.pi
deg2rad     = np.pi / 180.0
rad2deg     = 1 / deg2rad

class earthcenterorbit(object):

    def __init__(self,
                 line1,
                 line2,
                 wgs):
        self.line1 = line1
        self.line2 = line2

        if wgs == 0:
            self.wgs = wgs72old
            self.radiusearthkm = 6378.135 # km
            self.f = 1.0 / 298.26
        elif wgs == 1:
            self.wgs = wgs72
            self.radiusearthkm = 6378.135  # km
            self.f = 1.0 / 298.26
        elif wgs == 2:
            self.wgs = wgs84
            self.radiusearthkm = 6378.137 # km
            self.f = 1.0 / 298.257223563

        self.e2 = self.f * (2 - self.f)
        self.satellite = twoline2rv(self.line1, self.line2, self.wgs)
        self.current_side = 0
        self.tolerance = 1e-10 # rad

    def propagate_in_earth(self, string_time):
        position_i, velocity_i, self.current_jd = self.satellite.propagate(string_time[0], # YYYY
                                                                           string_time[1], # MM
                                                                           string_time[2], # DD
                                                                           string_time[3], # HH
                                                                           string_time[4], # MM
                                                                           string_time[5]) # SS
        self.position_i = np.array(position_i)*1000
        self.velocity_i = np.array(velocity_i)*1000
        return self.position_i, self.velocity_i # [m]

    def TransECItoGeo(self):
        self.current_side = _gstime(self.current_jd) # rad
        r = np.sqrt(self.position_i[0]**2 + self.position_i[1]**2)

        long = fmod2(np.arctan2(self.position_i[1], self.position_i[0]) - self.current_side)
        lat  = np.arctan2(self.position_i[2], r)

        flag_iteration = True
        while flag_iteration:
            phi = lat
            c = 1 / np.sqrt(1 - self.e2 * np.sin(phi) * np.sin(phi))
            lat = np.arctan2(self.position_i[2] + self.radiusearthkm*c*self.e2*np.sin(phi) * 1000, r)
            if (np.abs(lat - phi)) <= self.tolerance:
                flag_iteration = False

        alt = r/np.cos(lat) - self.radiusearthkm * c * 1000  # *metros
        if lat > np.pi/2:
            lat -= twopi
        return lat, long, alt