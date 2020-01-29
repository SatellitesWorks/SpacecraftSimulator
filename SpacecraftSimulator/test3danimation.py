# -*- coding: utf-8 -*-
"""
    Animated 3D sinc function
"""

import numpy as np

twopi = 2*np.pi
deg2rad = 360/twopi

def _gstime(jdut1):
    tut1 = (jdut1 - 2451545.0) / 36525.0;
    temp = -6.2e-6 * tut1 * tut1 * tut1 + 0.093104 * tut1 * tut1 + \
           (876600.0 * 3600 + 8640184.812866) * tut1 + 67310.54841;  # sec
    temp = (temp * deg2rad / 240.0) % twopi  # 360/86400 = 1/240, to deg, to rad

    #  ------------------------ check quadrants ---------------------
    if temp < 0.0:
        temp += twopi;

    return temp

print()