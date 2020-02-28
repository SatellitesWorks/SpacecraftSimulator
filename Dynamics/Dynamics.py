
from .SpacecraftOrbit.MainOrbit import MainOrbit
from .SpacecraftAttitude.Attitude import Attitude


class Dynamics(object):
    def __init__(self, dynamics_properties, simtime):
        self.simtime = simtime
        attitude_properties  = {'Omega_b': dynamics_properties['Attitude']['Omega_b'],
                                'Quaternion_i2b': dynamics_properties['Attitude']['Quaternion_i2b'],
                                'Inertia': dynamics_properties['Attitude']['Inertia'],
                                'attitudestep': self.simtime.attitudestep}
        orbit_properties = {'Orbit_info': dynamics_properties['Orbit']['Orbit_info'],
                            'propagate': dynamics_properties['Orbit']['propagate']}
        self.attitude = Attitude(attitude_properties)
        self.orbit = MainOrbit(orbit_properties)

    def update(self):
        self.orbit.update_orbit(self.simtime.get_array_time()[0])
        self.attitude.update_attitude(self.simtime.maincountTime)
        return
