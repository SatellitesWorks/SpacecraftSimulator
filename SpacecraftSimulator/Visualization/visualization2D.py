
from pyqtgraph.Qt import QtGui, QtCore

import numpy as np
import pyqtgraph as pg
import sys

rad2deg = 180/np.pi

class MainGraph(object):
    def __init__(self, datalog = None):
        self.datalog = datalog
        #QtGui.QApplication.setGraphicsSystem('raster')

        #mw = QtGui.QMainWindow()
        #mw.resize(800,800)

        self.win = pg.GraphicsWindow(title="Fly Simulator")
        self.win.resize(1000,600)
        self.win.setWindowTitle('Satellite components')

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        self.plot_all()

    def plot_all(self):
        self.plot1()
        self.plot2()
        self.plot3()
        self.win.nextRow()
        self.plot4()
        self.plot5()
        self.plot6()
        self.win.nextRow()
        self.plot7()
        self.plot8()
        self.plot9()

    def plot1(self):
        p1 = self.win.addPlot(title="Groundtrack")
        p1.plot(rad2deg*np.array(self.datalog['lon[rad]']), rad2deg*np.array(self.datalog['lat[rad]']))
        p1.showGrid(x=True, y=True)

    def plot2(self):

        p2 = self.win.addPlot(title="'Omega_t_b' and 'gyro_omega1_c' [rad/s]")
        p2.plot(np.array(self.datalog['omega_t_b(X)[rad/s]']), pen=(255,0,0), name="omega_t_b(X)")
        p2.plot(np.array(self.datalog['omega_t_b(Y)[rad/s]']), pen=(0,255,0), name="omega_t_b(Y)")
        p2.plot(np.array(self.datalog['omega_t_b(Z)[rad/s]']), pen=(0,0,255), name="omega_t_b(Z)")
        p2.showGrid(x=True, y=True)
        diam = 2
        p2.plot(np.array(self.datalog['gyro_omega1_c(X)[rad/s]']), pen=None, symbolBrush=(240,0,0),
                symbolPen='w', symbolSize = diam, name="gyro_omega1_c(X)")
        p2.plot(np.array(self.datalog['gyro_omega1_c(Y)[rad/s]']), pen=None, symbolBrush=(0,240,0),
                symbolPen='w', symbolSize = diam, name="gyro_omega1_c(Y)")
        p2.plot(np.array(self.datalog['gyro_omega1_c(Z)[rad/s]']), pen=None, symbolBrush=(0,0,240),
                symbolPen='w', symbolSize = diam, name="gyro_omega1_c(Z)")

    def plot3(self):
        p3 = self.win.addPlot(title="Drawing with points")
        p3.plot(np.random.normal(size=100), pen=(200,200,200), symbolBrush=(255,0,0), symbolPen='w')

    def plot4(self):
        p4 = self.win.addPlot(title="Parametric, grid enabled")
        x = np.cos(np.linspace(0, 2 * np.pi, 1000))
        y = np.sin(np.linspace(0, 4 * np.pi, 1000))
        p4.plot(x, y)
        p4.showGrid(x=True, y=True)

    def plot5(self):
        p5 = self.win.addPlot(title="Scatter plot, axis labels, log scale")
        x = np.random.normal(size=1000) * 1e-5
        y = x * 1000 + 0.005 * np.random.normal(size=1000)
        y -= y.min() - 1.0
        mask = x > 1e-15
        x = x[mask]
        y = y[mask]
        p5.plot(x, y, pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 50))
        p5.setLabel('left', "Y Axis", units='A')
        p5.setLabel('bottom', "Y Axis", units='s')
        p5.setLogMode(x=True, y=False)

    def plot6(self):
        p6 = self.win.addPlot(title="Updating plot")
        curve = p6.plot(pen='y')
        data = np.random.normal(size=(10, 1000))
        ptr = 0

        def update():
            global curve, data, ptr, p6
            curve.setData(data[ptr % 10])
            if ptr == 0:
                p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
            ptr += 1

        timer = QtCore.QTimer()
        timer.timeout.connect(update)
        timer.start(50)

    def plot7(self):
        p7 = self.win.addPlot(title="Filled plot, axis disabled")
        y = np.sin(np.linspace(0, 10, 1000)) + np.random.normal(size=1000, scale=0.1)
        p7.plot(y, fillLevel=-0.3, brush=(50, 50, 200, 100))
        p7.showAxis('bottom', False)

    def plot8(self):
        x2 = np.linspace(-100, 100, 1000)
        data2 = np.sin(x2) / x2
        p8 = self.win.addPlot(title="Region Selection")
        p8.plot(data2, pen=(255, 255, 255, 200))
        lr = pg.LinearRegionItem([400, 700])
        lr.setZValue(-10)
        p8.addItem(lr)

    def plot9(self):
        x2 = np.linspace(-100, 100, 1000)
        lr = pg.LinearRegionItem([400, 700])
        data2 = np.sin(x2) / x2
        lr.setZValue(-10)
        p9 = self.win.addPlot(title="Zoom on selected region")
        p9.plot(data2)
        def updatePlot():
            p9.setXRange(*lr.getRegion(), padding=0)

        def updateRegion():
            lr.setRegion(p9.getViewBox().viewRange()[0])

        lr.sigRegionChanged.connect(updatePlot)
        p9.sigXRangeChanged.connect(updateRegion)
        updatePlot()

## Start Qt event loop unless running in interactive mode or using pyside.

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    wd  = MainGraph()
    app.instance().exec_()