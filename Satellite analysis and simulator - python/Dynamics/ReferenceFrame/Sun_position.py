# -*- coding: utf-8 -*-
"""
Created on Tue Mar 19 14:52:52 2019

@author: Elias
"""

import astropy.coordinates as coord
from astropy.time import Time
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt


loc = coord.EarthLocation(lon=0.1 * u.deg,
                          lat=51.5 * u.deg)
now = Time.now()

altaz = coord.AltAz(location=loc, obstime=now)
sun = coord.get_sun(now)

print(sun.transform_to(altaz).alt)

import astropy as ap
v = ap.coordinates.get_sun(now)

N = 59+20
h = 00 + 15/60

x = (2*np.pi/365)*(N - 1 + (h - 12)/24)

declination = 0.006918-0.399912*np.cos(x)+0.070257*np.sin(x)-0.006758*np.cos(2*x)+0.000907*np.sin(2*x)-0.002697*np.cos(3*x)+0.001480*np.sin(3*x)

eqtime = 229.18*(0.00075 + 0.001868*np.cos(x)-0.032077*np.sin(x) - 0.014615*np.cos(2*x)-0.040849*np.sin(2*x))




w = -15*(h - 12) - eqtime*360/(24*60)

print(v)
print(np.degrees(declination), w)



plt.axis([0, 10, 0, 1])

for i in range(10):
    y = np.random.random()
    plt.scatter(i, y)
    plt.pause(0.5)

plt.show()

"""
plt.plot(N, np.degrees(declination))
plt.grid()

plt.figure()
plt.plot(N, eqtime)
plt.grid()


plt.figure()
plt.plot(h, w)
plt.grid()


"""