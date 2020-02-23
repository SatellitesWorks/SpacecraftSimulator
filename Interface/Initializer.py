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
        self.time_properties = TimeSim()
        self.spacecraft_properties, self.components_properties = SatSim()
        self.orbit_properties = OrbitSim()
        self.environment_properties = EnvSim()
        self.disturbance_properties = DistSim()
        self.logger_properties = self.LogSim()

    def LogSim(self):
        properties = {'orb_log': self.orbit_properties['logging'],
                      'env_mag_log': self.environment_properties['MAG']['mag_logging'],
                      'env_atm_log': self.environment_properties['ATM']['atm_logging'],
                      'env_srp_log': self.environment_properties['SRP']['srp_logging'],
                      'dis_mag_log': self.disturbance_properties['MAG']['mag_logging'],
                      'dis_gra_log': self.disturbance_properties['GRA']['gra_logging']}
        return properties


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
    tle = tlefile.read(tle_name, 'tle/' + tle_name + '.txt')
    return tle


def SatSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/Spacecraft.ini", encoding="utf8")
    spacecraft_name = config['NAME']['spacecraft_name']

    # Rotational speed [rad/s]
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
              'Mass': mass,
              'spacecraft_name': spacecraft_name}

    file_components = config['COMPONENTS']['file_components']
    comset = {'path_com': file_components,
              'gyro_flag': config['COMPONENTS']['gyro'],
              'obc_flag': config['COMPONENTS']['obc'],
              'power_flag': config['COMPONENTS']['power'],
              'rw_flag': config['COMPONENTS']['rw'],
              'thruster_flag': config['COMPONENTS']['thruster'],
              'stt_flag': config['COMPONENTS']['stt'],
              'ss_flag': config['COMPONENTS']['ss']}

    return satset, comset


def OrbitSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/Orbit.ini", encoding="utf8")
    # orbit
    orbit_tle = config['ORBIT']['orbit_tle']
    calculation = config['ORBIT']['calculation']
    logging = config['ORBIT']['logging']
    propagate = {}
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
    mag_calculation = config['MAG_ENVIRONMENT']['calculation']
    mag_logging = config['MAG_ENVIRONMENT']['logging']
    mag_rwdev = float(config['MAG_ENVIRONMENT']['mag_rwdev'])
    mag_rwlimit = float(config['MAG_ENVIRONMENT']['mag_rwlimit'])
    mag_wnvar = float(config['MAG_ENVIRONMENT']['mag_wnvar'])

    srp_calculation = config['SRP']['calculation']
    srp_logging = config['SRP']['logging']

    atm_calculation = config['ATMOSPHERE']['calculation']
    atm_logging = config['ATMOSPHERE']['logging']
    mag_properties = {'mag_calculation': mag_calculation,
                      'mag_logging': mag_logging,
                      'mag_rwdev': mag_rwdev,
                      'mag_rwlimit': mag_rwlimit,
                      'mag_wnvar': mag_wnvar}
    srp_properties = {'srp_calculation': srp_calculation,
                      'srp_logging': srp_logging}
    atm_properties = {'atm_calculation': atm_calculation,
                      'atm_logging': atm_logging}
    environment_properties = {'MAG': mag_properties,
                              'SRP': srp_properties,
                              'ATM': atm_properties}
    return environment_properties


