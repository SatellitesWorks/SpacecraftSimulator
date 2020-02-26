from Components.ADCS.Gyro import Gyro
from Components.ADCS.RWModel import RWModel
from Interface.InitComponents.InitComponents import InitCom


class Components(InitCom):
    def __init__(self, components_properties):
        InitCom.__init__(self, components_properties)
        self.components = []

        if self.gyro_properties is not None:
            self.gyro = Gyro(self.gyro_properties)
            self.components.append(self.gyro)
        if self.obc_properties is not None:
            g = 0
        if self.rw_properties is not None:
            self.rwmodel = []
            for i in range(len(self.rw_properties)):
                self.rwmodel.append(RWModel(self.rw_properties[i]))
                self.components.append(self.rwmodel[i])
        if self.power_properties is not None:
            g = 0
        if self.thruster_properties is not None:
            g = 0
        if self.stt_properties is not None:
            g = 0
        if self.ss_properties is not None:
            g = 0

    def update_components(self, variables):
        for com in self.components:
            com.update(variables)
        return
