
import pandas as pd
import pyvista as pv
import numpy as np
#from pyquaternion import Quaternion

class AttSimViz():
    file_path = ""
    sim_data = None

    def __init__(self):
        return

    def read_data(self, file_path='200117_030840_default.csv'):
        df = pd.read_csv(file_path, delimiter=',')
        self.sim_data = df

    def plot_orbit(self):
        nsamples = 100
        sat_pos = self.sim_data[['sat_position_i(X)[m]', 'sat_position_i(Y)[m]', 'sat_position_i(Z)[m]']].values[0: nsamples, :]
        sat_vel = self.sim_data[['sat_velocity_i(X)[m/s]', 'sat_velocity_i(Y)[m/s]', 'sat_velocity_i(Z)[m/s]']].values[0: nsamples, :]
        sat_quat_val = self.sim_data[['q_t_i2b(0)[-]', 'q_t_i2b(1)[-]', 'q_t_i2b(2)[-]', 'q_t_i2b(3)[-]']].values[0: nsamples, :]
        #sat_quat = [Quaternion(q) for q in sat_quat_val]

        ref_axis = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
        #ref_arrow = np.array([[quat.rotate(axis) for axis in ref_axis] for quat in sat_quat]).reshape((-1, 3))
        # ref_arrow = np.array(ref_axis*nsamples).reshape((-1, 3))
        ref_arrow_pos = np.array([list(pos)*3 for pos in sat_pos]).reshape((-1, 3))
        #ref_arrow_mag = [300]*ref_arrow.shape[0]

        sat_vel_mag = [0.1]*sat_vel.shape[0]

        earth_pos = [[0.0, 0.0, 0.0]]

        plotter = pv.Plotter()
        # plotter.add_points(np.append(sat_pos, earth_pos, axis=0))
        plotter.add_points(sat_pos, point_size=10.0)
        # plotter.add_arrows(sat_pos, sat_vel, mag=sat_vel_mag)
        #plotter.add_arrows(ref_arrow_pos, ref_arrow, mag=ref_arrow_mag)
        plotter.show()
        print(sat_pos)


if  __name__ == '__main__':
    sim_viz = AttSimViz()
    sim_viz.read_data()
    sim_viz.plot_orbit()