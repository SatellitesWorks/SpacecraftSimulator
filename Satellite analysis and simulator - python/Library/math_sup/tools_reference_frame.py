# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 14:34:09 2020

@author: EO
"""
import numpy as np

R_earth     = 6378.1350
mu          = 3.986044418e5
twopi       = 2.0 * np.pi
deg2rad     = np.pi / 180.0;
omega_earth = 7.2921150*1e-5 # rad/s

def fmod2(x):
    if x > np.pi:
        x -= twopi
    elif x < -np.pi:
        x += twopi
    else:
        x = x
    return x

def gstime(jdut1):

    jd0  = jdut1[0]
    utc  = jdut1[1]
    tut1 = (jd0 - 2451545.0) / 36525.0
    GST0_time = -6.2e-6* tut1**3 + 0.093104 * tut1**2 + 8640184.812866*tut1 + 24110.54841  #  sec

    GST0_rad = (GST0_time * deg2rad / 240.0)# 360/86400 = 1/240, to deg, to rad

    GST_rad = (GST0_rad + omega_earth*utc/3600)% twopi
    #  ------------------------ check quadrants ---------------------
    if GST_rad < 0.0:
        GST_rad += twopi;
    return GST_rad

def jday(year, mon, day, hr, minute, sec):
  jd0 = 367.0 * year - 7.0 * (year + ((mon + 9.0) // 12.0)) * 0.25 // 1.0 + 275.0 * mon // 9.0 + day + 1721013.5
  utc = ((sec / 60.0 + minute) / 60.0 + hr) #  utc in hours#
  return [jd0, utc]

def getOE(r, v):
    h = np.cross(r, v)
    rNorm = np.linalg.norm(r)
    vNorm = np.linalg.norm(v)
    eVect = np.cross(v, h)/mu - r/rNorm
    e = np.linalg.norm(eVect)
    a = 1/(2/rNorm-vNorm**2/mu)
    ie = eVect/e
    ih = h/np.linalg.norm(h)
    ip = np.cross(ih, ie)
    C31 = ih[0]
    C32 = ih[1]
    C33 = ih[2]
    C13 = ie[2]
    C23 = ip[2]
    RAAN = np.atan2(C31, - C32)
    i = np.arccos(C33)
    w = np.arctan2(C13, C23)
    #n = np.sqrt(mu/a**3)
    sigma0 = np.dot(r, v)/np.sqrt(mu)
    E0 = np.arctan2(sigma0/np.sqrt(a), 1 - rNorm/a)
    M = E0 - e*np.sin(E0)
    #f = 2*np.arctan(np.sqrt((1.0 + e)/(1.0 - e))*np.tan(0.5*E0))
    return a, e, np.rad2deg(i), np.rad2deg(RAAN), np.rad2deg(w), np.rad2deg(M)
