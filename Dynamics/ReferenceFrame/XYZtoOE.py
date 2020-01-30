# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 11:29:52 2018

@author: EO
"""
import math
import numpy as np


R_earth     = 6378.1350
mu          = 3.986044418e5

class :
    def __init__(self, D):
        self.x = D[0]
        self.y = D[1]
        self.z = D[2]
        self.vx = D[3]
        self.vy = D[4]
        self.vz = D[5]
        self.pos = D[0], D[1], D[2]
        self.vel = D[3], D[4], D[5]
      
    def getOE(self):
        r = self.x, self.y, self.z
        v = self.vx, self.vy, self.vz
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
        RAAN = math.atan2(C31, - C32)
        i = math.acos(C33)
        w = math.atan2(C13, C23)
        n = math.sqrt(mu/a**3)
        sigma0 = np.dot(r, v)/math.sqrt(mu)
        E0 = math.atan2(sigma0/math.sqrt(a), 1 - rNorm/a)
        M = E0 - e*math.sin(E0)
        f = 2*math.atan(math.sqrt((1.0 + e)/(1.0 - e))*math.tan(0.5*E0))
        return a, e, math.degrees(i), math.degrees(RAAN), math.degrees(w), math.degrees(M)
    




        