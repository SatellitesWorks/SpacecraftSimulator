# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 10:33:47 2020

@author: EO
"""
import sys

from PyQt5 import Qt
from threading import Thread
import numpy as np

import pyvista as pv
import time
from pyvista import examples

class MainWindow(Qt.QMainWindow):

    def __init__(self, parent=None, show=True):
        Qt.QMainWindow.__init__(self, parent)

        # create the frame
        self.frame = Qt.QFrame()
        vlayout = Qt.QVBoxLayout()

        # add the pyvista interactor object
        self.vtk_widget = pv.QtInteractor(self.frame)
        vlayout.addWidget(self.vtk_widget)

        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        # simple menu to demo functions
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('File')
        exitButton = Qt.QAction('Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        #self.add_sphere()
        #self.rotate_sphere()
        self.add_spacecraft()

        # allow adding a sphere
        # meshMenu = mainMenu.addMenu('Mesh')
        # self.add_sphere_action = Qt.QAction('Add Sphere', self)
        # self.rotate_sphere_action = Qt.QAction('Rotate Sphere', self)
        # self.add_sphere_action.triggered.connect(self.add_sphere)
        # self.rotate_sphere_action.triggered.connect(self.rotate_sphere)
        # meshMenu.addAction(self.add_sphere_action)
        # meshMenu.addAction(self.rotate_sphere_action)

        if show:
            self.show()

    def add_sphere(self):
        """ add a sphere to the pyqt frame """
        sphere = examples.load_globe()
        self.sphere = sphere
        self.vtk_widget.add_mesh(sphere)
        self.vtk_widget.reset_camera()

    def rotate_th(self):
        for i in range(1000):
            self.sphere.rotate_z(10)
            self.vtk_widget.update()
            print('rotating {} degree'.format( 30))
            time.sleep(0.5)

    def rotate_sphere(self):
        thread = Thread(target=self.rotate_th)
        thread.start()

    def add_spacecraft(self):
        self.spacecraft_cad = pv.PolyData('./Spacecraft/Model/PlantSat/PlantSat.stl')
        self.vtk_widget.add_mesh(self.spacecraft_cad)
        self.spacecraft_cad.center_of_mass(4.2)

        self.spacecraft_cad.translate(np.array([0, 0, -34.05/2]))
        ref_axis = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        center_ref = np.array([[0.0, 0.0, 0.0]])
        self.vtk_widget.add_arrows(cent=center_ref, direction=np.array([0, 0, 1]), mag=30, color = 'blue')
        self.vtk_widget.add_arrows(cent=center_ref, direction=np.array([0, 1, 0]), mag=30, color = 'green')
        self.vtk_widget.add_arrows(cent=center_ref, direction=np.array([1, 0, 0]), mag=30, color = 'red')

if __name__ == '__main__':
    app = Qt.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())