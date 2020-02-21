# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 03:58:00 2020

@author: EO
"""
import configparser
from Library.Pyorbital.pyorbital import tlefile
import numpy as np
from datetime import datetime


class InitialConfig(object):
    def __init__(self):
        self.tle_name = 'suchai'
        self.time_properties = TimeSim()
        self.spacecraft_properties = SatSim()
        self.orbit_properties = OrbitSim()
        self.environment_properties = EnvSim()
        return


def TimeSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/Spacecraft.ini", encoding="utf8")
    StartYMDHMS = config['TIME']['StartYMDHMS']
    if StartYMDHMS == ('Today' or 'TODAY' or 'today'):
        today = datetime.utcnow()
        StartYMDHMS = today.strftime("%Y/%m/%d %H:%M:%S")

    EndTimeSec = float(config['TIME']['EndTimeSec'])
    StepTimeSec = float(config['TIME']['StepTimeSec'])
    OrbitPropagateStepTimeSec = float(config['TIME']['OrbitPropagateStepTimeSec'])
    LogPeriod = float(config['TIME']['LogPeriod'])
    SimulationSpeed = float(config['TIME']['SimulationSpeed'])
    PropStepSec = float(config['ATTITUDE']['PropStepSec'])
    PropStepSec_Thermal = float(config['THERMAL']['PropStepSec_Thermal'])
    timesim = {'StartTime': StartYMDHMS,
               'EndTime': EndTimeSec,
               'StepTime': StepTimeSec,
               'OrbStepTime': OrbitPropagateStepTimeSec,
               'LogPeriod': LogPeriod,
               'SimulationSpeed': SimulationSpeed,
               'PropStepSec': PropStepSec,
               'PropStepSec_Thermal': PropStepSec_Thermal}
    return timesim


def tleSim(tle_name):
    tle = tlefile.read(tle_name, 'tle/'+tle_name+'.txt')
    return tle


def SatSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/Spacecraft.ini", encoding="utf8")
    #Rotational speed [rad/s]
    Omega_b = np.zeros(3)
    Omega_b[0] = config['ATTITUDE']['Omega_b(0)']
    Omega_b[1] = config['ATTITUDE']['Omega_b(1)']
    Omega_b[2] = config['ATTITUDE']['Omega_b(2)']
    # QuaternionCi2bC
    Quaternion_i2b = np.zeros(4)
    Quaternion_i2b[0] = config['ATTITUDE']['Quaternion_i2b(0)']
    Quaternion_i2b[1] = config['ATTITUDE']['Quaternion_i2b(1)']
    Quaternion_i2b[2] = config['ATTITUDE']['Quaternion_i2b(2)']
    Quaternion_i2b[3] = config['ATTITUDE']['Quaternion_i2b(3)']

    # Inertial
    Iner = np.zeros((3, 3))
    Iner[0, 0] = config['ATTITUDE']['Iner(0)']
    Iner[0, 1] = config['ATTITUDE']['Iner(1)']
    Iner[0, 2] = config['ATTITUDE']['Iner(2)']
    Iner[1, 0] = config['ATTITUDE']['Iner(3)']
    Iner[1, 1] = config['ATTITUDE']['Iner(4)']
    Iner[1, 2] = config['ATTITUDE']['Iner(5)']
    Iner[2, 0] = config['ATTITUDE']['Iner(6)']
    Iner[2, 1] = config['ATTITUDE']['Iner(7)']
    Iner[2, 2] = config['ATTITUDE']['Iner(8)']
    # mass
    mass = float(config['ATTITUDE']['mass'])
    satset = {'Omega_b': Omega_b,
              'Quaternion_i2b': Quaternion_i2b,
              'Inertia': Iner,
              'Mass': mass}
    return satset


def OrbitSim():
    config      = configparser.ConfigParser()
    config.read("Data/ini/Orbit.ini", encoding="utf8")
    # orbit
    orbit_tle = config['ORBIT']['orbit_tle']
    calculation = config['ORBIT']['calculation']
    logging     = config['ORBIT']['logging']
    propagate   = {}
    propagate_mode = float(config['PROPAGATION']['propagate_mode'])
    propagate['propagate_mode'] = propagate_mode
    if propagate_mode == 1:
        wgs = float(config['PROPAGATION']['wgs'])
        propagate['wgs'] = wgs
    if orbit_tle:
        tle_name = config['ORBIT']['tle_name']
        tle_info = tleSim(tle_name)

        orbitset = {'Orbit_info': [tle_info.line1, tle_info.line2],
                    'TLE': True,
                    'propagate': propagate,
                    'calculation': calculation,
                    'logging': logging}
    else:
        # position
        r = np.zeros((3, 1))
        r[0] = config['ORBIT']['rx']
        r[1] = config['ORBIT']['ry']
        r[2] = config['ORBIT']['rz']
        # velocity
        v = np.zeros((3, 1))
        v[0] = config['ORBIT']['vx']
        v[1] = config['ORBIT']['vy']
        v[2] = config['ORBIT']['vz']

        orbitset = {'Orbit_info': [r, v],
                    'TLE': False,
                    'propagate': propagate,
                    'calculation': calculation,
                    'logging': logging}
    return orbitset

def EnvSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/Environment.ini", encoding="utf8")

    return 0



