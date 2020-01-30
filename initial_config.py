# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 03:58:00 2020

@author: EO
"""
import configparser
from Library.Pyorbital.pyorbital import tlefile
import numpy as np
from datetime import datetime

def TimeSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/TimeSet.ini", encoding="utf8")
    StartYMDHMS                 = config['TIME']['StartYMDHMS']
    if StartYMDHMS == ('Today' or 'TODAY' or 'today'):
        today = datetime.utcnow()
        StartYMDHMS = today.strftime("%Y/%m/%d %H:%M:%S")
    EndTimeSec                  = float(config['TIME']['EndTimeSec'])
    StepTimeSec                 = float(config['TIME']['StepTimeSec'])
    OrbitPropagateStepTimeSec   = float(config['TIME']['OrbitPropagateStepTimeSec'])
    LogPeriod                   = float(config['TIME']['LogPeriod'])
    SimulationSpeed             = float(config['TIME']['SimulationSpeed'])
    PropStepSec = float(config['ATTITUDE']['PropStepSec'])
    timesim = {'StartTime'      : StartYMDHMS,
               'EndTime'        : EndTimeSec,
               'StepTime'       : StepTimeSec,
               'OrbStepTime'    : OrbitPropagateStepTimeSec,
               'LogPeriod'      : LogPeriod,
               'SimulationSpeed': SimulationSpeed,
               'PropStepSec'    : PropStepSec}
    return timesim

def tleSim(tle_name):
    tle = tlefile.read(tle_name, 'tle/'+tle_name+'.txt')
    return tle

def SatSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/SatelliteSet.ini", encoding="utf8")
    #Rotational speed [rad/s]
    Omega_b = np.zeros((3, 1))
    Omega_b[0] = config['ATTITUDE']['Omega_b(0)']
    Omega_b[1] = config['ATTITUDE']['Omega_b(1)']
    Omega_b[2] = config['ATTITUDE']['Omega_b(2)']
    # QuaternionCi2bC
    Quaternion_i2b = np.zeros((4, 1))
    Quaternion_i2b[0] = config['ATTITUDE']['Quaternion_i2b(0)']
    Quaternion_i2b[1] = config['ATTITUDE']['Quaternion_i2b(1)']
    Quaternion_i2b[2] = config['ATTITUDE']['Quaternion_i2b(2)']
    Quaternion_i2b[3] = config['ATTITUDE']['Quaternion_i2b(3)']

    # Inertial
    Iner = np.zeros((3, 3))
    Iner[0, 0] = config['PHYSICAL']['Iner(0)']
    Iner[0, 1] = config['PHYSICAL']['Iner(1)']
    Iner[0, 2] = config['PHYSICAL']['Iner(2)']
    Iner[1, 0] = config['PHYSICAL']['Iner(3)']
    Iner[1, 1] = config['PHYSICAL']['Iner(4)']
    Iner[1, 2] = config['PHYSICAL']['Iner(5)']
    Iner[2, 0] = config['PHYSICAL']['Iner(6)']
    Iner[2, 1] = config['PHYSICAL']['Iner(7)']
    Iner[2, 2] = config['PHYSICAL']['Iner(8)']
    # mass
    mass = float(config['PHYSICAL']['mass'])

    # orbit
    orbit_tle = config['ORBIT']['orbit_tle']

    if orbit_tle:
        tle_name = config['ORBIT']['tle_name']
        tle_info = tleSim(tle_name)

        satset = {'Omega_b': Omega_b,
                  'Quaternion_i2b': Quaternion_i2b,
                  'Inertia': Iner,
                  'Mass': mass,
                  'Orbit_info': [tle_info.line1, tle_info.line2],
                  'TLE': True}
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
        satset = {'Omega_b': Omega_b,
                  'Quaternion_i2b': Quaternion_i2b,
                  'Inertia': Iner,
                  'Mass': mass,
                  'Orbit_info': [r, v],
                  'TLE': False}
    return satset

def OrbitSim():
    config      = configparser.ConfigParser()
    config.read("Data/ini/OrbitSet.ini", encoding="utf8")
    calculation = config['ORBIT']['calculation']
    logging     = config['ORBIT']['logging']
    propagate   = {}
    propagate_mode = float(config['PROPAGATION']['propagate_mode'])
    propagate['propagate_mode'] = propagate_mode
    if propagate_mode == 1:
        wgs = float(config['PROPAGATION']['wgs'])
        propagate['wgs'] = wgs
    return propagate, calculation, logging

def initial_config():
    timeset = TimeSim()
    dynamics_satset  = SatSim()
    propset = OrbitSim()

    return timeset, dynamics_satset, propset, 0

