# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 22:30:40 2019

@author: EO
"""
from scipy import integrate
import numpy as np
from Atmospheric_data import denUSSA76
from scipy import signal
import matplotlib.pyplot as plt


#...Conversion factors:
hours = 3600; #Hours to seconds
days = 24*hours; #Days to seconds
deg = np.pi/180; #Degrees to radians

#Earth grav. parameter
#=============================================================================
rot_earth   = 7.292115854670501e-5
R_earth     = 6378.1350
m_earth     = 5.9722e24
G           = 6.674e-11
mu          = 3.986044418e5
J2          = 1.08263e-3


mu  = 398600 #Gravitational parameter (km^3/s^2)
#...Satellite data:
CD  = 2.2 #Drag coefficient
m   = 1.1 #Mass (kg)
A   = 0.01 #Frontal area Cubesat 1U (m^2)


def general_rate(t, y, B):
      
    h       = y[0]
    e       = y[1]
    f       = y[2]
    i       = y[4]
    w       = y[5]
    r       = h**2/mu/(1 + e*np.cos(f))
    
    u       = w + f
    
    #get pertubation force
    [pr_j2, ps_j2, pw_j2]       = get_J2_rsw(i, u, r)
    p_j2 = [pr_j2, ps_j2, pw_j2]
    
    [pr_drag, ps_drag, pw_drag] = get_Drag_rsw(h, e, f, r, B)
    p_drag = [pr_drag, ps_drag, pw_drag]
    
    [pr, ps, pw] = [p_j2[0] + p_drag[0], p_j2[1] + p_drag[1], p_j2[2] + p_drag[2]]
    
    
    hmu         = h/mu
    h2mu        = (h**2)/mu
    invEH       = 1/(e*h)
    invHmu      = 1/(mu*h)
    n           = h/r**2
    rh          = r/h
    
    sinf    = np.sin(f)
    cosf    = np.cos(f)
    sinU    = np.sin(u)
    cosU    = np.cos(u)
    sinI    = np.sin(i)
    
    dhdt    = r*ps
    dedt    = hmu*sinf*pr + invHmu*((h**2 + mu*r)*cosf + mu*e*r)*ps
    dfdt    = n + invEH*(h2mu*cosf*pr - (r + h2mu)*sinf*ps)
    draandt = (rh/sinI)*sinU*pw
    didt    = rh*cosU*pw
    dwdt    = -invEH*(h2mu*cosf*pr - (r + h2mu)*sinf*ps) - pw*rh*sinU/np.tan(i)
    doedt   =  [dhdt, dedt, dfdt, draandt, didt, dwdt]
    return np.array(doedt)
    

def get_perturbation(tspan, oe, B):
        
    h       = oe[0]
    e       = oe[1]
    f       = oe[2]
    raan    = oe[3] 
    i       = oe[4]
    w       = oe[5]
    r       = [h**2/mu/(1 + e*np.cos(f))]
    
    y0 = [h, e, f, raan, i, w]
    y = np.zeros((len(tspan), len(y0)))
    y[0, :] = y0
    dy = integrate.ode(general_rate).set_integrator("dopri5")
    dy.set_initial_value(y0, 0) # initial values
    dy.set_f_params(B)
    tsize = tspan.size
    print('Total iterations: ', tsize, '\n')
    print('Calculating results...\n')
    print('--------------------------')
    for i in range(1, tsize):
        y[i, :] = dy.integrate(tspan[i]) # get one more value, add it to the array
        r.append(y[i, 0]**2/mu/(1 + e*np.cos(y[i, 2])))
        print_percentage(i, tsize)
        if  (r[i] - R_earth) <60:
            break
        elif not dy.successful():
            raise RuntimeError("Could not integrate")
    return y, r

def get_J2_rsw(i, u, r):
    j2const = - 1.5*J2*mu*(R_earth**2)/r**4
    sinII = (np.sin(i))**2
    sinUU = (np.sin(u))**2
    sin2U = np.sin(2*u)
    sin2I = np.sin(2*i)
    sinU  = np.sin(u)
    
    pr = j2const*(1 - 3*sinII*sinUU) 
    ps = j2const*sinII*sin2U
    pw = j2const*sin2I*sinU
    return [pr, ps, pw]

def get_Drag_rsw(h, e, f, r, B):
    
    vs = h/r
    vr = (mu/h)*e*np.sin(f)
    v  = np.sqrt(vs**2 + vr**2)*1000
    
    pv = -0.5*denUSSA76(r - R_earth)*B*v**2
    
    pr = mu/(v*h)*e*pv*np.sin(f)
    ps = h/(v*r)*pv
    pw = 0
    return [pr, ps, pw]

def J2_lineal(a, ec, i): 
    Const       = -(1.5)*J2*(np.sqrt(mu))*(R_earth**2)/(((1-ec**2)**2)*(a**3.5))
    
    dhdt        = 0
    dedt        = 0
    dfdt        = Const*(1 - (3/2)*(np.sin(i))**2)   
    RAAN_dot    = Const*(np.cos(i)) 
    didt        = 0
    W_dot       = Const*(2.5*(np.sin(i))**2 - 2)
    return [dhdt, dedt, dfdt, RAAN_dot, didt, W_dot]
    
def print_percentage(ite, ite_max):
    perce = ((ite)/(ite_max-1))*100
    if perce == 1:
        print('1%')
    elif perce == 10:
        print('10%')    
    elif perce == 20:
        print('20%')
    elif perce == 30:
        print('30%')
    elif perce == 40:
        print('40%')
    elif perce == 50:
        print('50%')
    elif perce == 60:
        print('60%')
    elif perce == 70:
        print('70%')
    elif perce == 80:
        print('80%')
    elif perce == 90:
        print('90%')
    elif perce == 100:
        print('100%')
    return
