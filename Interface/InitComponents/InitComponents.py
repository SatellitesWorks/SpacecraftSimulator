

from .InitGyro import InitGyro


class InitCom(InitGyro):
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
        elif properties['obc_flag']:
            k = 0
        elif properties['power_flag']:
            k = 0
        elif properties['rw_flag']:
            k = 0
        elif properties['thruster_flag']:
            k = 0
        elif properties['stt_flag']:
            k = 0
        elif properties['ss_flag']:
            k = 0