# -*- coding: utf-8 -*-
"""
Created on Mon Aug 20 16:13:05 2018

@author: ELias Obreque
"""
from Update_TLE import get_UpdateTLE
import numpy as np

#Earth grav. parameter
#=============================================================================
rot_earth   = 7.292115854670501e-5
R_earth     = 6378.1350
m_earth     = 5.9722e24
G           = 6.674e-11
mu          = 3.986044418e5
J2          = 1.08263e-3

class Sat:
    def __init__(self, name, num, cla, YL, LNY, pl, EY, DEY, M1M,  M2M, BSTAR,
                 ET, esn, checksum, incl, RAAN, ec, ap, MA, nm, RNE):
        # TLE
        self.name   = name
        self.num    = num
        self.cla    = cla
        self.YL     = YL
        self.LNY    = LNY
        self.pl     = pl
        self.EY     = EY
        self.DEY    = DEY
        self.M1M    = M1M
        self.M2M    = M2M
        self.BSTAR  = BSTAR
        self.ET     = ET
        self.esn    = esn
        self.checksum = checksum
        self.incl   = incl
        self.RAAN   = RAAN
        self.ec     = ec/10000000.0
        self.ap     = ap
        self.MA     = MA
        self.nm     = (2.0*np.pi*nm/86400.0)
        self.RNE    = RNE
        # Orbit
        self.a      = (mu**(1.0/3.0))/(self.nm**(2.0/3.0))
        self.h      = np.sqrt(mu*self.a*(1 - self.ec**2)) 
        E           = Kepler_ite(self.MA, self.ec)
        self.f      = 2*np.arctan(np.sqrt((1.0 + self.ec)/(1.0 - self.ec))*np.tan(0.5*E))
        self.r      = ((self.h**2)/mu)/(1 + self.ec*np.cos(self.f)) 
        try:
            get_UpdateTLE(num, name)
        except:
            print('\nNo internet for Update\n')
        print('Satellite created:', name)            
   
        
    def ReadTLE(Archivo):
        TLE_open    = open(Archivo,'r')
        TLE_read    = TLE_open.read().split('\n')
        data        = ['','','']
        k = 0
        for i in range(len(TLE_read)):
            if TLE_read[i] != '':
                data[k] = TLE_read[i]
                k = k + 1               
        TLE_open.close()
        info        = data
        return info 
    
    def setTLE(info):
        title = info[0]
        line_1 = info[1] 
        line_2 = info[2]
        satel  = Sat(title, line_1[2:7], line_1[8], line_1[9:11], line_1[11:14], line_1[14:17],
                     float('20'+line_1[18:20]), float(line_1[20:32]), line_1[33:43], line_1[44:52],
                     line_1[53:61], line_1[62], line_1[64:68], line_1[68], float(line_2[8:16]),
                     float(line_2[17:25]), float(line_2[26:33]), float(line_2[33:42]),
                     float(line_2[43:51]), float(line_2[52:63]), float(line_2[63:68]))
        return satel


    def set_data_rad(self):
        self.incl = self.incl*np.pi/180.0
        self.RAAN = self.RAAN*np.pi/180.0
        self.ap   = self.ap*np.pi/180.0
        self.MA   = self.MA*np.pi/180.0
        return

    def get_OE(self):
        h       = self.h 
        e       = self.ec
        f       = (self.f)%(2*np.pi)
        RAAN    = (self.RAAN)%(2*np.pi)
        i       = (self.incl)%(2*np.pi)
        w       = (self.ap)%(2*np.pi)
        a       = (mu**(1.0/3.0))/(self.nm**(2.0/3.0))
        n       = self.nm
        r       = ((h**2)/mu)/(1 + e*np.cos(f))
        return [h, e, f, RAAN, i, w, a, n, r]
    
   
    def setOE_pert(self, r, doedt, dt):
        self.h    = self.h      + doedt[0]*dt 
        self.ec   = self.ec     + doedt[1]*dt
        self.f    = self.f      + doedt[2]*dt
        self.RAAN = self.RAAN   + doedt[3]*dt
        self.incl = self.incl   + doedt[4]*dt
        self.ap   = self.ap     + doedt[5]*dt
        self.r    = r
        self.nm   = self.h/r**2 
        return 
    
    def setOE_pert_ini(self, doedt, dt):
        self.h    = self.h     + doedt[0]*dt 
        self.ec   = self.ec    + doedt[1]*dt
        self.f    = self.f     + doedt[2]*dt
        self.RAAN = self.RAAN  + doedt[3]*dt
        self.incl = self.incl  + doedt[4]*dt
        self.ap   = self.ap    + doedt[5]*dt
        return 

      
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
        
    
