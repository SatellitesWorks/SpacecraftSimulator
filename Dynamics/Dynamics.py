
from .SpacecraftOrbit.MainOrbit import MainOrbit
from .SpacecraftAttitude.Attitude import Attitude
from .CelestialBody.Ephemeris import Ephemeris
import numpy as np


class Dynamics(object):
    def __init__(self, dynamics_properties, simtime):
        self.simtime = simtime
        attitude_properties  = {'Omega_b': dynamics_properties['Attitude']['Omega_b'],
                                'Quaternion_i2b': dynamics_properties['Attitude']['Quaternion_i2b'],
                                'Inertia': dynamics_properties['Attitude']['Inertia'],
                                'Mass': dynamics_properties['Attitude']['Mass'],
                                'attitudestep': self.simtime.attitudestep}
        orbit_properties = {'Orbit_info': dynamics_properties['Orbit']['Orbit_info'],
                            'propagate': dynamics_properties['Orbit']['propagate']}
        self.attitude  = Attitude(attitude_properties)
        self.ephemeris = Ephemeris(dynamics_properties['Ephemerides'])
        self.orbit     = MainOrbit(orbit_properties, self.simtime.orbitstep, self.ephemeris.selected_center_object)

    def update(self):
        self.attitude.update_attitude(self.simtime.maincountTime)
        if self.simtime.orbit_update_flag:
            self.orbit.update_orbit(self.simtime.current_jd)
            self.ephemeris.update(self.simtime.current_jd)
            self.orbit.TransECItoGeo(self.ephemeris.selected_center_object.get_current_sideral())
        self.orbit.update_attitte(self.attitude.get_class_q_i2b())

    def add_ext_force_b(self, force_b):
        self.orbit.add_ext_force_b(force_b, self.attitude.get_class_q_i2b(), self.attitude.mass)

    def add_int_force_b(self, force_b):
        self.orbit.add_int_force_b(force_b, self.attitude.get_class_q_i2b(), self.attitude.mass)

