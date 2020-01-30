"""
Created on Wed Oct 31 11:23:34 2018

@author: Elias Obreque
"""

#Satellite ground track with TLE
#================================
#TLE must be. txt file
#SUCHAI
#1 42788U 17036Z   18203.83802595  .00001168  00000-0  54122-4 0  9994
#2 42788  97.3987 263.1397 0010661 317.6944  42.3469 15.22024574 60010
#================================
# librery: 
# - matplotlib.ticker, cartopy.crs, cartopy.mpl.gridliner, TLESatellite
#================================

#Import
import matplotlib.ticker as mticker
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
import math
import time
import cartopy.crs as ccrs
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER

from TLESatellite import Sat
from UTCtoJD import JulianDate, JulianEpoch, JD2GMST
from CoordTransf import Plane, ECI, RotationEarth, GroundTrack
from Orbital_Perturbations import J2_lineal, get_perturbation

from mpl_toolkits.mplot3d import Axes3D

#Santiago, Chile
SanLat = -33.4541
SanLon = -70.6502
SanAlt =  570

#=============================================================================

NombreTle = 'suchai'

Area   = 0.01
Masa = 1.13
CD = 2.2

#Julian day initial
t1      = time.strftime('%X %x %Z', time.gmtime())
       
 #=============================================================================
#     Function      
 


def VelViento(x, y, z):
    omegav  = np.array([0, 0, rot_earth])
    pos     = np.array([x, y, z])
    velv    = np.cross(omegav, pos)*R_earth/np.linalg.norm(pos)
    V       = np.linalg.norm(velv)
    return velv[0], velv[1], velv[2], V

def VelRelativa(vx, vy, vz, Vx, Vy, Vz):
	vxr = Vx - vx
	vyr = Vy - vy
	vzr = Vz - vz
	vr 	= math.sqrt(vxr**2 + vyr**2 + vzr**2) 
	return vxr, vyr, vzr, vr


def ECIV(t, x, y, W0, W_dot, RAAN0, RAAN_dot, i):
	X   = [ ]
	Y   = [ ]
	Z   = [ ]
	k   = 0
	for ti in t:
		w  = W0 + W_dot*ti
		raan  = RAAN0 + RAAN_dot*ti
		PO = [[- math.sin(raan)*math.sin(w)*math.cos(i) + math.cos(raan)*math.cos(w), - math.sin(raan)*math.cos(w)*math.cos(i) - math.cos(raan)*math.sin(w), 0],
               [math.cos(raan)*math.sin(w)*math.cos(i) + math.sin(raan)*math.cos(w), math.cos(raan)*math.cos(w)*math.cos(i) - math.sin(raan)*math.sin(w), 0], 
               [math.sin(w)*math.sin(i), math.cos(w)*math.sin(i), 0]]
		Z.append((PO[2][0]*x[k] + PO[2][1]*y[k]))
		X.append(-(PO[0][0]*x[k] + PO[0][1]*y[k]))
		Y.append((PO[1][0]*x[k] + PO[1][1]*y[k]))
		k = k + 1
	return [X, Y, Z]



    
#=============================================================================
#Earth grav. parameter
#=============================================================================
rot_earth   = 7.292115854670501e-5
R_earth     = 6378.1350
m_earth     = 5.9722e24
G           = 6.674e-11
mu          = 3.986044418e5
J2          = 1.08263e-3


InfoTLE = Sat.ReadTLE(NombreTle + '.txt')
sat = Sat.setTLE(InfoTLE)

#Time
JD1, UT1 	= JulianDate(t1)
JD2     	= JD1 + 12/24.0
GM          = JD2GMST(JD1)%360

Yepoch   	= sat.EY
J0epoch  	= JulianEpoch(Yepoch) 
Jepoch   	= J0epoch + sat.DEY

dt       	= 1 #s
tset     	= (JD1 - Jepoch)*24*3600
t        	= np.arange(0,  (JD2 - JD1)*24.0*3600.0, dt)


#ORBITAL ELEMENTS
sat.set_data_rad()

#orbit_elem   = sat.get_OE()
h           = sat.h #orbit_elem[0] # 
ecsat       = sat.ec #orbit_elem[1] #
fsat        = sat.f #orbit_elem[2] #
RAANsat     = sat.RAAN #orbit_elem[3] #
isat        = sat.incl #orbit_elem[4] #
Wsat        = sat.ap #orbit_elem[5] #
asat        = sat.a #orbit_elem[6] #
nsat        = sat.nm #orbit_elem[7] # 


#Correcion de Fecha: movimineto y perturbacion 
doedt = J2_lineal(asat, ecsat, isat)

sat.setOE_pert_ini(doedt, tset)

start_orbit_elem = [55839, 0.17136, 40*np.pi/180, 45*np.pi/180, 28*np.pi/180, 30*np.pi/180] #sat.get_OE()

Cd = 2.2 
At = 0.01
m  = 1
B  = Cd*At/m

# propagator
time_init = time.time()
orbit_elem, r = get_perturbation(t, start_orbit_elem, B)
time_final = time.time()


total_time = time_final - time_init
print('Calculation time:', total_time, '\n')


#%%
x = []
y = []
f = []
e_sat        = [ ]
RAAN_sat     = [ ] 
i_sat        = [ ]
w_sat        = [ ]
n            = [ ]
h            = [ ]
alt          = [ ]

for i in range(len(r)):
    xy = Plane(orbit_elem[i], r[i])
    x.append(xy[0])
    y.append(xy[1])
    e_sat.append(orbit_elem[i][1])
    f.append(orbit_elem[i][2]*180/np.pi%360)
    h.append(orbit_elem[i][0] - orbit_elem[0][0])
    RAAN_sat.append((orbit_elem[i][3])*180/np.pi)
    i_sat.append((orbit_elem[i][4])*180/np.pi)
    w_sat.append((orbit_elem[i][5])*180/np.pi)
    alt.append(r[i] - R_earth)


plt.figure(figsize=(13,6))

plt.subplot(321)
plt.title('Angular moment')
plt.plot(t[0:len(r)]/3600, h)
plt.xlabel('Time [hr]')
plt.grid()

plt.subplot(322)
plt.title('RAAN')
plt.plot(t[0:len(r)]/3600, RAAN_sat)
plt.xlabel('Time [hr]')
plt.grid()

plt.subplot(323)
plt.title('Ar. Per.')
plt.plot(t[0:len(r)]/3600, w_sat)
plt.xlabel('Time [hr]')
plt.grid()	 

plt.subplot(324)
plt.title('Inclination')
plt.plot(t[0:len(r)]/3600, i_sat)
plt.xlabel('Time [hr]')
plt.grid()

plt.subplot(325)
plt.title('ecc')
plt.plot(t[0:len(r)]/3600, e_sat)
plt.xlabel('Time [hr]')
plt.grid()	

plt.subplot(326)
plt.title('Alt')
plt.plot(t[0:len(r)]/3600, alt)
plt.xlabel('Time [hr]')
plt.grid()	

plt.tight_layout()
