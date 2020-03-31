from .ComponentBase import ComponentBase
from Spacecraft.Components import Components
from Library.math_sup.Quaternion import Quaternions
from ..Logic.Control.Controller import Controller
import numpy as np

REF_POINT = 2
NAD_POINT = 1
DETUMBLING = 0


class ADCS(ComponentBase):
    def __init__(self, init_componenets, subsystem_setting, dynamics):
        # prescalar_time in [ms]
        ComponentBase.__init__(self, prescalar_time=(1000 / subsystem_setting['ADCS_com_frequency']))
        # component quaternion
        self.q_b2c = subsystem_setting['q_b2c']
        # cycle in [ms]
        self.ctrl_cycle = 1000 / subsystem_setting['ADCS_com_frequency']
        self.port_id = subsystem_setting['port_id']
        self.comp_number = subsystem_setting['ADCS_COMPONENT_NUMBER']
        self.dynamics = dynamics
        self.components = Components(init_componenets, self.dynamics, self.port_id)
        self.current_omega_c_gyro = np.zeros(3)
        self.torque_rw_b = np.zeros(3)
        self.omega_b_est = np.zeros(3)
        self.control_torque = np.zeros(3)
        self.historical_control = []
        self.P_omega = subsystem_setting['P_omega']
        self.I_quat = subsystem_setting['I_quat']
        self.P_quat = subsystem_setting['P_quat']
        self.rw_torque_b = np.zeros(3)
        self.q_i2b_est = Quaternions([0, 0, 0, 1])
        self.q_b2b_now2tar = Quaternions([0, 0, 0, 1])
        self.q_i2b_tar = Quaternions([0, 0, 0, 1])

        self.adcs_mode = DETUMBLING
        for rw in self.components.rwmodel:
            rw.set_step_width(self.ctrl_cycle / 1000)
        self.controller = Controller().pid(self.P_quat, self.I_quat, self.P_omega, self.ctrl_cycle/1000)

    def main_routine(self, count):
        self.read_sensors()

        self.check_mode()

        self.determine_attitude()

        self.calculate_control_torque()

        self.calc_rw_torque()
        return

    def read_sensors(self):
        self.current_omega_c_gyro = self.components.gyro.measure(self.dynamics.attitude.current_omega_b)

    def determine_attitude(self):
        self.omega_b_est = self.current_omega_c_gyro
        att = self.dynamics.attitude.get_current_q_i2b()
        self.q_i2b_est.setquaternion(att)
        return

    def check_mode(self):
        if self.adcs_mode == DETUMBLING:
            self.omega_b_tar = np.array([0.0, 0.0, 0.0])
            self.controller.set_gain(self.P_omega, self.I_quat, np.diag([0.0, 0.0, 0.0]))
        elif self.adcs_mode == NAD_POINT:
            print('Nadir pointing mode...')
        elif self.adcs_mode == REF_POINT:
            # Vector direction of the Body frame to point to another vector
            b_dir = np.array([0, 0, 1])

            # Vector target from Inertial frame
            i_tar = np.array([1, 1, 1])
            i_tar = i_tar / np.linalg.norm(i_tar)

            # Vector target from body frame
            b_tar = self.q_i2b_est.frame_conv(i_tar)
            b_tar /= np.linalg.norm(b_tar)

            b_lambda = np.cross(b_dir, b_tar)
            b_lambda /= np.linalg.norm(b_lambda)

            rot = np.arccos(np.dot(b_dir, b_tar))

            self.q_b2b_now2tar.setquaternion([b_lambda, rot])
            self.q_b2b_now2tar.normalize()
            self.q_i2b_tar = self.q_i2b_est * self.q_b2b_now2tar
        else:
            print('No mode selected')

    def calculate_control_torque(self):
        q_b2i_est = Quaternions(self.q_i2b_est.conjugate())
        # First it is necessary to pass the quaternion from attitude to inertial,
        # then the target vector is rotated from the inertial to body frame
        q_i2b_now2tar = q_b2i_est * self.q_i2b_tar
        q_i2b_now2tar.normalize()

        torque_direction = np.zeros(3)
        torque_direction[0] = q_i2b_now2tar()[0]
        torque_direction[1] = q_i2b_now2tar()[1]
        torque_direction[2] = q_i2b_now2tar()[2]

        angle_rotation = 2 * np.arccos(q_i2b_now2tar()[3])

        error_omega_ = self.omega_b_tar - self.omega_b_est
        error_ = angle_rotation * torque_direction
        control = self.controller.calc_control(error_, error_omega_, self.adcs_mode)
        self.control_torque = control

    def calc_rw_torque(self):
        f = 0
        for rw in self.components.rwmodel:
            rw.control_power()
            rw.set_torque(self.control_torque[f], self.ctrl_cycle)
            self.rw_torque_b += rw.calc_torque(self.ctrl_cycle)
            f += 1
        return

    def get_rwtorque(self):
        return self.rw_torque_b

    def save_data(self):
        self.historical_control.append(self.control_torque)

    def get_log_values(self, subsys):
        report = {'RWModel_' + subsys + '_b(X)[Nm]': 0,
                  'RWModel_' + subsys + '_b(Y)[Nm]': 0,
                  'RWModel_' + subsys + '_b(Z)[Nm]': 0}
        if hasattr(self.components, 'gyro'):
            gyro = self.components.gyro
            report['gyro_omega_' + subsys + '_c(X)[rad/s]'] = np.array(gyro.historical_omega_c)[:, 0]
            report['gyro_omega_' + subsys + '_c(Y)[rad/s]'] = np.array(gyro.historical_omega_c)[:, 1]
            report['gyro_omega_' + subsys + '_c(Z)[rad/s]'] = np.array(gyro.historical_omega_c)[:, 2]
        if hasattr(self.components, 'rwmodel'):
            for rw in self.components.rwmodel:
                report['RWModel_' + subsys + '_b(X)[Nm]'] += np.array(rw.historical_rw_torque_b)[:, 0]
                report['RWModel_' + subsys + '_b(Y)[Nm]'] += np.array(rw.historical_rw_torque_b)[:, 1]
                report['RWModel_' + subsys + '_b(Z)[Nm]'] += np.array(rw.historical_rw_torque_b)[:, 2]
        report_control = {'Control_(X)[Nm]': np.array(self.historical_control)[:, 0],
                          'Control_(Y)[Nm]': np.array(self.historical_control)[:, 1],
                          'Control_(Z)[Nm]': np.array(self.historical_control)[:, 2]}
        report = {**report, **report_control}
        return report
