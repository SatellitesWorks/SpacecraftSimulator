
from .InitGyro import InitGyro
from .InitRWModel import InitRWModel


class InitComponents(object):
    def __init__(self, properties,  prop_step):

        init_gyro = None
        init_obc = None
        init_power= None
        init_rw = None
        init_thruster = None
        init_stt = None
        init_ss = None

        components_init = {'gyro_flag': init_gyro,
                           'obc_flag': init_obc,
                           'power_flag': init_power,
                           'rw_flag': init_rw,
                           'thruster_flag': init_thruster,
                           'stt_flag': init_stt,
                           'ss_flag': init_ss}

        self.gyro_properties    = None
        self.obc_properties     = None
        self.rw_properties      = None
        self.power_properties   = None
        self.thruster_properties= None
        self.stt_properties     = None
        self.ss_properties      = None
        self.gps_properties     = None
        self.temperature_properties = None
        self.thermal_actuator_properties = None
        self.camera_properties = None
        self.antenna_properties = None

        path = properties['path_com']

        if properties['gyro_flag']:
            self.gyro_properties = InitGyro(path).gyro_properties
        if properties['obc_flag']:
            k = 0
        if properties['power_flag']:
            k = 0
        if properties['rw_flag']:
            self.rw_properties = InitRWModel(path,  prop_step).rw_properties
        if properties['thruster_flag']:
            k = 0
        if properties['stt_flag']:
            k = 0
        if properties['ss_flag']:
            k = 0
