# -*- coding: utf-8 -*-
"""
Created on Sun Apr 28 18:50:36 2019

@author: EO
"""

import numpy as np
from Orbital_Perturbations import get_perturbation
import matplotlib.pyplot as plt


mu = 3.986044418e5

t = 0
rp = 6678
ra = 9440

raan = np.deg2rad(45)
i = np.deg2rad(28)
w = np.deg2rad(30)
f = np.deg2rad(40)


def Plane(orbit_elem):
    h        = orbit_elem[0] # 
    e        = orbit_elem[1] #
    f        = orbit_elem[2] #
            
    r = ((h**2)/mu)/(1 + e*np.cos(f))
    x = (r*np.cos(f))
    y = (r*np.sin(f))
    plane_elem = [r, f, x, y]
    return plane_elem

def setOE_pert(oe, doedt ,dt):
    h    = oe[0] + doedt[0]*dt 
    ec   = oe[1] + doedt[1]*dt
    RAAN = oe[3] + doedt[3]*dt
    incl = oe[4] + doedt[4]*dt
    ap   = oe[5] + doedt[5]*dt
    f    = (oe[2] + doedt[2]*dt)%(2*np.pi)
    return [h, ec, f, RAAN, incl, ap]


def Kepler_ite(M, e):
    err     = 1.0e-10
    E0      = M
    t       = 1
    itt     = 0
    while(t):
        E     =  M + e*np.sin(E0)
        if (abs(E - E0) < err):
            t = 0
        E0    = E
        itt   = itt + 1
        E     = E0
    return E  


e = (ra - rp)/(ra + rp)
a = rp/(1 - e)
T = (2*np.pi/np.sqrt(mu))*a**(3.0/2.0)
h = np.sqrt(a*mu*(1 - e**2))
n = 2*np.pi/T


r = a*(1 - e**2)/(1 + e*np.cos(f))

oe0 = [h, e, f, raan, i, w, r]


t = np.linspace(0, 15*3600, 3000)
dt = t[1]

oe = get_perturbation(t, oe0)
    
    
e_sat        = []
RAAN_sat     = []
i_sat        = []
w_sat        = []
x            = [] 
y            = []
h = []
for i in range(len(t)):
    e_sat.append(oe[i][1])
    RAAN_sat.append(oe[i][3]*180/np.pi)
    i_sat.append(oe[i][4]*180/np.pi)
    w_sat.append(oe[i][5]*180/np.pi)
    h.append(oe[i][0] - oe[0][0])
    

plt.figure()
plt.plot(t, h)
plt.grid()    
    
plt.figure()
plt.title('RAAN')
plt.plot(t/3600, np.array(RAAN_sat) - raan*180/np.pi)
plt.grid()

plt.figure()
plt.title('w')
plt.plot(t/3600, np.array(w_sat) - w*180/np.pi)
plt.grid()	


plt.figure()
plt.title('i')
plt.plot(t/3600, np.array(i_sat) - i*180/np.pi)
plt.grid()	

plt.figure()
plt.title('e')
plt.plot(t/3600, np.array(e_sat) - e)
plt.grid()	    


    