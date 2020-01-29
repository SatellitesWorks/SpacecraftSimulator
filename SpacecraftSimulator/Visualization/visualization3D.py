# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 02:47:18 2020

@author: EO
"""
import sys
from PyQt5 import Qt
from threading import Thread
import time
import numpy as np
import pyvista as pv
from .geometry_definition import GeoDef
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pandas as pd
from .visualization2D import MainGraph

class Main3D(GeoDef, Qt.QMainWindow):

    def __init__(self, dataLog = None, parent=None, show=True):
        self.dataLog = dataLog
        try:
            self.simtime        = dataLog[0]
            self.sat_dynamics   = dataLog[1]
            self.earth_gst      = dataLog[2]
            self.current_pos = self.sat_dynamics['Orbital']['Position'][0, :]
        except:
            print('No datalog, please load some file')

        self.time_speed     = 1
        self.earth_av       = 7.2921150*360.0*1e-5/(2*np.pi)
        self.run_flag       = False
        self.pause_flag     = False
        self.stop_flag      = False
        self.thread         = None
        Qt.QMainWindow.__init__(self, parent)
        # create the frame
        self.frame = Qt.QFrame()
        vlayout = Qt.QVBoxLayout()

        # add the pyvista interactor object
        self.vtk_widget = pv.QtInteractor(self.frame, shape=(1, 2))
        self.vtk_widget.set_background([0.25, 0.25, 0.25])
        self.vtk_widget.setFixedWidth(1000)
        self.vtk_widget.setFixedHeight(500)
        vlayout.addWidget(self.vtk_widget)
        GeoDef.__init__(self, self.vtk_widget)

        self.frame.setLayout(vlayout)
        self.setCentralWidget(self.frame)

        #self.add_sphere()
        self.add_bar()
        self.add_i_frame_attitude()

        #--------------------------------------------------------------------------------------------------------------
        # simple menu to functions
        mainMenu = self.menuBar()
        #--------------------------------------------------------------------------------------------------------------
        # File option
        fileMenu        = mainMenu.addMenu('File')
        loadcsvData     = Qt.QAction('Load csv data', self)
        exitButton      = Qt.QAction('Exit', self)

        exitButton.setShortcut('Ctrl+Q')
        loadcsvData.triggered.connect(self.load_csv_file)
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(loadcsvData)
        fileMenu.addAction(exitButton)
        #--------------------------------------------------------------------------------------------------------------
        # Path Orbit option
        OrbMenu         = mainMenu.addMenu('Orbit')
        orbit_action    = Qt.QAction('Show Orbit', self)
        cad_action      = Qt.QAction('Add satellite', self)
        orbit_action.triggered.connect(self.add_orbit)
        cad_action.triggered.connect(self.add_spacecraft_2_orbit)

        OrbMenu.addAction(orbit_action)
        OrbMenu.addAction(cad_action)
        #--------------------------------------------------------------------------------------------------------------
        # Attitude
        AttMenu         = mainMenu.addMenu('Attitude')
        sat_action      = Qt.QAction('Add satellite', self)
        frame_action    = Qt.QAction('Add reference frame', self)

        sat_action.triggered.connect(self.add_spacecraft_2_attitude)
        AttMenu.addAction(sat_action)
        frame_action.triggered.connect(self.add_i_frame_attitude)
        AttMenu.addAction(frame_action)
        #--------------------------------------------------------------------------------------------------------------
        # Simulation option
        SimMenu         = mainMenu.addMenu('Simulation')
        run_action      = Qt.QAction('Run', self)
        pause_action    = Qt.QAction('Pause', self)
        stop_action     = Qt.QAction('Stop', self)

        run_action.triggered.connect(self.run_simulation)
        pause_action.triggered.connect(self.pause_simulation)
        stop_action.triggered.connect(self.stop_simulation)

        SimMenu.addAction(run_action)
        SimMenu.addAction(pause_action)
        SimMenu.addAction(stop_action)
        #--------------------------------------------------------------------------------------------------------------
        graph2dMenu = mainMenu.addMenu('Data')
        plot_action = Qt.QAction('Generate graph', self)

        plot_action.triggered.connect(self.add_graph2d)

        graph2dMenu.addAction(plot_action)
        #--------------------------------------------------------------------------------------------------------------

        if show:
            self.show()

    def add_graph2d(self):
        self.screen = MainGraph(self.dataLog)
        self.screen.win.show()

    def load_csv_file(self):
        def read_data(file_path):
            df = pd.read_csv(file_path, delimiter=',')
            sim_data = df
            return sim_data

        Tk().withdraw()
        filename = askopenfilename()
        self.dataLog = read_data(filename)
        print('Data lag created')

    def run_simulation(self):
        self.run_flag = True
        self.run_orbit_3d()
        print('Running...')
        return

    def pause_simulation(self):
        self.pause_flag = True
        self.run_flag = False
        print('Paused...')

        return

    def stop_simulation(self):
        return

    def rotate_th(self):
        self.vtk_widget.subplot(0,0)
        i = 1
        self.simtime.reset()
        while self.simtime.countTime <= self.simtime.end:
            while self.pause_flag:
                if self.run_flag:
                    self.pause_flag = False

            # Update Orbit
            self.sphere.rotate_z((self.earth_gst[i] - self.earth_gst[i - 1])*500)
            self.current_pos = self.sat_dynamics['Orbital']['Position'][i, :] - self.sat_dynamics['Orbital']['Position'][i - 1, :]
            self.spacecraft_in_orbit.translate(self.current_pos)

            # Update Attitude
            self.vtk_widget.update()
            time.sleep(self.simtime.step/self.time_speed)

            # update time
            self.simtime.countTime += self.simtime.step
            self.simtime.update_time()
            i += 1
        self.thread = None

    def run_orbit_3d(self):
        if self.thread == None:
            self.thread = Thread(target = self.rotate_th, daemon = True)
            self.thread.start()

    def sim_speed(self, value):
        self.time_speed = value
        return

if __name__ == '__main__':
    app = Qt.QApplication(sys.argv)
    window = Main3D()
    sys.exit(app.exec_())