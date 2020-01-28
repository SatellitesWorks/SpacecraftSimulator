# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 14:58:02 2019

@author: Elias
"""

import math
import numpy as np 

def JulianDate(t):
    m   = float(t[9:11])
    d   = float(t[12:14]) 
    y   = float('20' + t[15] + t[16])
    UT  = (float(t[0] + t[1]) + float(t[3] + t[4])/60.0 + float(t[6] + t[7])/3600.0) % 24.0
    J0  = 367.0*y - math.floor(7.0*(y + math.floor((m + 9.0)/12.0))/4.0) + math.floor(275.0*m/9.0) + d + 1721013.5
    JD  = J0 + UT/24.0
    return JD, UT

def JulianEpoch(y):
    m   = 1
    J0  = 367.0*y - math.floor(7.0*(y + math.floor((m + 9.0)/12.0))/4.0) + math.floor(275.0*m/9.0) + 1721013.5
    return J0

def JD2GMST(JD):
    JD0     = np.round(JD) - 0.5
    UT      = (JD - JD0)*24.0      #%Time in hours past previous midnight
    D0      = JD0 - 2451545.0   #%Compute the number of days since J2000
    T       = D0/36525          #%Compute the number of centuries since J2000
    GMST0   = 100.4606184 + 36000.77004*T + 0.000387933*T**2.0 - (2.583e-8)*T**3.0
    GMST0   = GMST0 - math.floor(GMST0/360.0)*360.0
    GMST    = GMST0 + 360.98564724*UT/24.0
    return GMST
