
from Components.AOCS.Gyro import Gyro
from Components.AOCS.RWModel import RWModel


class Components(object):
    def __init__(self, data, dynamics, port_):
        self.data = data
        # general component
        self.obc     = None
        self.gyro    = None
        self.rwmodel = None
        self.thruster = None
        self.stt     = None
        self.ss      = None
        self.power   = None
        self.gps     = None

        self.components_list = []

        if data is not None:
            # For individual components
            if self.data.obc_properties is not None:
                g = 0
            else:
                del self.obc
                self.components_list.append(None)
            if self.data.gyro_properties is not None:
                self.gyro = Gyro(port_, self.data.gyro_properties, dynamics)
                self.components_list.append(self.gyro)
            else:
                del self.gyro
                self.components_list.append(None)
            if self.data.power_properties is not None:
                g = 0
            else:
                del self.power
                self.components_list.append(None)
            if self.data.rw_properties is not None:
                self.rwmodel = []
                for i in range(len(self.data.rw_properties)):
                    self.rwmodel.append(RWModel(self.data.rw_properties[i], dynamics))
                    self.components_list.append(self.rwmodel[i])
            else:
                del self.rwmodel
                self.components_list.append(None)
            if self.data.thruster_properties is not None:
                g = 0
            else:
                del self.thruster
                self.components_list.append(None)
            if self.data.stt_properties is not None:
                g = 0
            else:
                del self.stt
                self.components_list.append(None)
            if self.data.ss_properties is not None:
                g = 0
            else:
                del self.ss
                self.components_list.append(None)