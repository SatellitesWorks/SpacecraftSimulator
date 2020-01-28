from pyvista import examples
import numpy as np
import pyvista as pv


class GeoDef(object):
    def __init__(self, vtk_widget):
        self.vtk_widget = vtk_widget

    #def add_sphere(self):
        # add a sphere to the pyqt frame
        self.vtk_widget.subplot(0, 0)
        sphere      = examples.load_globe()
        sphere.points /= 1000000
        self.sphere = sphere
        self.vtk_widget.add_mesh(self.sphere)
        self.sphere.rotate_z(self.earth_gst[0])
        self.vtk_widget.view_isometric()
        #self.vtk_widget.reset_camera()

    def add_orbit(self):
        self.vtk_widget.subplot(0, 0)
        self.vtk_widget.add_text('Satellite position', font_size=10)
        self.vtk_widget.add_points(self.sat_dynamics['Orbital']['Position'], point_size=0.8)

    def add_spacecraft_2_orbit(self):
        self.vtk_widget.subplot(0, 0)
        self.spacecraft_in_orbit = pv.PolyData('./Spacecraft/Model/PlantSat/PlantSat.stl')
        self.spacecraft_in_orbit.translate(np.array([0, 0, -34.05 / 2]))
        self.spacecraft_in_orbit.points *= 15.0
        self.vtk_widget.add_mesh(self.spacecraft_in_orbit)
        self.spacecraft_in_orbit.translate(self.current_pos)

    def add_spacecraft_2_attitude(self):
        self.vtk_widget.subplot(0, 1)
        self.spacecraft_in_attitude = pv.PolyData('./Spacecraft/Model/PlantSat/PlantSat.stl')
        self.vtk_widget.add_mesh(self.spacecraft_in_attitude)
        self.spacecraft_in_attitude.translate(np.array([0, 0, -34.05/2]))

    def add_i_frame_attitude(self):
        center_ref = np.array([[0.0, 0.0, 0.0]])
        self.vtk_widget.subplot(0, 1)
        self.vtk_widget.add_arrows(cent=center_ref, direction=np.array([0, 0, 1]), mag=30, color='blue')
        self.vtk_widget.add_arrows(cent=center_ref, direction=np.array([0, 1, 0]), mag=30, color='green')
        self.vtk_widget.add_arrows(cent=center_ref, direction=np.array([1, 0, 0]), mag=30, color='red')

    def add_bar(self):
        self.vtk_widget.subplot(0, 0)
        self.vtk_widget.add_slider_widget(self.sim_speed, [0.5, 100], value = 1, title='Simulation speed')

