
"""
Created by:

@author: Elias Obreque
els.obrq@gmail.com

ref to force and torque definition:
 - Dynamics of Atmospheric Re-entry AIAA, chapter 11, eq. (11.24)
 - Gauss error function
"""
from scipy.special import erf
import numpy as np
from .SurfaceForce import SurfaceForce
c2K = 273.15


class AirDrag(SurfaceForce):
    def __init__(self, drag_properties, surface_properties):
        SurfaceForce.__init__(self, surface_properties)
        self.dist_flag = drag_properties['atm_calculation']
        self.module_wall_temperature = drag_properties['Temp_wall'] + c2K
        self.specularity = drag_properties['specularity']
        self.MM = drag_properties['Molecular']
        self.temp_molecular = drag_properties['Temp_molecular']
        self.reflectivity = np.ones(6)
        self.Cp = 0.1
        self.Ct = 0.1
        self.char_dimension = 0.1
        self.sigma_n = 1 - self.specularity
        self.sigma_t = self.sigma_n
        self.boltzmann = 1.3806488e-23  # J/K
        self.force_b = np.zeros(3)
        self.torque_b = np.zeros(3)

    def update(self, environment, spacecraft):
        density = environment.atm.current_density
        velocity_b = spacecraft.dynamics.orbit.get_velocity_b()
        #velocity_b = np.array([-1, 5, -5])
        velocity_b_norm = np.linalg.norm(velocity_b)
        q_inf = 0.5 * density * velocity_b_norm ** 2
        unit_velocity_b = velocity_b / velocity_b_norm
        self.calc_ang_parameters(unit_velocity_b)
        self.calc_aerodynamics_coeff(environment, velocity_b_norm)
        self.calc_force_torque_vector_b(unit_velocity_b, self.Cp, self.Ct)
        self.force_b = self.force_vector_b * q_inf
        self.torque_b = self.torque_vector_b * q_inf

    def get_torque_b(self):
        return self.torque_b

    def get_force_b(self):
        return self.force_b

    def calc_aerodynamics_coeff(self, envir, v_b):
        s = np.sqrt((self.MM * v_b) / (2 * self.boltzmann * self.module_wall_temperature))
        ss = s ** 2
        s_stheta = s * self.sen_theta[self.condition_]
        s_ctheta = s * self.cos_theta[self.condition_]
        s2sn = 2 - self.sigma_n[self.condition_]
        sntw_tinf = 0.5 * self.sigma_n[self.condition_] * (self.module_wall_temperature /
                                                           self.temp_molecular) ** 0.5
        erf_s_theta = 1 + erf(s_stheta)
        sqrt_pi = np.sqrt(np.pi)
        s_stheta2 = s_stheta ** 2
        exp_s_s = np.exp(- s_stheta2)
        gt_sc_pi = self.sigma_t[self.condition_] * s_ctheta / sqrt_pi
        deltaP_q_inf_s2 = [s2sn * s_stheta / sqrt_pi + sntw_tinf] * exp_s_s + \
                          [s2sn * (0.5 + s_stheta2) + sntw_tinf * sqrt_pi * s_stheta] * erf_s_theta
        deltaT_q_inf_s2 = gt_sc_pi * (exp_s_s + sqrt_pi * s_stheta * erf_s_theta)
        self.Cp = deltaP_q_inf_s2 / ss
        self.Ct = deltaT_q_inf_s2 / ss
