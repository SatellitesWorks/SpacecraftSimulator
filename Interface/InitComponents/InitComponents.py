

from .InitGyro import InitGyro
from .InitRWModel import InitRWModel


class InitCom(InitGyro, InitRWModel):
    def __init__(self, properties):
        self.gyro_properties    = None
        self.obc_properties     = None
        self.rw_properties      = None
        self.power_properties   = None
        self.thruster_properties= None
        self.stt_properties     = None
        self.ss_properties      = None

        self.path_com = properties['path_com']
        if properties['gyro_flag']:
            InitGyro.__init__(self, self.path_com)
        if properties['obc_flag']:
            k = 0
        if properties['power_flag']:
            k = 0
        if properties['rw_flag']:
            InitRWModel.__init__(self, self.path_com)
        if properties['thruster_flag']:
            k = 0
        if properties['stt_flag']:
            k = 0
        if properties['ss_flag']:
            k = 0