
from .MagEnv import MagEnv


class Environment(MagEnv):
    def __init__(self, environment_properties):
        MagEnv.__init__(self, environment_properties['MAG'])

        self.env_mag_flag = environment_properties['MAG']['mag_calculation']
        self.env_srp_flag = environment_properties['SRP']['srp_calculation']
        self.env_atm_flag = environment_properties['ATM']['atm_calculation']

        print('\nEnvironment properties')
        print('------------------------------')
        print('Magnetic: ' + str(self.env_mag_flag))
        print('Solar radiation: ' + str(self.env_srp_flag))
        print('Atmosphere: ' + str(self.env_atm_flag))
        print('------------------------------')

    def update(self, decyear, dynamics):
        sideral  = dynamics.ephemeris.selected_center_object.current_sideral
        lat = dynamics.orbit.current_lat
        lon = dynamics.orbit.current_long
        alt = dynamics.orbit.current_alt
        q_i2b = dynamics.attitude.current_quaternion_i2b
        if self.env_mag_flag:
            self.calc_mag(decyear, sideral, lat, lon, alt, q_i2b)




