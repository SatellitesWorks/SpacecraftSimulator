

import numpy as np

# quaternion = [i, j, k, 1]


class Quaternions(object):
    def __init__(self, quaterion_ini):
        self.q = np.array(quaterion_ini)

    def __call__(self, *args, **kwargs):
        return self.q

    def setquaternion(self, setvalue):
        self.q = setvalue

    def normalizeq(self):
        div = np.linalg.norm(self.q)
        self.q = self.q / div

    def conjugate(self):
        return np.array([-self.q[0],
                         -self.q[1],
                         -self.q[2],
                         self.q[3]])

    def frame_conv(self, v):
        dcm = self.todcm()
        ans = dcm.dot(v)
        return ans

    def todcm(self):
        q1 = self.q[0]
        q2 = self.q[1]
        q3 = self.q[2]
        q4 = self.q[3]

        dcm = [[q1 ** 2 - q2 ** 2 - q3 ** 2 + q4 ** 2, 2 * (q1 * q2 + q3 * q4), 2 * (q1 * q3 - q2 * q4)],
               [2 * (q1 * q2 - q3 * q4), -q1 ** 2 + q2 ** 2 - q3 ** 2 + q4 ** 2, 2 * (q2 * q3 + q1 * q4)],
               [2 * (q1 * q3 + q2 * q4), 2 * (q2 * q3 - q1 * q4), -q1 ** 2 - q2 ** 2 + q3 ** 2 + q4 ** 2]]
        return  np.array(dcm)

    def toeuler(self):
        """
        This function finds the angles of the classical Euler sequence
        R3(gamma)*R1(beta)*R3(alpha) from the direction cosine matrix.
        Q - direction cosine matrix
        alpha - first angle of the sequence (deg)
        beta - second angle of the sequence (deg)
        gamma - third angle of the sequence (deg)
        """
        Q = self.todcm()
        alpha = np.arctan2(Q[2, 0], -Q[2, 1])
        beta = np.arccos(Q[2, 2])
        gamma = np.arctan2(Q[0, 2], Q[1, 2])
        return alpha, beta, gamma

    def toypr(self):
        """
        This function finds the angles of the yaw-pitch-roll sequence
        R1(gamma)*R2(beta)*R3(alpha) from the direction cosine matrix.
        Q - direction cosine matrix
        yaw - yaw angle (deg)
        pitch - pitch angle (deg)
        roll - roll angle (deg)
        """
        Q = self.todcm()
        yaw = np.arctan2(Q[0, 1], Q[0, 0])
        pitch = np.arcsin(-Q[0, 2])
        roll = np.arctan2(Q[1, 2], Q[2, 2])
        return yaw, pitch, roll


if __name__ == '__main__':
    Q = Quaternions(np.array([-.6, 0, 0, 1]))
    Q.setquaternion(np.array([-.6, 0, 2, 1]))
    print(Q())