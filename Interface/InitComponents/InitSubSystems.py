
from .InitComponents import InitComponents
import configparser


class InitSubSystems(object):
    def __init__(self, properties,  prop_step):
        self.system_name = ['CDH', 'ADCS', 'ODCS', 'POWER', 'COM', 'STR', 'PAYLOAD', 'TCS']
        self.file_components = properties['path_com']

        self.system_init = {}
        self.rewrite_init(properties)

        self.init_components = {}
        for sub_elem in self.system_name:
            print("-----------------------------")
            print('SubSystem: ', sub_elem)
            self.init_components[sub_elem] = InitComponents(self.system_init[sub_elem],  prop_step)

    def rewrite_init(self, properties):
        for subsys in self.system_name:
            self.system_init[subsys] = self.get_properties_for_subsystems(properties[subsys.lower() + '_setting'],
                                                                          subsys)

    def get_properties_for_subsystems(self, path, section):
        config = configparser.ConfigParser()
        config.read(path, encoding="utf8")

        properties_ = {'path_com': self.file_components,
                       'gyro_flag': config[section]['gyro'] == 'True',
                       'obc_flag': config[section]['obc'] == 'True',
                       'rw_flag': config[section]['rw'] == 'True',
                       'thruster_flag': config[section]['thruster'] == 'True',
                       'stt_flag': config[section]['stt'] == 'True',
                       'ss_flag': config[section]['ss'] == 'True',
                       'power_flag': config[section]['power'] == 'True'}
        return properties_
