from Components.ADCS.Gyro import Gyro
from Interface.InitComponents.InitComponents import InitCom


class Components(InitCom):
    def __init__(self, components_properties):
        InitCom.__init__(self, components_properties)
        self.components = []
        if self.gyro_properties is not None:
            self.gyro = Gyro(self.gyro_properties)
            self.components.append(self.gyro)
            print(' - Gyro')
        elif self.obc_properties is not None:
            g = 0
        elif self.rw_properties is not None:
            g = 0
        elif self.power_properties is not None:
            g = 0
        elif self.thruster_properties is not None:
            g = 0
        elif self.stt_properties is not None:
            g = 0
        elif self.ss_properties is not None:
            g = 0

    def update_components(self, variables):
        for com in self.components:
            com.update(variables)
        return