def DistSim():
    config = configparser.ConfigParser()
    config.read("Data/ini/Disturbance.ini", encoding="utf8")
    grav_properties = {'gra_calculation': config['GRAVITY_GRADIENT']['calculation'],
                       'gra_logging': config['GRAVITY_GRADIENT']['logging']}
    rmm_const_b = np.zeros(3)
    rmm_const_b[0] = config['MAG_DISTURBANCE']['rmm_const_b(0)']
    rmm_const_b[1] = config['MAG_DISTURBANCE']['rmm_const_b(1)']
    rmm_const_b[2] = config['MAG_DISTURBANCE']['rmm_const_b(2)']
    mag_properties = {'mag_calculation': config['MAG_DISTURBANCE']['calculation'],
                      'mag_logging': config['MAG_DISTURBANCE']['logging'],
                      'mag_rmm_const_b': rmm_const_b,
                      'mag_rmm_rwdev': float(config['MAG_DISTURBANCE']['rmm_rwdev']),
                      'mag_rmm_rwlimit': float(config['MAG_DISTURBANCE']['rmm_rwlimit']),
                      'mag_rmm_wnvar': float(config['MAG_DISTURBANCE']['rmm_wnvar'])}

    position_vector_surface = np.zeros((6, 3))
    position_vector_surface[0] = [config['SURFACEFORCE']['px_arm(0)'],
                                  config['SURFACEFORCE']['px_arm(1)'],
                                  config['SURFACEFORCE']['px_arm(2)']]
    position_vector_surface[1] = [config['SURFACEFORCE']['mx_arm(0)'],
                                  config['SURFACEFORCE']['mx_arm(1)'],
                                  config['SURFACEFORCE']['mx_arm(2)']]
    position_vector_surface[2] = [config['SURFACEFORCE']['py_arm(0)'],
                                  config['SURFACEFORCE']['py_arm(1)'],
                                  config['SURFACEFORCE']['py_arm(2)']]
    position_vector_surface[3] = [config['SURFACEFORCE']['my_arm(0)'],
                                  config['SURFACEFORCE']['my_arm(1)'],
                                  config['SURFACEFORCE']['my_arm(2)']]
    position_vector_surface[4] = [config['SURFACEFORCE']['pz_arm(0)'],
                                  config['SURFACEFORCE']['pz_arm(1)'],
                                  config['SURFACEFORCE']['pz_arm(2)']]
    position_vector_surface[5] = [config['SURFACEFORCE']['mz_arm(0)'],
                                  config['SURFACEFORCE']['mz_arm(1)'],
                                  config['SURFACEFORCE']['mz_arm(2)']]
    sff_area = np.zeros(6)
    sff_area[:] = [config['SURFACEFORCE']['area(0)'],
                   config['SURFACEFORCE']['area(1)'],
                   config['SURFACEFORCE']['area(2)'],
                   config['SURFACEFORCE']['area(3)'],
                   config['SURFACEFORCE']['area(4)'],
                   config['SURFACEFORCE']['area(5)']]

    sff_vector = np.zeros((6, 3))
    sff_vector[0] = [config['SURFACEFORCE']['px_normal(0)'],
                     config['SURFACEFORCE']['px_normal(1)'],
                     config['SURFACEFORCE']['px_normal(2)']]
    sff_vector[1] = [config['SURFACEFORCE']['mx_normal(0)'],
                     config['SURFACEFORCE']['mx_normal(1)'],
                     config['SURFACEFORCE']['mx_normal(2)']]
    sff_vector[2] = [config['SURFACEFORCE']['py_normal(0)'],
                     config['SURFACEFORCE']['py_normal(1)'],
                     config['SURFACEFORCE']['py_normal(2)']]
    sff_vector[3] = [config['SURFACEFORCE']['my_normal(0)'],
                     config['SURFACEFORCE']['my_normal(1)'],
                     config['SURFACEFORCE']['my_normal(2)']]
    sff_vector[4] = [config['SURFACEFORCE']['pz_normal(0)'],
                     config['SURFACEFORCE']['pz_normal(1)'],
                     config['SURFACEFORCE']['pz_normal(2)']]
    sff_vector[5] = [config['SURFACEFORCE']['mz_normal(0)'],
                     config['SURFACEFORCE']['mz_normal(1)'],
                     config['SURFACEFORCE']['mz_normal(2)']]

    sff_center = np.array([config['SURFACEFORCE']['center(0)'],
                           config['SURFACEFORCE']['center(1)'],
                           config['SURFACEFORCE']['center(2)']])

    sff_properties = {'sff_position': position_vector_surface,
                      'sff_area': sff_area,
                      'sff_vector': sff_vector,
                      'sff_center': sff_center}

    disturbance_properties = {'GRA': grav_properties,
                              'MAG': mag_properties,
                              'SFF': sff_properties}
    return disturbance_properties
