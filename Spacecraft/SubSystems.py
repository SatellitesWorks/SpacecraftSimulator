
from Interface.InitComponents.InitSubSystems import InitSubSystems
from .Components import Components
import numpy as np


class SubSystems(InitSubSystems):
    def __init__(self, components_properties, dynamics):
        InitSubSystems.__init__(self, components_properties)

        self.components = {}
        number_i = 1
        for sub_elem in self.system_name:
            self.components[sub_elem] = Components(self.init_components[sub_elem], dynamics, number_i)
            number_i += 1

    def generate_torque_b(self):
        torque_b = np.zeros(3)
        if self.components['ADCS'].rwmodel is not None:
            for rw in self.components['ADCS'].rwmodel:
                torque_b += rw.get_torque()
        return torque_b

    def update(self):
        for sub_elem in self.system_name:
            for comp in self.components[sub_elem].components_list:
                if comp is not None:
                    comp.log_value()