
import numpy as np
from Library.math_sup.Quaternion import Quaternions
from Library.math_sup.RandomWalk import RandomWalk


class Gyro(object):
    def __init__(self, properties):
        self.current = properties['current']
        self.q_b2c = Quaternions(properties['q_b2c'])
        self.scalefactor = properties['ScaleFactor']
        self.bias_c = properties['Bias_c']
        self.n_rw_c = RandomWalk(properties['rw_stepwidth'], properties['rw_stddev_c'], properties['rw_limit_c'])
        self.range_to_const = properties['Range_to_const']
        self.range_to_zero = properties['Range_to_zero']
        self.current_omega_c = np.zeros(3)
        self.historical_omega_c = []

    def measure(self, omega_b):
        self.RangeCheck()

        # Convert angular velocity from body (b) coordinate system to sensor actual coordinate system (c)
        omega_c = self.q_b2c.frame_conv(omega_b)

        # Addition of scale factor
        omega_c = self.scalefactor.dot(omega_c)

        # Addition of bias
        omega_c += self.bias_c

        # Addition of random walk
        #omega_c += self.n_rw_c()

        # Adding gaussian noise
        #omega_c += self.nrs_c

        self.current_omega_c = omega_c

        self.clip()

    def RangeCheck(self):
        if self.range_to_const < 0.0 or self.range_to_zero < 0.0:
            print("Gyro: range should be positive!!")
        elif self.range_to_const > self.range_to_zero:
            print("Gyro: range2 should be greater than range1!!")
        return

    def clip(self):
        for i in range(self.current_omega_c.size):
            if self.range_to_const <= self.current_omega_c[i] < self.range_to_zero:
                self.current_omega_c[i] = self.range_to_const
            elif -self.range_to_const >= self.current_omega_c[i] > -self.range_to_zero:
                self.current_omega_c[i] = -self.range_to_const
            elif np.abs(self.current_omega_c[i]) >= self.range_to_zero:
                self.current_omega_c[i] = 0.0
        return

    def get_omega_c(self):
        return self.current_omega_c

    def get_historical_omega_c(self):
        return self.historical_omega_c

    def update(self, variables):
        self.measure(variables['omega'])
        self.historical_omega_c.append(self.current_omega_c)
        return

    def get_current(self):
        return self.current
