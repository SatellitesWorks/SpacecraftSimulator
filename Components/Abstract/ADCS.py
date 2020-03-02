
from .ComponentBase import ComponentBase
from Spacecraft.Components import Components
import numpy as np


class ADCS(ComponentBase):
    def __init__(self, init_componenets, dynamics):
        ComponentBase.__init__(self, 5)
        self.dynamics = dynamics
        self.components = Components(init_componenets, self.dynamics, 2)
        self.current_omega_c_gyro = np.zeros(3)
        self.torque_rw_b = np.zeros(3)

    def main_routine(self, count):

        self.read_sensors()

        self.determine_attitude()

        self.check_mode()

        self.calculate_control_torque()

        self.calc_rw_torque()
        return

    def read_sensors(self):
        self.current_omega_c_gyro = self.components.gyro.measure(self.dynamics.attitude.current_omega_b)

    def determine_attitude(self):
        return

    def check_mode(self):
        return

    def calculate_control_torque(self):
        return

    def calc_rw_torque(self):
        return

    def get_torque(self):
        return self.torque_rw_b
