# -*- coding: utf-8 -*-
"""
Created on Wed Apr 17 15:01:25 2019

@author: Elias
"""
import math
import numpy as np

#Earth grav. parameter
#=============================================================================
rot_earth   = 7.292115854670501e-5
R_earth     = 6378.1350
m_earth     = 5.9722e24
G           = 6.674e-11
mu          = 3.986044418e5


def Kepler_ite(M, e):
    err     = 1.0e-10
    E0      = M
    t       = 1
    itt     = 0
    while(t):
          E     =  M + e*math.sin(E0);
          if ( abs(E - E0) < err):
              t = 0
          E0    = E
          itt   = itt + 1
          E     = E0
    return E

def Plane(orbit_elem, r):
    f        = orbit_elem[2] #
    x = (r*np.cos(f))
    y = (r*np.sin(f))
    #vr.append((mu/h)*math.sin(f[k]))
    #vf.append((mu/h)*(ec + math.cos(f[k])))
    #vx = ((mu/h)*math.sin(ang))
    #vy = ((mu/h)*(ec + math.cos(ang)))
    plane_elem = [x, y]
    return plane_elem

def ECI(t, x, y, W, W_dot, RAAN, RAAN_dot, i):
    X   	= [ ]
    Y   	= [ ]
    Z   	= [ ]
    k   	= 0
    Raan 	= [ ]
    WW 		= [ ]
    for DT in t:
        w  = W + W_dot*DT
        raan  = RAAN + RAAN_dot*DT
        Raan.append(math.degrees(raan))
        WW.append(math.degrees(w))
        PO = [[- math.sin(raan)*math.sin(w)*math.cos(i) + math.cos(raan)*math.cos(w), - math.sin(raan)*math.cos(w)*math.cos(i) - math.cos(raan)*math.sin(w), 0],
               [math.cos(raan)*math.sin(w)*math.cos(i) + math.sin(raan)*math.cos(w), math.cos(raan)*math.cos(w)*math.cos(i) - math.sin(raan)*math.sin(w), 0], 
               [math.sin(w)*math.sin(i), math.cos(w)*math.sin(i), 0]]
        X.append(PO[0][0]*x[k] + PO[0][1]*y[k])
        Y.append(PO[1][0]*x[k] + PO[1][1]*y[k])
        Z.append(PO[2][0]*x[k] + PO[2][1]*y[k])
        k = k + 1     
    return [X, Y, Z, Raan, WW]

def GroundTrack(Xe, Ye, Ze, r):
    lat 	= [ ]
    lon 	= [ ]
    alt   = [ ]
    #Latitude and longitude (geocentric equatorial frame)
    for k in range(len(Xe)):
        alt.append(r[k] - R_earth)
        lon.append(math.degrees(math.atan2(Ye[k],Xe[k])))
        lat.append(math.degrees(math.asin(Ze[k]/r[k])))
    return [lon, lat, alt]

def RotationEarth(X, Y, Z, GM, rot_earth, t):
    Xe  = [ ]
    Ye  = [ ]
    Ze  = [ ]
    ke  = 0
    for DT in t:
        theta = GM*math.pi/180.0 + rot_earth*DT
        RO = [[math.cos(theta), math.sin(theta), 0],
               [-math.sin(theta), math.cos(theta), 0],
               [0, 0, 1]]
        Xe.append(RO[0][0]*X[ke] + RO[0][1]*Y[ke])
        Ye.append(RO[1][0]*X[ke] + RO[1][1]*Y[ke])
        Ze.append(Z[ke])
        ke = ke + 1
    return [Xe, Ye, Ze]

